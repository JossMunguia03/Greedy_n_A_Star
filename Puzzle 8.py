from copy import deepcopy
import heapq

class Node:
    def __init__(self, data, level, fval):
        self.data = data  # Puzzle state as a 2D list
        self.level = level  # Level of the node in the tree
        self.fval = fval  # Heuristic value (f = g + h)

    def generate_child(self):
        x, y = self.find(self.data, '_')
        val_list = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        children = []
        for i in val_list:
            child = self.shuffle(self.data, x, y, i[0], i[1])
            if child is not None:
                child_node = Node(child, self.level + 1, 0)
                children.append(child_node)
        return children

    def shuffle(self, puz, x1, y1, x2, y2):
        if 0 <= x2 < len(puz) and 0 <= y2 < len(puz[0]):
            temp_puz = deepcopy(puz)
            temp_puz[x1][y1], temp_puz[x2][y2] = temp_puz[x2][y2], temp_puz[x1][y1]
            return temp_puz
        return None

    def find(self, puz, x):
        for i in range(len(puz)):
            for j in range(len(puz[i])):
                if puz[i][j] == x:
                    return i, j
        raise ValueError(f"Valor '{x}' no se encontro en el puzzle")

class Puzzle:
    def __init__(self, size):
        self.n = size
        self.open = []
        self.closed = []

    def accept(self):
        print(f"Inserte el estado del puzzle {self.n} filas, separadas por espacios (use '_' para el area en blanco):")
        puz = []
        for _ in range(self.n):
            row = input().split()
            if len(row) != self.n:
                raise ValueError("Invalid row length!")
            puz.append(row)
        return puz

    def f(self, start, goal):
        return self.h(start.data, goal) + start.level

    def h(self, start, goal):
        temp = 0
        for i in range(self.n):
            for j in range(self.n):
                if start[i][j] != goal[i][j] and start[i][j] != '_':
                    temp += 1
        return temp

    def process(self):
        print("Inserte el estado inicial de la matriz:")
        start = self.accept()
        print("Inserte el estado meta de la matriz:")
        goal = self.accept()

        start_node = Node(start, 0, 0)
        start_node.fval = self.f(start_node, goal)
        heapq.heappush(self.open, (start_node.fval, start_node))

        print("\nSolving...\n")
        while self.open:
            cur = heapq.heappop(self.open)[1]
            print("Estado actual (Level: {}):".format(cur.level))
            for row in cur.data:
                print(" ".join(row))
            print("\n")

            if self.h(cur.data, goal) == 0:
                print("Se ha llegado a la meta!")
                return

            self.closed.append(cur)
            for child in cur.generate_child():
                if child.data not in [node.data for _, node in self.open] and child.data not in [node.data for node in self.closed]:
                    child.fval = self.f(child, goal)
                    heapq.heappush(self.open, (child.fval, child))

        print("No se ha encontrado solucion!")


try:
    puz = Puzzle(3) 
    puz.process()
except Exception as e:
    print(f"Error: {e}")