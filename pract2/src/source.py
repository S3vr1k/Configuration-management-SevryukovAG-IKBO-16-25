import json
from repository import fetch_text, get_package_path
from test_repository import load_test_repository
from versions import matches_version, version_numbers

# Одна загрузка метаданных на имя пакета за запуск
def create_source(repository, test):
    cache = {}
    data = load_test_repository(repository) if test else None

    def get_records(name):
        if name not in cache:
            if test:
                if name not in data:
                    raise ValueError("Пакет не найден: " + name)
                cache[name] = [
                    {"vers": version, "deps": dependencies}
                    for version, dependencies in data[name].items()
                ]
            else:
                url = repository.rstrip("/") + "/" + get_package_path(name)
                text = fetch_text(url)
                cache[name] = [json.loads(line) for line in text.splitlines()
                               if line.strip()]
        return cache[name]

    def get_dependencies(name, version):
        for record in get_records(name):
            if record["vers"] == version:
                for dependency in record["deps"]:
                    if dependency.get("registry"):
                        raise ValueError("Другой реестр не поддерживается")
                return record["deps"]
        raise ValueError("Версия пакета не найдена: " + name + " " + version)

    def resolve_version(name, requirement):
        return select_version(get_records(name), requirement, name)

    return get_dependencies, resolve_version

# Выбираем максимальную подходящую стабильную, не отозванную версию
def select_version(records, requirement, name):
    candidates = []
    for record in records:
        version = record["vers"]
        if record.get("yanked") or "-" in version.split("+")[0]:
            continue
        if matches_version(version, requirement):
            candidates.append(version)
    if not candidates:
        raise ValueError("Нет подходящей версии: " + name + " " + requirement)
    return max(candidates, key=version_numbers)
