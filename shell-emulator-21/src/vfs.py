"""Загрузка CSV в виртуальную файловую систему в памяти."""

import base64
import binascii
import csv
from pathlib import PurePosixPath

COLUMNS = ["path", "type", "content_base64"]


class VirtualFileSystem:
    """Хранит виртуальные папки и содержимое файлов в словаре."""

    def __init__(self, nodes=None):
        """Принимает загруженные узлы или создаёт пустой корень."""
        if nodes is None:
            nodes = {"/": {"type": "dir", "content": b""}}
        self.nodes = nodes

    def get_motd(self):
        """Возвращает текст /motd либо None, если файла нет."""
        node = self.nodes.get("/motd")
        if node is None:
            return None
        if node["type"] != "file":
            raise ValueError("/motd должен быть файлом")
        return node["content"].decode("utf-8")


def validate_path(path):
    """Проверяет абсолютный путь без точек и лишних разделителей."""
    parsed = PurePosixPath(path)
    if parsed.root != "/" or str(parsed) != path:
        raise ValueError(f"Неверный виртуальный путь: {path!r}")
    if ".." in parsed.parts or "\x00" in path:
        raise ValueError(f"Недопустимый виртуальный путь: {path!r}")


def parse_row(row):
    """Проверяет строку CSV и декодирует содержимое узла."""
    if set(row) != set(COLUMNS) or None in row.values():
        raise ValueError("Неверное количество полей в строке CSV")

    path = row["path"]
    kind = row["type"]
    encoded = row["content_base64"]
    validate_path(path)

    if kind not in ("file", "dir"):
        raise ValueError(f"Неизвестный тип узла: {kind!r}")
    if kind == "dir" and encoded:
        raise ValueError(f"У папки не должно быть содержимого: {path}")

    try:
        content = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError) as error:
        raise ValueError(f"Неверный base64 у файла {path}") from error

    return path, {"type": kind, "content": content}


def validate_nodes(nodes):
    """Проверяет корень и наличие родительских папок."""
    if nodes.get("/", {}).get("type") != "dir":
        raise ValueError("VFS должна содержать корневую папку /")

    for path in nodes:
        if path == "/":
            continue
        parent = str(PurePosixPath(path).parent)
        if nodes.get(parent, {}).get("type") != "dir":
            raise ValueError(f"Нет родительской папки для {path}")


def load_vfs(filename):
    """Читает CSV без изменения файла и возвращает готовую VFS."""
    nodes = {}
    try:
        with open(filename, encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream, strict=True)
            if reader.fieldnames != COLUMNS:
                raise ValueError(f"Ожидаются столбцы: {COLUMNS}")

            for row in reader:
                path, node = parse_row(row)
                if path in nodes:
                    raise ValueError(f"Повторяющийся путь: {path}")
                nodes[path] = node
    except csv.Error as error:
        raise ValueError(f"Неверный формат CSV: {error}") from error

    validate_nodes(nodes)
    return VirtualFileSystem(nodes)
