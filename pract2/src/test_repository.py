import json

# Формат: имя -> версия -> список объектов name, req
def load_test_repository(path):
    with open(path, encoding="utf-8") as file:
        data = json.load(file)
    
    if not isinstance(data, dict):
        raise ValueError("Тестовый репозиторий должен быть JSON-объектом")
    
    for name, versions in data.items():
        if not name or any(letter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                           for letter in name):
            raise ValueError("Имена тестовых пакетов: заглавные A-Z")
        
        if not isinstance(versions, dict):
            raise ValueError("Для пакета нужен словарь версий")
        
        for dependencies in versions.values():
            if not isinstance(dependencies, list):
                raise ValueError("Зависимости должны быть списком")
            
            for dependency in dependencies:
                if not isinstance(dependency, dict):
                    raise ValueError("Зависимость должна быть объектом")
                
                if not all(isinstance(dependency.get(key), str)
                           for key in ("name", "req")):
                    raise ValueError("У зависимости нужны строки name и req")
    return data
