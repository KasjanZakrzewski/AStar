import math
import time

class Cell:
    def __init__(self, x, y):
        self.neighbours = []
        self.x = x
        self.y = y

    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)

class Wall(Cell):
    def __init__(self):
        super().__init__("w", "w")
        # self.neighbours = []
        self.char = "#"
        # self.x = "w"
        # self.y = "w"
    None

class Empty(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)
        # self.neighbours = []
        self.came = []
        self.char = "."
        # self.x = x
        # self.y = y
        self.f = 10000 #!!!!! do zmiany jak tablica będzie ogromna
        self.g = 10000
        self.h = 0
    
w = 10
h = 10

world = [[Empty(x,y) for x in range(h)] for y in range(w)] 

world[5][5] = Wall()
# world[5][4] = Wall()
world[5][2] = Wall()
world[5][3] = Wall()
world[4][5] = Wall()
# world[3][5] = Wall()
world[2][5] = Wall()
# world[3][5] = Wall()

world[6][5] = Wall()
world[7][5] = Wall()
world[8][5] = Wall()

def neighbours(h, w, world):
    for i in range(h):
        for j in range(w):
            pomI = i - 1
            pomJ = j - 1
            for k in range(3):
                for l in range(3):
                    if pomI >= 0 and pomI < h and pomJ >= 0 and pomJ < w:
                        if pomI != i or pomJ != j:
                            world[j][i].add_neighbour(world[pomJ][pomI])
                    pomI += 1
                pomI = i - 1
                pomJ += 1

def dist(cell, finish):
    x = abs(cell.x - finish.x)
    y = abs(cell.y - finish.y)

    h = (x*x + y*y)
    h = math.sqrt(h)

    return h

neighbours(h, w, world)

for row in world:
    for cell in row:
        print(cell.x, end="-")
        print(cell.y, end=" ")
    print("")

start = world[9][7]
finish = world[4][4]
finish.char = "F"

start.g = 0
start.f = dist(start, finish)
# print(start.f)

openSet = [start]
start.char = "o"

while openSet is not Empty:
    current = min(openSet, key=lambda x: (x.f, x.h))
    if current == finish:
        # End
        break

    openSet.remove(current)
    current.char = "c"

    for n in current.neighbours:
        if n.char == "#":
            continue

        temp = current.g + dist(current, n)
        if temp < n.g:
            n.came = current
            n.g = temp
            n.h = dist(n, finish)
            n.f = temp + n.h
            if n not in openSet:
                n.char = "o"
                openSet.append(n)

    for row in world:
        for cell in row:
            print(cell.char, end=" ")
        print("")
    print("===================")

    current.char = "x"
    time.sleep(0.5) 

finish.char = "F"
start.char = "S"
temp = finish.came

while temp != start:
    temp.char = "+"
    temp = temp.came

for row in world:
    for cell in row:
        print(cell.char, end=" ")
    print("")
print("===================")

# print("")
# print("")
    
# spr sąsiadów
# for row in world:
#     for cell in row:
#         for neighbour in cell.neighbours:
#             print(neighbour.x, end="-")
#             print(neighbour.y, end=" ")
#         print("")