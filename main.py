import numpy as np
import heapq

GERACOES = 250
# Create a binary matrix of 65x85
matriz_3d = np.zeros((65, 85,GERACOES), dtype=bool)

# Read the file and fill the binary matrix
with open('input.txt', 'r') as file:
    for i, line in enumerate(file):
        row = list(map(int, line.strip().split()))
        for j, value in enumerate(row):
            matriz_3d[i, j,0] = bool(value)

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

for i in range(GERACOES-2):
    matriz_3d[:, :, i + 1] = proxima_geracao(matriz_3d[:, :, i])

""" 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# Define the update function for the animation
def update(frame):
    im.set_array(matriz_3d[:, :, frame])
    return [im]

# Set up the plot
fig, ax = plt.subplots()
im = ax.imshow(matriz_3d[:, :, 0], cmap='Greens', animated=True)
ax.set_title("Cellular Automaton")

# Create the animation
ani = FuncAnimation(fig, update, frames=GERACOES, blit=True, interval=100)

# Display the animation
plt.show()
"""
print("environment")

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])

def neighbors(matrix, current):
    x, y, z = current
    for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        nx, ny, nz = x + dx, y + dy, z + 1
        if 0 <= nx < matrix.shape[0] and 0 <= ny < matrix.shape[1] and 0 <= nz < matrix.shape[2] and not matrix[nx, ny, nz]:
            yield (nx, ny, nz)

def a_star(matrix, start):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        _, current = heapq.heappop(frontier)
        if current[:2] == (64, 84):
            break

        for next_node in neighbors(matrix, current):
            new_cost = cost_so_far[current] + 1
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic((64, 84, current[2] + 1), next_node)
                heapq.heappush(frontier, (priority, next_node))
                came_from[next_node] = current

    if current[:2] != (64, 84):
        return None

    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def path_to_directions(path):

    directions = [''] * len(path)
    for i in range(len(path) - 1):
        dx, dy = path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1]
        if dx == 1:
            directions[i] = 'R'
        elif dx == -1:
            directions[i] = 'L'
        elif dy == 1:
            directions[i] = 'U'
        elif dy == -1:
            directions[i] = 'D'
    return directions

start = (0, 0, 0)
path = a_star(matriz_3d, start)

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors

def update_frame(frame, path, matrix):
    ax.clear()
    z = path[frame][2]
    layer = matrix[:, :, z].copy()
    cmap_layer = np.zeros_like(layer, dtype=np.int)
    cmap_layer[layer] = 1  # blocked cells are black
    for x, y, _ in path[:frame + 1]:
        cmap_layer[x, y] = 2  # path cells are green
    ax.imshow(cmap_layer, cmap=custom_cmap)
    ax.set_title(f"Step {frame}, z = {z}")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])

custom_cmap = colors.ListedColormap(["white","green", (0,0,0)])

if path:
    print("Path found:")
    print(path)
    directions = path_to_directions(path)
    print("Directions:")
    print(' '.join(str(elem) for elem in directions))

    fig, ax = plt.subplots()
    ani = animation.FuncAnimation(fig, update_frame, frames=len(path), fargs=(path, matriz_3d), interval=100)
    plt.show()
else:
    print("No path found")
