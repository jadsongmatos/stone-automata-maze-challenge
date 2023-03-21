import numpy as np
import heapq

# Create a binary matrix of 65x85
matriz_3d = np.zeros((65, 85,500), dtype=bool)

# Read the file and fill the binary matrix
with open('input.txt', 'r') as file:
    for i, line in enumerate(file):
        row = list(map(int, line.strip().split()))
        for j, value in enumerate(row):
            matriz_3d[i, j,0] = bool(value)

print(matriz_3d)

def contar_celulas_adjacentes(matriz, i, j):
    altura, largura = matriz.shape
    celulas_adjacentes = 0

    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue

            if 0 <= i + x < altura and 0 <= j + y < largura:
                celulas_adjacentes += matriz[i + x, j + y]

    return celulas_adjacentes

def proxima_geracao(matriz):
    altura, largura = matriz.shape
    nova_geracao = np.zeros((altura, largura), dtype=bool)

    for i in range(altura):
        for j in range(largura):
            celulas_adjacentes_verdes = contar_celulas_adjacentes(matriz, i, j)
            if not matriz[i, j]:
                if 1 < celulas_adjacentes_verdes < 5:
                    nova_geracao[i, j] = True
            else:
                if 3 < celulas_adjacentes_verdes < 6:
                    nova_geracao[i, j] = True

    return nova_geracao

geracoes = 498
index = 0

for _ in range(geracoes):
    matriz_3d[:, :, index + 1] = proxima_geracao(matriz_3d[:, :, index])


print("environment")

def heuristic(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2 + (b[2] - a[2]) ** 2)


def get_neighbors(environment, node):
    neighbors = []
    for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
        x, y, z = node[0] + dx, node[1] + dy, node[2] + dz
        if 0 <= x < environment.shape[0] and 0 <= y < environment.shape[1] and 0 <= z < environment.shape[2]:
            if not environment[x, y, z]:
                neighbors.append((x, y, z))
    return neighbors


def find_path(environment):
    start = (0, 0, 0)
    goal = (65, 85, environment.shape[2] - 1)

    if environment[start] or environment[goal]:
        return None  # No path if start or goal is an obstacle

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor in get_neighbors(environment, current):
            tentative_g_score = g_score[current] + heuristic(current, neighbor)
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # No path found

print(find_path(matriz_3d))