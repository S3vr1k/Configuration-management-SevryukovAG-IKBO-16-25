"""Проверки настроек и стартового скрипта без графического окна."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.config import parse_options
from src.startup import run_script


class ConfigTests(unittest.TestCase):
    """Проверяет параметры запуска."""

    def test_defaults(self):
        """Без параметров оба пути равны None."""
        options = parse_options([])
        self.assertIsNone(options.vfs)
        self.assertIsNone(options.script)

    def test_paths(self):
        """Оба параметра сохраняют переданные пути."""
        options = parse_options([
            "--vfs", "fixtures/demo.csv",
            "--script", "scripts/my script.txt",
        ])
        self.assertEqual(options.vfs, "fixtures/demo.csv")
        self.assertEqual(options.script, "scripts/my script.txt")


class StartupTests(unittest.TestCase):
    """Проверяет порядок команд, ошибки и завершение."""

    def setUp(self):
        """Создаёт временную папку и список сообщений."""
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.script = Path(self.directory.name) / "startup.txt"
        self.messages = []

    def run_text(self, text):
        """Записывает тестовый скрипт и выполняет его."""
        self.script.write_text(text, encoding="utf-8")
        return run_script(self.script, self.messages.append)

    def test_success(self):
        """Команды и результаты выводятся в правильном порядке."""
        should_exit = self.run_text("ls /\n\ncd /docs\n")
        self.assertFalse(should_exit)
        self.assertEqual(self.messages, [
            "> ls /",
            "Команда: ls; аргументы: ['/']",
            "> cd /docs",
            "Команда: cd; аргументы: ['/docs']",
        ])

    def test_first_error(self):
        """После неизвестной команды следующая строка не выполняется."""
        self.run_text("ls /\nunknown\ncd /after-error\n")
        self.assertNotIn("> cd /after-error", self.messages)
        self.assertTrue(any(
            "Ошибка в строке 2" in text for text in self.messages
        ))

    def test_invalid_arguments(self):
        """Лишние аргументы также останавливают скрипт."""
        self.run_text("ls one two\ncd /after-error\n")
        self.assertNotIn("> cd /after-error", self.messages)

    def test_invalid_quotes(self):
        """Незакрытая кавычка останавливает скрипт."""
        self.run_text('cd "unfinished\nls /after-error\n')
        self.assertNotIn("> ls /after-error", self.messages)

    def test_exit(self):
        """Exit завершает скрипт до последующих строк."""
        should_exit = self.run_text("exit\nls /after-exit\n")
        self.assertTrue(should_exit)
        self.assertEqual(self.messages, ["> exit"])

    def test_missing_file(self):
        """Отсутствующий файл даёт сообщение, а не исключение."""
        should_exit = run_script(self.script, self.messages.append)
        self.assertFalse(should_exit)
        self.assertIn("Ошибка чтения скрипта", self.messages[0])

    def test_invalid_encoding(self):
        """Файл не в UTF-8 обрабатывается как ошибка чтения."""
        self.script.write_bytes(b"\xff")
        run_script(self.script, self.messages.append)
        self.assertIn("Ошибка чтения скрипта", self.messages[0])
