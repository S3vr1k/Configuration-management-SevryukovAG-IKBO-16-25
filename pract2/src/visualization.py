import json
import subprocess
from pathlib import Path

# Строки в кавычках безопасно передаются в язык DOT
def package_label(package):
    name, version = package
    return f"{name}@{version}"

# Отдельно объявляем вершины, чтобы сохранить пакеты без зависимостей
def make_dot(graph):
    lines = ["digraph dependencies {", "    rankdir=LR;"]
    for package, dependencies in graph.items():
        parent = json.dumps(package_label(package), ensure_ascii=False)
        lines.append(f"    {parent};")
        for dependency in dependencies:
            child = json.dumps(package_label(dependency), ensure_ascii=False)
            lines.append(f"    {parent} -> {child};")
    lines.append("}")
    return "\n".join(lines) + "\n"

# Сохраняем DOT рядом с SVG и вызываем Graphviz без командной оболочки
def save_graph(graph, output):
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    dot = make_dot(graph)
    path.with_suffix(".dot").write_text(dot, encoding="utf-8")
    try:
        result = subprocess.run(
            ["dot", "-Tsvg"], input=dot, text=True, encoding="utf-8",
            capture_output=True, check=True
        )
    except FileNotFoundError:
        raise ValueError("Graphviz не установлен: sudo pacman -S graphviz")
    except subprocess.CalledProcessError as error:
        raise ValueError("Ошибка Graphviz: " + error.stderr.strip())
    path.write_text(result.stdout, encoding="utf-8")

# Стек вместо рекурсии; повторные вершины не разворачиваются заново
def make_ascii_tree(graph):
    if not graph:
        return "Граф пуст"
    root = next(iter(graph))
    lines = []
    visited = set()
    stack = [(root, "", "", "")]
    while stack:
        package, prefix, branch, children_prefix = stack.pop()
        repeated = package in visited
        label = package_label(package)
        lines.append(prefix + branch + label + (" (*)" if repeated else ""))
        if repeated:
            continue
        visited.add(package)
        children = graph[package]
        for i in range(len(children) - 1, -1, -1):
            last = i == len(children) - 1
            marker = "`-- " if last else "|-- "
            padding = "    " if last else "|   "
            stack.append((children[i], children_prefix, marker,
                          children_prefix + padding))
    return "\n".join(lines)
