from collections import deque

# BFS без рекурсии
def build_graph(name, version, get_dependencies, resolve_version, exclude):
    root = (name, version)
    graph = {}

    if exclude and exclude in name:
        return graph
    
    queue = deque([root])
    visited = {root}

    while queue:
        current = queue.popleft()
        graph[current] = []
        for dependency in get_dependencies(*current):
            child_name = dependency.get("package") or dependency["name"]
            
            if exclude and exclude in child_name:
                continue
            
            child_version = resolve_version(child_name, dependency["req"])
            child = (child_name, child_version)
            
            if child not in graph[current]:
                graph[current].append(child)
            if child not in visited:
                visited.add(child)
                queue.append(child)
    
    return graph
