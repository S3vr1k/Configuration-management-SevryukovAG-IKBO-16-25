from collections import deque

# Сначала пакеты без зависимостей, затем использующие их пакеты
def get_load_order(graph):
    remaining = {}
    parents = {package: [] for package in graph}
    for package, dependencies in graph.items():
        remaining[package] = len(dependencies)
        for dependency in dependencies:
            parents[dependency].append(package)

    queue = deque(
        package for package in graph if remaining[package] == 0
    )
    order = []
    while queue:
        package = queue.popleft()
        order.append(package)
        for parent in parents[package]:
            remaining[parent] -= 1
            if remaining[parent] == 0:
                queue.append(parent)

    if len(order) != len(graph):
        raise ValueError("Цикл: порядок загрузки зависимостей невозможен")
    return order
