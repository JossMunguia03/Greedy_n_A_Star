import copy 
from heapq import heappush, heappop 
n = 3 
row = [1, 0, -1, 0] 
col = [0, -1, 0, 1] 

class priorityQueue: 
    def __init__(self): 
        self.heap = [] 

    def push(self, k): 
        heappush(self.heap, k) 

    def pop(self): 
        return heappop(self.heap) 
    
    def empty(self): 
        return len(self.heap) == 0 
    
class node: 
    def __init__(self, parent, mat, empty_tile_pos, cost, level): 
        self.parent = parent 
        self.mat = mat 
        self.empty_tile_pos = empty_tile_pos 
        self.cost = cost 
        self.level = level 

        def __lt__(self, nxt): 
            return (self.cost + self.level) < (nxt.cost + nxt.level) 
        
def calculateCost(mat, final) -> int: 

    goal_positions = {} 
    for i in range(n): 
        for j in range(n): 
            if final[i][j] != 0: goal_positions[final[i][j]] = (i, j) 
            cost = 0 

            for i in range(n): 
                for j in range(n): 
                    if mat[i][j] != 0: 
                        if mat[i][j] in goal_positions: goal_x, goal_y = goal_positions[mat[i][j]] 
                        cost += abs(i - goal_x) + abs(j - goal_y) 
                    else: 
                        raise ValueError(f"Value {mat[i][j]} not found in the final matrix.") 
                    return cost 
                
def newNode(mat, empty_tile_pos, new_empty_tile_pos, level, parent, final): 
    new_mat = copy.deepcopy(mat) 
    x1, y1 = empty_tile_pos 
    x2, y2 = new_empty_tile_pos 
    new_mat[x1][y1], new_mat[x2][y2] = new_mat[x2][y2], new_mat[x1][y1] 
    cost = calculateCost(new_mat, final) 
    return node(parent, new_mat, new_empty_tile_pos, cost, level) 
def printMatrix(mat): 

    for row in mat: 
        print(" ".join(str(x) for x in row)) 
        print() 

def isSafe(x, y): 
    return 0 <= x < n and 0 <= y < n 

def printPath(root): 
    if root is None: return printPath(root.parent) 
    printMatrix(root.mat) 
    
def solve(initial, empty_tile_pos, final): 
    pq = priorityQueue() 
    cost = calculateCost(initial, final) 
    root = node(None, initial, empty_tile_pos, cost, 0) 
    pq.push(root) 
    visited = set() 
    visited.add(tuple(tuple(row) for row in initial)) 

    while not pq.empty(): 
        minimum = pq.pop() 
        print(f"Step {minimum.level + 1} Level = {minimum.level}, Cost = {minimum.cost}, Total = {minimum.level + minimum.cost}") 
        printMatrix(minimum.mat) 
        if minimum.cost == 0: 
            
            return 
        
        for i in range(4): 
            new_tile_pos = [minimum.empty_tile_pos[0] + row[i], minimum.empty_tile_pos[1] + col[i]] 
            if isSafe(new_tile_pos[0], new_tile_pos[1]): 
                child = newNode(minimum.mat, minimum.empty_tile_pos, new_tile_pos, minimum.level + 1, minimum, final) 
                child_state = tuple(tuple(row) for row in child.mat) 
                if child_state not in visited: 
                    pq.push(child) 
                    visited.add(child_state) 

print("Please enter the numbers for the puzzle configuration:") 
row1 = input(": ").split('|') 
row2 = input(": ").split('|') 
row3 = input(": ").split('|') 
initial = [ [int(x.strip()) for x in row1], [int(x.strip()) for x in row2], [int(x.strip()) for x in row3] ] 
print("\nPlease enter the numbers for the final puzzle configuration:") 
row1_final = input(": ").split('|')
row2_final = input(": ").split('|') 
row3_final = input(": ").split('|') 
final = [ [int(x.strip()) for x in row1_final], [int(x.strip()) for x in row2_final], [int(x.strip()) for x in row3_final] ] 
empty_tile_pos = [(i, j) for i in range(len(initial)) for j in range(len(initial[i])) if initial[i][j] == 0][0] 
print("Initial configuration:")
printMatrix(initial) 
print("Final configuration:")
printMatrix(final) 
solve(initial, empty_tile_pos, final)