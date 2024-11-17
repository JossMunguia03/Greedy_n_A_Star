import copy 

from heapq import heappush, heappop

n = 3
row = [1, 0, -1, 0]
col = [0, -1, 0, 1]
    
class priorityQueue:

    # Inicializamos a con un constructor
    def __init__(self):
        self.heap = []

    # Insertamos una nueva 'k'
    def push(self, k):
        heappush(self.heap, k)

    # Definicimos una funcion para que el metodo remueva un elemento
    def pop(self):
        return heappop(self.heap)
    
    # Definimos una funcion para que el metodo reconozca
    # si hay un espacio vacio
    def empty(self):
        if not self.heap:
            return True
        else:
            return False 
              
# Para estruturar el Nodo
class node: 

    def __init__(self, parent, mat, empty_tile_pos, cost, level):

        # Guarda el nodo padre del nodo actual para que pueda
        # encontrar el camino para la respuesta
        self.parent = parent

        # Guarda la matriz
        self.mat = mat

        # Guarda la posicion del espacio vacio
        # existente en la matriz
        self.empty_tile_pos = empty_tile_pos

        # Guarda el numero de los espacios mal colocados
        self.cost = cost

        # Guarda el nuemro de movimientos hasta ahora
        self.level = level

    # Este metodo define que la prioridad sea formada
    # en el costo de las variables de los objetos
    def __lt__(self, nxt):
        return self.cost < nxt.cost

# Hacemos una funcion para calcular el numero de 
# espacios mal colocados, el numero de los espacios llenos
# que no esten en su meta
def calculateCost(mat, final) -> int:

    count = 0
    for i in range(n):
        for j in range(n):
            if ((mat[i][j]) and
                (mat[i][j] != final[i][j])):
                count += 1
    return count

def newNode(mat, empty_tile_pos, new_empty_tile_pos,
            level, parent, final) -> node:
    
    # Copia la informacion de la matriz padre a la matriz actual
    new_mat = copy.deepcopy(mat)

    # Movemos un espacio en 1 posicion
    x1 = empty_tile_pos[0]
    y1 = empty_tile_pos[1]
    x2 = new_empty_tile_pos[0]
    y2 = new_empty_tile_pos[1]
    new_mat[x1][y1], new_mat[x2][y2] = new_mat[x2][y2], new_mat[x1][y1]

    # Coloca el numero de espacios mal colocados
    cost = calculateCost(new_mat, final)

    new_node = node(parent, new_mat, new_empty_tile_pos, cost, level)
    return new_node

# Funcion para imprimir la matriz N x N
def printMatrix(mat):

    for i in range(n):
        for j in range(n):
            print("%d " % (mat[i][j]), end= " ")
        print()

# Funcion para verficiar si (x, y) es valido
def isSafe(x, y):
    return x >= 0 and x < n and y >= 0 and y < n

# Imprimimos el camino del nodo raiz hasta el destino
def printPath(root):

    if root == None:
        return
    printPath(root.parent)
    printMatrix(root.mat)
    print()

# Funcion para resolver algotimo N*N - 1 usando
# la posicion vacia y el estado inicial
def solve(initial, empty_tile_pos, final):

    # Crea una lista de prioridad para guardar nodos
    pq = priorityQueue()

    # Crea el nodo raiz
    cost = calculateCost(initial, final)
    root = node(None, initial, empty_tile_pos, cost, 0)

    # Añade la raiz a la lista de nodos
    pq.push(root)

    # Encuentra el nodo con el menor costo
    # añade la lista hijo a la lista de nodos y lo
    # borra de la lista
    
    while not pq.empty():

        # Encuentra el nodo con menor costo
        # estimado y lo borra de la lista de nodos
        minimum = pq.pop()

        # Si la respuesta es minima
        if minimum.cost == 0:

            # Imprime el camino de raiz al destino
            printPath(minimum)
            return
        
        # Genera todos los hijos posibles
        for i in range(4):
            new_tile_pos = [
                minimum.empty_tile_pos[0] + row[i],
                minimum.empty_tile_pos[1] + col[i],
            ]

            if isSafe(new_tile_pos[0], new_tile_pos[1]):

                # Crea un nodo hijo

                child = newNode(minimum.mat,
                                minimum.empty_tile_pos,
                                new_tile_pos,
                                minimum.level + 1,
                                minimum, final,)
                
                # añade un hijo a la lista de nodos
                pq.push(child)
# print("Please enter the numbers for the puzzle configuration:")
# num1 = int(input(" "))
# num2 = int(input("| "))
# num3 = int(input("| "))
# num4 = int(input(" "))
# num5 = int(input("| "))
# num6 = int(input("| "))
# num7 = int(input(" "))
# num8 = int(input("| "))
# num9 = int(input("| "))
print("Please enter the numbers for the puzzle configuration:")
row1 = input(": ").split('|')
row2 = input(": ").split('|')
row3 = input(": ").split('|')

# Configuracion inicial
# 0 Representa el espacio vacio
initial = [ [int(x.strip()) for x in row1],
    [int(x.strip()) for x in row2],
    [int(x.strip()) for x in row3]]

# print("The initial puzzle configuration is:")
# for row in initial:
#     print(" | ".join(map(str, row)))

# Resuelve la configuracion final
final = [ [1, 2, 3],
                [4, 5, 6],
                [7, 8, 0]]
# Coordina los espacios en blanco en
# la configuracion inicial
empty_tile_pos = [
    (i, j) for i in range(len(initial)) 
           for j in range(len(initial[i])) 
           if initial[i][j] == 0
][0]

# Llama a la funcion para resolver el problema
solve(initial, empty_tile_pos, final)