from urllib.request import urlopen
import json

def get_direct_dependencies(repository, name, version):
    path = get_package_path(name)
    url = repository.rstrip("/") + "/" + path

    text = fetch_text(url)
    record = parse_package_version(text, version)

    return record["deps"]

#Получить текст по http
def fetch_text(url):
    with urlopen(url, timeout=15) as response:
        return response.read().decode("utf-8")

#Получить путь на Cargo
def get_package_path(name):
    name = name.lower()

    if not name:
        raise ValueError("Имя пакета не должно быть пустым")
    elif len(name) <= 2:
        return f"{len(name)}/{name}"
    elif len(name) == 3:
        return f"3/{name[0]}/{name}"
    else:
        return f"{name[:2]}/{name[2:4]}/{name}"

#Получить версию из json
def parse_package_version(text, version):
    for line in text.splitlines():
        if not line.strip():
            continue
        record = json.loads(line)

        if record["vers"] == version:
            return record
    raise ValueError("Версия пакета не найдена")