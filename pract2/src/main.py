import argparse
from validation import validate_args
from source import create_source
from graph import build_graph
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
    get_dependencies, resolve_version = create_source(
        args.repository, args.test
    )
    graph = build_graph(
        args.package, args.version, get_dependencies,
        resolve_version, args.filter
    )
except HTTPError as error:
    parser.error(f"Ошибка HTTP {error.code} при получении пакета")
except URLError as error:
    parser.error(f"Не удалось подключиться: {error.reason}")
except TimeoutError as error:
    parser.error("Истекло время ожидания ответа")
except OSError as error:
    parser.error(f"Ошибка чтения данных: {error}")
except (ValueError, KeyError, TypeError) as error:
    parser.error(str(error))

if not graph:
    print("Граф пуст: исходный пакет исключен фильтром")
else:
    for package, dependencies in graph.items():
        name, version = package
        children = ", ".join(
            f"{child_name}@{child_version}"
            for child_name, child_version in dependencies
        )
        print(f"{name}@{version}: {children or 'нет зависимостей'}")
