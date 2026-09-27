from pygame import *
from random import *

init()
k = 9
WIDTH, HEIGHT = 100 * k, 100 * k
# display.set_icon(transform.scale(image.load(""), (32, 32)))
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("LogCells1")
clock = time.Clock()
font = font.Font(None, 10)

type_to_color = {
    'None': 'Black',
    'Core': 'Red',
    'Mouth': 'Yellow',
    'Branch': 'Dark green',
    'Duster': 'Blue',
}
shifter = [[1, 0], [0, -1], [-1, 0], [0, 1]]
shifter_cen = [[1, 0], [0, -1], [-1, 0], [0, 1],[0,0]]

def choice_weighted(poses, weights):
    r = randint(0, sum(weights))
    i = -1
    while r > 0:
        i += 1
        r -= weights[i]
    return poses[i]


class Cell():
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.color = type_to_color[type]
        self.energy = 10
        self.dust = 0
        self.weights = [randint(0, 20), randint(0, 20), randint(0, 20)]

    def tick(self):
        if self.type == 'None':
            if randint(0, 100_000) == 0:
                self.type = 'Core'
                self.energy = 10
                self.color = type_to_color['Core']

        elif self.type == 'Core':

            if field_mana[self.x][self.y] > 0:
                self.energy += 1
                field_mana[self.x][self.y] -= 1
            if field_dust[self.x][self.y] > 0:
                self.dust += 1
                field_dust[self.x][self.y] -= 1

            if self.energy > 8:
                self.grow()

        elif self.type == 'Branch':
            core = self.find_neighbor('Core', 200)
            if core != None:
                if self.energy > 2:
                    core.energy += self.energy - 2
                    self.energy = 2

            else:
                self.energy -= 1
                self.dust += 1

        elif self.type == 'Mouth':
            for s in shifter_cen:
                try:
                    if field_mana[self.x+s[0]][self.y+s[1]] > 0:
                        self.energy += 1
                        field_mana[self.x+s[0]][self.y+s[1]] -= 1
                except IndexError:
                    pass
            core = self.find_neighbor('Core', 200)
            if core != None:
                core.energy += self.energy - 2
                self.energy = 2
            else:
                self.energy -= 1
                self.dust += 1
            if field_mana[self.x][self.y] < field_dust[self.x][self.y] * 2:
                self.die()

        elif self.type == 'Duster':
            for s in shifter_cen:
                try:
                    if field_dust[self.x+s[0]][self.y+s[1]] > 0:
                        self.energy += 1
                        field_dust[self.x+s[0]][self.y+s[1]] -= 1
                except IndexError:
                    pass
            core = self.find_neighbor('Core', 200)
            if core != None:
                core.energy += self.energy - 2
                self.energy = 2
            else:
                self.energy -= 1

        if self.energy <= 0 or self.dust > 100:
            self.die()

    def die(self):
        self.type = 'None'
        field_dust[self.x][self.y] += self.dust
        self.energy = 0
        self.dust = 0
        self.color = type_to_color[self.type]

    def grow(self):
        poses = [self.find_neighbor('None', 100)]
        while poses[-1] != None:
            poses.append(self.find_all_neighbors('None', 100, poses))
        if len(poses) > 1:
            self.energy -= 7
            new = choice(poses[:-1])
            new.type = choice_weighted(['Branch', 'Mouth', 'Duster'], self.weights)
            new.color = type_to_color[new.type]
            new.energy = 7

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

    def find_all_neighbors(self, type, depth, found):
        if depth <= 0:
            return None
        try:
            for s in shifter:
                who = field[self.x + s[0]][self.y + s[1]]
                if who.type == type and who not in found:
                    return who
                elif who.type == 'Branch':
                    return who.find_all_neighbors(type, depth - 1, found)
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
        field_mana[i].append(randint(100, 1000))

field_dust = []
for i in range(100):
    field_dust.append([])
    for j in range(100):
        field_dust[i].append(0)

direction_mana = 2
direction_dust = 0


def tick_field(field, direction):
    direction -= (random() - 0.5) / 0.5
    direction %= 4
    for i in range(100):
        for j in range(100):
            try:
                dif = randint(0, 40)
                if field[i + shifter[int(direction)][0]][j + shifter[int(direction)][1]] < 500:
                    field[i + shifter[int(direction)][0]][j + shifter[int(direction)][1]] += min(dif, field[i][j])
                    field[i][j] -= min(dif, field[i][j])
            except IndexError:
                pass


running = True
while running:
    for events in event.get():
        if events.type == QUIT:
            running = False
    tick_field(field_mana, direction_mana)
    tick_field(field_dust, direction_dust)
    for i in range(len(field)):
        for j in range(len(field[i])):
            field[i][j].tick()
            c0 = abs(min(254, field_dust[i][j] * 2))
            c1 = 0  # abs(min(254 * 3, field_mana[i][j]) // 3)
            c = (c0, 0, c0)
            draw.rect(screen, c, Rect(i * k, j * k, k, k))
            if field[i][j].type != 'None':
                draw.rect(screen, field[i][j].color, Rect(i * k, j * k, k, k))
            # if field[i][j].type == 'Core':
            #     text_surface = font.render(str(field[i][j].energy), True, (255, 255, 255))
            #     screen.blit(text_surface, (i*k, j*k))

    for i in range(100):
        draw.line(screen, (100, 100, 100), (i * k, 0), (i * k, HEIGHT))
        draw.line(screen, (100, 100, 100), (0, i * k), (WIDTH, i * k))

    display.flip()
    clock.tick(60)

quit()
exit()
