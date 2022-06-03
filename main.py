import math
import random, time
from tkinter import *
import pygame


def textBox():
    textBox = Tk()
    textBox.title("Input")
    textBox.geometry("150x100+600+300")#+875+400

    global values

    L1 = Label(textBox, text="Start Pos: ")
    L1.place(x=0, y=0)
    X1 = Label(textBox, text="x=")
    X1.place(x=55, y=0)
    x_start = StringVar()
    X_input_1 = Entry(textBox, width=3, textvariable=x_start)
    X_input_1.place(x=75, y=1)
    Y1 = Label(textBox, text="y=")
    Y1.place(x=105, y=0)
    y_start = StringVar()
    y_input_1 = Entry(textBox, width=3, textvariable=y_start)
    y_input_1.place(x=125, y=1)

    L2 = Label(textBox, text="End Pos: ")
    L2.place(x=0, y=20)
    X2 = Label(textBox, text="x=")
    X2.place(x=55, y=20)
    x_end = StringVar()
    x_input_2 = Entry(textBox, width=3, textvariable=x_end)
    x_input_2.place(x=75, y=21)
    Y2 = Label(textBox, text="y=")
    Y2.place(x=105, y=20)
    y_end = StringVar()
    y_input_2 = Entry(textBox, width=3, textvariable=y_end)
    y_input_2.place(x=125, y=21)

    visualize = IntVar()
    checkBox = Checkbutton(textBox, text="Visualize", variable=visualize)
    checkBox.place(x=35, y=40)

    def click_command():
        global values
        if x_start.get().isnumeric() == False or x_end.get().isnumeric() == False or y_start.get().isnumeric() == False or y_end.get().isnumeric() == False:
            print("Please input an integer")
        elif x_start.get() == x_end.get() and y_start.get() == y_end.get():
            print("Start and End position must be different")
        elif 0 <= int(x_start.get()) < cubes[0] and 0 <= int(y_start.get()) < cubes[1] and 0 <= int(x_end.get()) < \
                cubes[0] and 0 <= int(y_end.get()) < cubes[1]:
            textBox.destroy()
            values = [x_start.get(), y_start.get(), x_end.get(), y_end.get(), visualize.get()]
        else:
            print("Please input a value within range")

    click_me = Button(text="Start", command=click_command)
    click_me.place(x=60, y=65)

    click_me = Button(text="Config", command=click_command)
    click_me.place(x=5, y=65)

    textBox.mainloop()
    return values


def cost(n1,n2):
    return abs(n1.pos[0] - n2.pos[0]) + abs(n1.pos[1] - n2.pos[1])


def g(n):
    if n.parent is not None:
        return g(n.parent) + 1.414
    else:
        return 0


def calculate_f_cost(node, start, end, h_mode):
    # g_cost = abs(start[0] - node.pos[0]) + abs(start[1] - node.pos[1])
    g_cost = g(node)
    if h_mode == 'manhattan':
        h_cost = abs(node.pos[0] - end[0]) + abs(node.pos[1] - end[1])
    elif h_mode == 'diagonal':
        d_max = max((temp := node.pos[0] - end[0]), (temp2 := node.pos[1] - end[1]))
        d_min = min(temp, temp2)
        c_n = 6
        c_d = c_n * 1.414
        h_cost = c_d * d_min + c_n * (d_max - d_min)
    else:
        h_cost = math.sqrt(abs(node.pos[0] - end[0])**2 + abs(node.pos[1] - end[1])**2)
    node.g_cost = g_cost
    node.h_cost = h_cost
    print(node.pos, node.h_cost, node.g_cost)
    node.f_cost = g_cost + h_cost
    return node.f_cost


def calculate_path(node, initValues, cameFrom=None):
    dist = 0
    final = False
    parent = node
    tempParent = node.parent
    if cameFrom is not None: node.parent = cameFrom
    while not final:
        if parent.parent is not None:
            if parent.parent.pos[0] != int(initValues[0]) and parent.parent.pos[1] != int(initValues[1]):
                xDist = abs(parent.parent.pos[0] - parent.pos[0])
                yDist = abs(parent.parent.pos[1] - parent.pos[1])
                dist += xDist + yDist
                parent = parent.parent
            else:
                final = True
        else:
            final = True
        # print(parent.pos, parent.parent.pos)

    node.parent = tempParent
    return dist


class Grid:
    def __init__(self, cubes):
        self.cubes = cubes
        self.cubeWidth, self.cubeHeight = width // self.cubes[0], height // self.cubes[1]
        self.grid = [[Square([i, j], ((255, 255, 255))) for j in range(cubes[1])] for i in range(cubes[0])]

    def draw(self, win):
        for i in range(self.cubes[0]):
            for j in range(self.cubes[1]):
                pygame.draw.rect(win, (self.grid[i][j].col), (i * self.cubeWidth, j * self.cubeHeight,
                                                              (i + 1) * self.cubeWidth, (j + 1) * self.cubeHeight))


class Square:
    def __init__(self, pos, col):
        self.pos = pos
        self.col = col
        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = 0
        self.parent = None
        self.path = 0


def redrawWindow(grid,win):
    grid.draw(win)

    for i in range(grid.cubes[0] + 1):
        pygame.draw.line(win, (0, 0, 0), (i * grid.cubeWidth, 0), (i * grid.cubeWidth, height))
    for j in range(grid.cubes[1] + 1):
        pygame.draw.line(win, (0, 0, 0), (0, j * grid.cubeHeight), (width, j * grid.cubeHeight))

width, height = 600, 600
cubes = 50, 50

def main():
    global openList, closedList
    clock = pygame.time.Clock()
    grid = Grid(cubes)
    initValues = textBox()
    #initValues = [random.randint(1,25),random.randint(1,25),random.randint(26,48),random.randint(26,48),1]
    grid.grid[int(initValues[0])][int(initValues[1])].col = (0, 0, 255)
    grid.grid[int(initValues[2])][int(initValues[3])].col = (0, 0, 0)

    # initilize
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("A* Algorithm")

    redrawWindow(grid, win)
    pygame.display.update()

    hh = 0
    algo_loop_count = 0
    final_line = False
    run_algo = False
    run = True
    while run:
        clock.tick()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.mod == pygame.KMOD_NONE:
                    pass
                else:
                    if event.mod & pygame.KMOD_CTRL:
                        pass

        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]: return False
        if key[pygame.K_SPACE]: run_algo = True
        if key[pygame.K_r]: return True

        if pygame.mouse.get_pressed(3)[0]:
            mouseDown = True
        else:
            mouseDown = False

        if pygame.mouse.get_pos()[0] > width or pygame.mouse.get_pos()[0] < 0 or pygame.mouse.get_pos()[1] > height or \
                pygame.mouse.get_pos()[1] < 0:
            mouseDown = False
        if mouseDown and not run_algo:
            mouseX, mouseY = pygame.mouse.get_pos()
            X = mouseX // grid.cubeWidth
            Y = mouseY // grid.cubeHeight
            if X != int(initValues[0]) or Y != int(initValues[1]):
                if X != int(initValues[2]) or Y != int(initValues[3]):
                    grid.grid[X][Y].col = (128, 128, 128)

        if run_algo and algo_loop_count == 0:
            openList = [grid.grid[int(initValues[0])][int(initValues[1])]]
            calculate_f_cost(openList[0], (int(initValues[0]), int(initValues[1])),
                             (int(initValues[2]), int(initValues[3])), '')
            closedList = []
        if run_algo:
            algo_loop_count += 1
            if len(openList) == 0:
                print("No path found")
                return True
            smallest_f = [openList[0]]
            for node in openList:
                if (x := node.f_cost) < smallest_f[0].f_cost:
                    smallest_f = [node]
                elif x == smallest_f[0].f_cost:
                    smallest_f.append(node)
            if len(smallest_f) > 1:
                smallest_h = [smallest_f[0]]
                for node in smallest_f:
                    if node.g_cost < smallest_h[0].g_cost:
                        smallest_h = [node]
                    elif node.g_cost == smallest_h[0].g_cost:
                        smallest_h.append(node)
                if len(smallest_h) > 1:
                    current = random.choice(smallest_h)
                else:
                    current = smallest_h[0]
            else:
                current = smallest_f[0]

            openListCopy = openList
            openList = []
            for node in range(len(openListCopy)):
                if openListCopy[node] != current:
                    openList.append(openListCopy[node])
            closedList.append(current)

            if (current.pos[0] != int(initValues[2]) or current.pos[1] != int(initValues[3])):
                for neighbourValue in range(8):
                    neighbour = None
                    if neighbourValue == 0 and current.pos[0] > 0 and current.pos[1] < grid.cubes[1]-1:
                        neighbour = grid.grid[current.pos[0] - 1][current.pos[1] + 1]
                    elif neighbourValue == 1 and current.pos[1] < grid.cubes[1]-1:
                        neighbour = grid.grid[current.pos[0]][current.pos[1] + 1]
                    elif neighbourValue == 2 and current.pos[0] < grid.cubes[0]-1 and current.pos[1] < grid.cubes[1]-1:
                        neighbour = grid.grid[current.pos[0] + 1][current.pos[1] + 1]
                    elif neighbourValue == 3 and current.pos[0] > 0:
                        neighbour = grid.grid[current.pos[0] - 1][current.pos[1]]
                    elif neighbourValue == 4 and current.pos[0] < grid.cubes[0]-1:
                        neighbour = grid.grid[current.pos[0] + 1][current.pos[1]]
                    elif neighbourValue == 5 and current.pos[0] > 0 and current.pos[1] > 0:
                        neighbour = grid.grid[current.pos[0] - 1][current.pos[1] - 1]
                    elif neighbourValue == 6 and current.pos[1] > 0:
                        neighbour = grid.grid[current.pos[0]][current.pos[1] - 1]
                    elif current.pos[0] < grid.cubes[0]-1 and current.pos[1] > 0:
                        neighbour = grid.grid[current.pos[0] + 1][current.pos[1] - 1]
                    if neighbour is not None:
                        if neighbour not in closedList and neighbour.col != (128, 128, 128) and 0 <= neighbour.pos[0] < \
                                grid.cubes[0] and 0 <= neighbour.pos[1] < grid.cubes[1]:
                            #if (c := calculate_path(neighbour, initValues)) != neighbour.path: print(c,neighbour.path)
                            #print(calculate_path(neighbour, initValues), neighbour.path)
                            #if (g := calculate_path(neighbour, initValues, current)) < neighbour.path: print(g)
                            if neighbour not in openList or calculate_path(neighbour, initValues, current) < neighbour.path:
                                neighbour.f_cost = calculate_f_cost(neighbour, (int(initValues[0]), int(initValues[1])),
                                                                    (int(initValues[2]), int(initValues[3])),'')
                                neighbour.parent = current
                                if neighbour not in openList: openList.append(neighbour)
                                neighbour.path = calculate_path(neighbour,initValues)
                                if neighbour.h_cost > hh: hh = neighbour.h_cost
            else:
                run_algo = False
                final_line = True
            if int(initValues[4]) == 1:
                for open in openList:
                    open.col = (0, 255, 0)
                for closed in closedList:
                    closed.col = (255, 0, 0)
                grid.grid[int(initValues[0])][int(initValues[1])].col = (0, 0, 255)
                grid.grid[int(initValues[2])][int(initValues[3])].col = (0, 0, 0)
                time.sleep(.02)

            if final_line:
                parent = grid.grid[int(initValues[2])][int(initValues[3])]
                if parent.parent is not None:
                    count = 0
                    while final_line:
                        parent = parent.parent
                        parent.col = (0, 0, 255)
                        if parent.parent == grid.grid[int(initValues[0])][int(initValues[1])]: final_line = False
                        count += 1
                    print("Length:", count)
                    print(hh)

        redrawWindow(grid, win)
        pygame.display.update()
    pygame.quit()


reset = True
while reset: reset = main()

# https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
# https://www.youtube.com/watch?v=-L-WgKMFuhE
