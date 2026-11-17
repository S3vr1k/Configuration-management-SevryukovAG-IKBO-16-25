import argparse

def parse_options(arguments=None):
    """Читает параметры из списка или командной строки процесса"""
    parser = argparse.ArgumentParser(
        description="Эмулятор оболочки, вариант 21",
        allow_abbrev=False,
    )

    parser.add_argument(
        "--vfs",
        metavar="PATH",
        help="Путь к файлу виртуальной файловой системы",
    )

    parser.add_argument(
        "--script",
        metavar="PATH",
        help="Путь к стартовому скрипту эмулятора",
    )

    return parser.parse_args(arguments)