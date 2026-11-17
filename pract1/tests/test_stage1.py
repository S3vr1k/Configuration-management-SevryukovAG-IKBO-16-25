import os
import unittest

from src.parser import parse_command
from src.shell import execute_command


class StageOneTests(unittest.TestCase):
    """Проверка разбора ввода и обработки команд"""

    def test_parser(self):
        """Проверка обработки кавычек"""
        result = parse_command('cd "my folder"')
        self.assertEqual(result, ["cd", "my folder"])

    def test_home(self):
        """Проверка HOME"""
        result = parse_command("cd $HOME")
        self.assertEqual(result, ["cd", os.environ["HOME"]])

    def test_stub(self):
        """Проверка. вывода имени и аргументов"""
        output, should_exit = execute_command("ls /docs")
        self.assertEqual(
            output,
            "Команда: ls; аргументы: ['/docs']",
        )
        self.assertFalse(should_exit)

    def test_exit(self):
        """Проверка exit"""
        self.assertEqual(execute_command("exit"), ("", True))

    def test_errors(self):
        """Проверка исключений"""
        examples = (
            "unknown",
            "ls one two",
            "exit extra",
            'cd "unfinished',
        )

        for text in examples:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    execute_command(text)