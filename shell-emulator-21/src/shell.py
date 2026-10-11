"""Заглушки ls, cd и завершение"""
from src.parser import parse_command

MAX_PATH_ARGUMENTS = 1


def execute_command(text):
    """Возвращает текст ответа и признак завершения"""
    tokens = parse_command(text)

    if not tokens:
        return "", False

    command = tokens[0]
    arguments = tokens[1:]

    if command == "exit":
        if arguments:
            raise ValueError("exit не принимает аргументы")
        return "", True

    if command not in ("ls", "cd"):
        raise ValueError(f"Неизвестная команда {command}")

    if len(arguments) > MAX_PATH_ARGUMENTS:
        raise ValueError(f"{command}: ожидается не более одного пути")

    return f"Команда: {command}; аргументы: {arguments!r}", False