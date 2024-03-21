import tkinter as tk
import math
import random as Randy

# Colors
# BACKGROUND = "#000000"
# EMPTY = "#FFFFFF"
# OPEN = "#FFFF00"
# CLOSE = "#00FFFF"
# START = "#00FF00"
# FINISH = "#00FF00"
# WALL = "#FF0000"
# CURRENT = "#0000FF"
# PATH = "#FF00FF"

# Colors V2
BACKGROUND = "#000000"
EMPTY = "#555555"#d3d3d3
OPEN = "#B5A8FF"
CLOSE = "#F3C7EF"
START = "#DBF5A4"
FINISH = "#DBF5A4"
WALL = "#9c99a9" #"#d3d3d3" #"#F5899F"
CURRENT = "#094AE0"
PATH = "#A8FFED"

# Paramiters
WIDTH = 1200
HEIGHT = 600
SPACE_SIZE = 10

COLUMNS = int(WIDTH/SPACE_SIZE)
ROWS = int(HEIGHT/SPACE_SIZE)

E = 2
WALL_PROCENT = 0.5
DYNAMIC = False

class Cell:
    def __init__(self, x, y):
        self.neighbours = []
        self.x = x
        self.y = y

    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)

class Wall(Cell):
    def __init__(self, x, y, canvas):
        super().__init__(x, y)
        # self.neighbours = []
        self.color = WALL
        # self.x = x
        # self.y = y

        self.rectangle = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=self.color)


class Empty(Cell):
    def __init__(self, x, y, canvas):
        super().__init__(x, y)
        # self.neighbours = []
        self.came = []
        self.color = EMPTY
        # self.x = x
        # self.y = y
        self.f = 100000 #!!!!! do zmiany jak tablica będzie ogromna
        self.g = 100000
        self.h = 0

        if DYNAMIC:
            self.n = 0

        self.rectangle = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=self.color)
        

# world = [[Empty(x*SPACE_SIZE,y*SPACE_SIZE, canvas) for x in range(COLUMNS)] for y in range(ROWS)] 

# world[1][1] = Wall(1*SPACE_SIZE,1*SPACE_SIZE)

def reset(h, w, world, start, finish):
    for j in range(h):
        for i in range(w):
            temp = world[j][i]
            temp.f = 100000
            temp.g = 100000
            temp.h = 0
            temp.came = []

            if type(temp) is Empty:
                temp.color = EMPTY
                canvas.itemconfig(temp.rectangle, fill=EMPTY)
            else:
                temp.color = WALL
                canvas.itemconfig(temp.rectangle, fill=WALL)

    start.color = START
    canvas.itemconfig(start.rectangle, fill=START)
    start.g = 0
    start.f = dist(start, finish)
    finish.color = FINISH
    canvas.itemconfig(finish.rectangle, fill=FINISH)

    openSet = [start]
    step(openSet, finish, start, None)

def neighbours(h, w, world):
    for j in range(h):
        for i in range(w):
            pomI = i - 1
            pomJ = j - 1

            for k in range(3):
                for l in range(3):
                    if pomI >= 0 and pomI < w and pomJ >= 0 and pomJ < h:
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

def trace(finish, start):
    canvas.itemconfig(finish.rectangle, fill=FINISH)
    canvas.itemconfig(start.rectangle, fill=START)
    temp = finish.came

    while temp != start:
        canvas.itemconfig(temp.rectangle, fill=PATH)
        temp = temp.came

def step(openSet, finish, start, current):
    if current != None:
        canvas.itemconfig(current.rectangle, fill=CLOSE)

    if len(openSet) != 0:
        current = min(openSet, key=lambda x: (x.f, x.h))
        if current == finish:
            # End
            trace(finish, start)
        else:
            openSet.remove(current)
            canvas.itemconfig(current.rectangle, fill=CURRENT)

            for n in current.neighbours:
                if type(n) is Wall:
                    continue
                temp = current.g + dist(current, n)
                if temp < n.g:
                    n.came = current
                    n.g = temp
                    
                    if DYNAMIC:
                        n.n = current.n + 1
                        d = dist(n, finish)
                        if d <= n.n:
                            n.h = (1+d/n.n)*dist(n, finish)
                        else:
                            n.h = 1*dist(n, finish)
                    else:
                        n.h = E*dist(n, finish)

                    n.f = temp + n.h

                    if n not in openSet:
                        canvas.itemconfig(n.rectangle, fill=OPEN)
                        openSet.append(n)

            root.after(50, step, openSet, finish, start, current)

    # canvas.update()
    # time.sleep(0.01) 
    # if current != finish:                
    #     root.after(500, step, openSet, finish, current)

def spawn(x, y, canvas, wall_procent):
    temp = int(100*wall_procent)
    if Randy.randint(0,100) <= temp:
        return Wall(x*SPACE_SIZE,y*SPACE_SIZE, canvas)
    else:
        return Empty(x*SPACE_SIZE,y*SPACE_SIZE, canvas)

def new_sim():
    None

root = tk.Tk() 

menu = tk.Menu(root)
action_menu = tk.Menu(menu, tearoff=0)
action_menu.add_command(label="Reset", command=lambda: reset(ROWS, COLUMNS, world, start, finish))
menu.add_cascade(menu=action_menu, label="Action")
root.config(menu=menu)

canvas = tk.Canvas(root, bg=BACKGROUND, height=HEIGHT, width=WIDTH) 
canvas.pack()


# world = [[Empty(x*SPACE_SIZE,y*SPACE_SIZE, canvas) for x in range(COLUMNS)] for y in range(ROWS)] 
world = [[spawn(x, y, canvas, WALL_PROCENT) for x in range(COLUMNS)] for y in range(ROWS)] 
canvas.update()

neighbours(ROWS, COLUMNS, world)

# canvas.itemconfig(world[7][7].rectangle, fill=START)

# start = world[9][7]
# finish = world[4][4]

start = world[Randy.randint(0,ROWS-1)][Randy.randint(0,COLUMNS-1)]
while type(start) is Wall:
    start = world[Randy.randint(0,ROWS-1)][Randy.randint(0,COLUMNS-1)]

finish = world[Randy.randint(0,ROWS-1)][Randy.randint(0,COLUMNS-1)]
while type(finish) is Wall:
    finish = world[Randy.randint(0,ROWS-1)][Randy.randint(0,COLUMNS-1)]




canvas.itemconfig(start.rectangle, fill=START)
start.g = 0
start.f = dist(start, finish)

canvas.itemconfig(finish.rectangle, fill=FINISH)

openSet = [start]

step(openSet, finish, start, None)
root.mainloop()





