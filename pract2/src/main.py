import argparse
from validation import validate_args
from repository import get_direct_dependencies
from urllib.error import HTTPError, URLError

parser = argparse.ArgumentParser(
    description="Визуализация зависимостей пакетов Cargo"
)

#Аргументы парсера
parser.add_argument(
    "--package",
    required=True,
    help="Имя анализируемого пакета"
)

parser.add_argument(
    "--version",
    required=True,
    help="Версия пакета"
)

parser.add_argument(
    "--repository",
    required=True,
    help="URL-адрес репозитория или путь к файлу тестового репозитория"
)

parser.add_argument(
    "--output",
    default="graph.svg",
    help="Имя сгенерированного файла с изображением графа"
)

parser.add_argument(
    "--test",
    action="store_true",
    help="Использовать локальный тестовый репозиторий"
)

parser.add_argument(
    "--ascii",
    action="store_true",
    help="Режим вывода зависимостей в формате ASCII-дерева"
)

parser.add_argument(
    "--filter",
    default="",
    help="Подстрока для фильтрации пакетов"
)

args = parser.parse_args()
validate_args(args, parser)

try:
    dependencies = get_direct_dependencies(
        args.repository, args.package, args.version
    )
except HTTPError as error:
    parser.error(f"Ошибка HTTP {error.code} при получении пакета")
except URLError as error:
    parser.error("Не удалось подключиться к репозиторию: {error.reason}")
except TimeoutError as error:
    parser.error("Истекло время ожидания ответа")
except ValueError as error:
    parser.error(str(error))

if not dependencies:
    print("У пакета нет зависимостей")
else:
    for dependency in dependencies:
        name = dependency.get("package") or dependency["name"]
        ver = dependency["req"]
        print(f"{name}:{ver}")