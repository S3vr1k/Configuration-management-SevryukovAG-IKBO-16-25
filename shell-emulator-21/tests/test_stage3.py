"""Проверки CSV, памяти, motd и связи с запуском приложения."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

from src.config import parse_options
from src.gui import EmulatorWindow
from src.vfs import VirtualFileSystem, load_vfs

HEADER = "path,type,content_base64\n"
FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


class VfsTests(unittest.TestCase):
    """Проверяет корректные и повреждённые VFS."""

    def setUp(self):
        """Создаёт отдельную папку и имя CSV для каждого теста."""
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.filename = Path(self.directory.name) / "vfs.csv"

    def load_text(self, text):
        """Записывает текст тестового CSV и загружает его."""
        self.filename.write_text(text, encoding="utf-8")
        return load_vfs(self.filename)

    def test_default(self):
        """Без CSV создаётся только корень, сообщения motd нет."""
        vfs = VirtualFileSystem()
        self.assertEqual(list(vfs.nodes), ["/"])
        self.assertIsNone(vfs.get_motd())

    def test_fixtures(self):
        """Все три примера загружаются в память."""
        for name, count in (
            ("minimal.csv", 1), ("several.csv", 5), ("nested.csv", 8),
        ):
            with self.subTest(name=name):
                vfs = load_vfs(FIXTURES / name)
                self.assertEqual(len(vfs.nodes), count)
        vfs = load_vfs(FIXTURES / "nested.csv")
        path = "/docs/projects/demo/hello.txt"
        self.assertEqual(vfs.nodes[path]["content"], b"Hello\n")

    def test_binary_and_motd(self):
        """Двоичные данные и motd декодируются без потерь."""
        vfs = load_vfs(FIXTURES / "several.csv")
        self.assertEqual(vfs.nodes["/data.bin"]["content"], b"\x00\xffA")
        self.assertEqual(vfs.get_motd(), "Welcome!\n")

    def test_source_unchanged(self):
        """Изменение памяти не меняет CSV, загрузка восстанавливает узел."""
        self.filename.write_text(HEADER + "/,dir,\n/a,file,\n")
        before = self.filename.read_bytes()
        vfs = load_vfs(self.filename)
        del vfs.nodes["/a"]
        self.assertEqual(self.filename.read_bytes(), before)
        self.assertIn("/a", load_vfs(self.filename).nodes)

    def test_child_before_parent(self):
        """Порядок строк не влияет на проверку родительских папок."""
        vfs = self.load_text(HEADER + "/a/b,file,\n/a,dir,\n/,dir,\n")
        self.assertIn("/a/b", vfs.nodes)

    def test_invalid_structure(self):
        """Отвергает плохие поля, типы, дубликаты, связи и base64."""
        examples = (
            "wrong,header\n",
            HEADER,
            HEADER + "/,file,\n",
            HEADER + "/,dir,\n/a,dir,\n/a,dir,\n",
            HEADER + "/,dir,\n/a/b,file,\n",
            HEADER + "/,dir,\n/a,file,\n/a/b,file,\n",
            HEADER + "/,dir,\n/a,unknown,\n",
            HEADER + "/,dir,\n/a,dir,SGVsbG8K\n",
            HEADER + "/,dir,\n/a,file\n",
            HEADER + "/,dir,extra,field\n",
            HEADER + "/,dir,\n/a,file,%%%\n",
            HEADER + "/,dir,\n/a,file,текст\n",
            HEADER + '/,dir,\n"/unfinished,file,\n',
        )
        for text in examples:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    self.load_text(text)

    def test_invalid_paths(self):
        """В CSV нужны канонические абсолютные пути."""
        paths = ("a", "//a", "/a/", "/a//b", "/a/../b", "/a/./b")
        for path in paths:
            with self.subTest(path=path):
                with self.assertRaises(ValueError):
                    self.load_text(HEADER + f"/,dir,\n{path},file,\n")

    def test_read_errors(self):
        """Отсутствующий файл и неверный UTF-8 вызывают ошибки."""
        with self.assertRaises(OSError):
            load_vfs(self.filename)
        self.filename.write_bytes(b"\xff")
        with self.assertRaises(UnicodeError):
            load_vfs(self.filename)

    def test_utf8_bom(self):
        """CSV с меткой UTF-8 BOM также читается."""
        vfs = self.load_text("\ufeff" + HEADER + "/,dir,\n")
        self.assertIn("/", vfs.nodes)

    def test_invalid_motd(self):
        """Папка и нетекстовые данные не подходят для motd."""
        vfs = self.load_text(HEADER + "/,dir,\n/motd,dir,\n")
        with self.assertRaises(ValueError):
            vfs.get_motd()
        vfs = self.load_text(HEADER + "/,dir,\n/motd,file,/w==\n")
        with self.assertRaises(UnicodeError):
            vfs.get_motd()


class StartupIntegrationTests(unittest.TestCase):
    """Проверяет метод запуска без создания настоящего окна."""

    def test_default(self):
        """Без параметров GUI получает пустую VFS."""
        window = Mock()
        EmulatorWindow.run_startup(window, parse_options([]))
        self.assertEqual(list(window.vfs.nodes), ["/"])
        window.root.destroy.assert_not_called()

    def test_motd_before_script(self):
        """Motd появляется перед выполнением стартового скрипта."""
        window = Mock()
        options = parse_options([
            "--vfs", str(FIXTURES / "nested.csv"),
            "--script", "startup.txt",
        ])

        def check_order(filename, write):
            """Проверяет состояние в момент запуска скрипта."""
            window.write.assert_any_call("Welcome!")
            self.assertIn("/docs/projects/demo", window.vfs.nodes)
            return False

        with patch("src.gui.run_script", side_effect=check_order):
            EmulatorWindow.run_startup(window, options)

    def test_error_blocks_script(self):
        """После ошибки VFS ввод блокируется, скрипт не запускается."""
        window = Mock()
        options = parse_options([
            "--vfs", str(FIXTURES / "invalid.csv"),
            "--script", "startup.txt",
        ])
        with patch("src.gui.run_script") as runner:
            EmulatorWindow.run_startup(window, options)
            runner.assert_not_called()
        window.entry.configure.assert_called_once_with(state="disabled")
