from queue import PriorityQueue

# Datos del problema: conexiones entre ciudades y distancias
graph = {
    'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
    'Zerind': [('Arad', 75), ('Oradea', 71)],
    'Oradea': [('Zerind', 71), ('Sibiu', 151)],
    'Sibiu': [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
    'Timisoara': [('Arad', 118), ('Lugoj', 111)],
    'Lugoj': [('Timisoara', 111), ('Mehadia', 70)],
    'Mehadia': [('Lugoj', 70), ('Drobeta', 75)],
    'Drobeta': [('Mehadia', 75), ('Craiova', 120)],
    'Craiova': [('Drobeta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
    'Rimnicu Vilcea': [('Sibiu', 80), ('Craiova', 146), ('Pitesti', 97)],
    'Fagaras': [('Sibiu', 99), ('Bucharest', 211)],
    'Pitesti': [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucharest', 101)],
    'Bucharest': [('Fagaras', 211), ('Pitesti', 101), ('Giurgiu', 90), ('Urziceni', 85)],
    'Giurgiu': [('Bucharest', 90)],
    'Urziceni': [('Bucharest', 85), ('Hirsova', 98), ('Vaslui', 142)],
    'Hirsova': [('Urziceni', 98), ('Eforie', 86)],
    'Eforie': [('Hirsova', 86)],
    'Vaslui': [('Urziceni', 142), ('Iasi', 92)],
    'Iasi': [('Vaslui', 92), ('Neamt', 87)],
    'Neamt': [('Iasi', 87)],
}

# Distancias heurísticas (en línea recta) hasta Bucharest
heuristic = {
    'Arad': 366, 'Bucharest': 0, 'Craiova': 160, 'Drobeta': 242, 'Eforie': 161,
    'Fagaras': 176, 'Giurgiu': 77, 'Hirsova': 151, 'Iasi': 226, 'Lugoj': 244,
    'Mehadia': 241, 'Neamt': 234, 'Oradea': 380, 'Pitesti': 100, 'Rimnicu Vilcea': 193,
    'Sibiu': 253, 'Timisoara': 329, 'Urziceni': 80, 'Vaslui': 199, 'Zerind': 374,
}

# Implementación del algoritmo Greedy
def greedy_search(graph, heuristic, start, goal):
    """
    Realiza una búsqueda heurística tipo Greedy para encontrar un camino desde
    el nodo inicial (start) hasta el nodo objetivo (goal).

    Argumentos:
        graph (dict): Grafo que representa las conexiones entre ciudades.
        heuristic (dict): Diccionario con las estimaciones heurísticas.
        start (str): Nodo inicial.
        goal (str): Nodo objetivo.

    Returns:
        list: Camino encontrado, o None si no se encuentra solución.
    """
    # Cola de prioridad para gestionar los nodos por heurística
    frontier = PriorityQueue() 
    #Se agrega el nodo inicial con su heurística
    frontier.put((heuristic[start], start))  
    # Conjunto de nodos visitados
    visited = set() 
    # Almacena el camino recorrido
    path = []
    
    while not frontier.empty():
        # Extrae el nodo con menor valor heurístico
        _, current = frontier.get()
        path.append(current)

        # Verifica si se alcanzó el nodo objetivo
        if current == goal: 
            return path
        
        # Marca el nodo actual como visitado
        visited.add(current) 
        
        # Explora los vecinos del nodo actual
        for neighbor, cost in graph[current]:
            if neighbor not in visited:
                frontier.put((heuristic[neighbor], neighbor))
    
    return None # Retorna None si no se encuentra un camino al objetivo

# Implementación del algoritmo A*
def a_star_search(graph, heuristic, start, goal):
    """
    Realiza una búsqueda tipo A* para encontrar el camino más corto entre
    un nodo inicial y un nodo objetivo.

    Args:
        graph (dict): Grafo que representa las conexiones entre ciudades.
        heuristic (dict): Diccionario con las estimaciones heurísticas.
        start (str): Nodo inicial.
        goal (str): Nodo objetivo.

    Returns:
        list: Camino más corto encontrado, o None si no hay solución.
    """
    # Cola de prioridad que considera costo acumulado y heurística
    frontier = PriorityQueue() 
    # Se agrega el nodo inicial
    frontier.put((0 + heuristic[start], start))
    # Traza el camino desde el nodo inicial
    came_from = {start: None}
    # Almacena el costo acumulado para cada nodo
    cost_so_far = {start: 0}
    
    while not frontier.empty():
        # Extrae el nodo con menor prioridad
        _, current = frontier.get()
        
        # Verifica si se alcanzó el nodo objetivo
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            # Reconstruye el camino en el orden correcto
            path.reverse()
            return path
        # Explora los vecinos del nodo actual
        for neighbor, cost in graph[current]:
            new_cost = cost_so_far[current] + cost
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic[neighbor]
                frontier.put((priority, neighbor))
                came_from[neighbor] = current
    # Retorna None si no se encuentra un camino al objetivo            
    return None

# Ejecución de pruebas con ambos algoritmos
print("Ruta con Greedy:", greedy_search(graph, heuristic, 'Arad', 'Bucharest'))
print("Ruta con A*:", a_star_search(graph, heuristic, 'Arad', 'Bucharest'))
