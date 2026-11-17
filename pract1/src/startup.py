"""Выполнение стартового скрипта до первой ошибки."""

from pathlib import Path

from src.shell import execute_command


def run_script(filename, write):
    """Выводит диалог и возвращает True только при команде exit."""
    try:
        lines = Path(filename).read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        write(f"Ошибка чтения скрипта {filename}: {error}")
        return False

    for number, text in enumerate(lines, start=1):
        if not text.strip():
            continue

        write(f"> {text}")

        try:
            output, should_exit = execute_command(text)
        except ValueError as error:
            write(f"Ошибка в строке {number}: {error}")
            write("Выполнение стартового скрипта остановлено.")
            return False

        if output:
            write(output)

        if should_exit:
            return True

    return False