from pygame import *
from random import *

init()
k = 9
WIDTH, HEIGHT = 100 * k, 100 * k
# display.set_icon(transform.scale(image.load(""), (32, 32)))
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("LogCells1")
clock = time.Clock()

type_to_color = {
    'None': 'Black',
    'Core': 'Red',
    'Mouth': 'Yellow',
    'Branch': 'Dark green',
}
shifter = [[1, 0], [0, -1], [-1, 0], [0, 1]]


class Cell():
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.color = type_to_color[type]
        self.energy = 10

    def tick(self):
        if self.type == 'None':
            if randint(0,100_000)==0:
                self.type = 'Core'
                self.energy = 10
                self.color = type_to_color['Core']
        elif self.type == 'Core':
            if field_mana[self.x][self.y] > 0:
                self.energy += 1
                field_mana[self.x][self.y] -= 1
            else:
                self.energy -= 1

            if self.energy > 15:
                self.grow()

        elif self.type == 'Branch':
            core = self.find_neighbor('Core', 100)
            if core != None:
                if self.energy > 1:
                    self.energy -= 1
                    core.energy += 1
            else:
                self.die()

        elif self.type == 'Mouth':
            pass

        if self.energy <= 0:
            self.die()

    def die(self):
        self.type = 'None'
        self.energy = 0
        self.color = type_to_color[self.type]

    def grow(self):
        poses = []
        try:
            for s in shifter:
                if field[self.x + s[0]][self.y + s[1]].type == 'None':
                    poses.append(field[self.x + s[0]][self.y + s[1]])
        except IndexError:
            pass
        if poses:
            self.energy -= 7
            new = choice(poses)
            new.type = 'Branch' #choice с вариациями
            new.color = type_to_color[new.type]
            new.energy = 5

    def find_neighbor(self, type, depth):
        if depth <= 0:
            return None
        try:
            for s in shifter:
                who = field[self.x + s[0]][self.y + s[1]]
                if who.type == type:
                    return who
                elif who.type == 'Branch':
                    return who.find_neighbor(type, depth - 1)
        except IndexError:
            pass
        return None




field = []
for i in range(100):
    field.append([])
    for j in range(100):
        field[i].append(Cell(i, j, 'None' if randint(0, 100) != 0 else 'Core'))

field_mana = []
for i in range(100):
    field_mana.append([])
    for j in range(100):
        field_mana[i].append(randint(0, 100))

# def tick_mana():
#     global field_mana


running = True
while running:
    for events in event.get():
        if events.type == QUIT:
            running = False
    for i in range(len(field)):
        for j in range(len(field[i])):
            field[i][j].tick()
            c = field[i][j].color
            draw.rect(screen, c, Rect(i * k, j * k, k, k))
    for i in range(100):
        draw.line(screen, (100, 100, 100), (i * k, 0), (i * k, HEIGHT))
        draw.line(screen, (100, 100, 100), (0, i * k), (WIDTH, i * k))

    display.flip()
    clock.tick(10)

quit()
exit()
