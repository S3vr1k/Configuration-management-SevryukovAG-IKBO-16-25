import argparse
from validation import validate_args

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

#Вывод информации
print(f"package={args.package}")
print(f"version={args.version}")
print(f"repository={args.repository}")
print(f"output={args.output}")
print(f"test={args.test}")
print(f"ascii={args.ascii}")
print(f"filter={args.filter}")