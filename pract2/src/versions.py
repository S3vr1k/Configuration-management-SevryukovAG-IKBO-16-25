import re

# Версии сравниваются как тройки чисел
def version_numbers(version):
    core = version.split("+")[0]
    
    if not re.fullmatch(r"\d+\.\d+\.\d+", core):
        raise ValueError("Нужна стабильная версия: " + version)
    
    return tuple(int(number) for number in core.split("."))

# Проверка одного ограничения
def matches_part(version, requirement):
    match = re.fullmatch(
        r"(>=|<=|>|<|=|\^|~)?\s*(\d+(?:\.\d+){0,2}|\*)(\.\*)?",
        requirement.strip()
    )
    
    if not match:
        raise ValueError("Неподдерживаемое требование: " + requirement)
    operator, number, wildcard = match.groups()
    
    if number == "*":
        return True
    
    parts = tuple(int(value) for value in number.split("."))
    lower = parts + (0,) * (3 - len(parts))
    
    if wildcard or operator == "=":
        return version[:len(parts)] == parts
    if operator in (">", "<", ">=", "<="):
        return compare_numbers(version[:len(parts)], parts, operator)
    if operator == "~":
        position = min(1, len(parts) - 1)
    else:
        position = next(
            (i for i, value in enumerate(parts) if value != 0),
            len(parts) - 1
        )
    upper = list(lower)
    upper[position] += 1
    
    for i in range(position + 1, 3):
        upper[i] = 0
    return lower <= version < tuple(upper)

def compare_numbers(left, right, operator):
    if operator == ">":
        return left > right
    if operator == "<":
        return left < right
    if operator == ">=":
        return left >= right
    return left <= right

def matches_version(version, requirement):
    numbers = version_numbers(version)
    
    return all(matches_part(numbers, part) for part in requirement.split(","))
