import time

from pygame import *
from random import *

# from datetime import *
#

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
    'Outer': 'light blue',
}
shifter = [[1, 0], [0, -1], [-1, 0], [0, 1]]
shifter_cen = [[1, 0], [0, -1], [-1, 0], [0, 1], [0, 0]]
shifter_square = [[1, 0], [0, -1], [-1, 0], [0, 1], [1, 1], [1, -1], [-1, 1], [-1, -1]]


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
        self.energy = 15
        self.dust = 0
        self.weights = [randint(0, 20), randint(0, 20), randint(0, 20), randint(0, 20)]
        self.br_neighbours = 0

    def tick(self):
        if self.type == 'None':
            if randint(0, 100_000) == 0:
                self.type = 'Core'
                self.energy = 15
                self.color = type_to_color['Core']

        elif self.type == 'Core':
            if field_mana[self.x][self.y] > 0:
                self.energy += 1
                field_mana[self.x][self.y] -= 1
            if field_dust[self.x][self.y] > 0:
                self.dust += 1
                field_dust[self.x][self.y] -= 1
            if self.energy > 15:
                self.grow()
            if self.dust > 1:
                out = self.find_neighbor('Outer', 20, [])
                if out != None:
                    self.energy -= 2
                    out.energy += 2
                    out.dust += self.dust
                    self.dust = 0
            self.energy -= 1
            self.dust += 1

        elif self.type == 'Branch':
            core = self.find_neighbor('Core', 20, [])
            if core != None:
                if self.energy > 2:
                    core.energy += self.energy - 2
                    self.energy = 2
            else:
                self.energy -= 1
                self.dust += 1
            if self.br_neighbours > 6:
                self.die()
                for s in shifter_square:
                    try:
                        field[self.x + s[0]][self.y + s[1]].br_neighbours -= 1
                    except IndexError:
                        pass

        elif self.type == 'Mouth':
            for s in shifter_cen:
                try:
                    if field_mana[self.x + s[0]][self.y + s[1]] > 0:
                        self.energy += 1
                        field_mana[self.x + s[0]][self.y + s[1]] -= 1
                except IndexError:
                    pass
            core = self.find_neighbor('Core', 20, [])
            if core != None:
                core.energy += self.energy - 2
                self.energy = 2
            # else:
            self.energy -= 1
            self.dust += 1
            if field_mana[self.x][self.y] < field_dust[self.x][self.y]:
                self.die()

        elif self.type == 'Duster':
            for s in shifter_cen:
                try:
                    if field_dust[self.x + s[0]][self.y + s[1]] > 0:
                        self.energy += 1
                        field_dust[self.x + s[0]][self.y + s[1]] -= 1
                except IndexError:
                    pass
            core = self.find_neighbor('Core', 20, [])
            if core != None:
                core.energy += self.energy - 2
                self.energy = 2
            # else:
            self.energy -= 1

        elif self.type == 'Outer':
            if self.dust > 2:
                field_dust[self.x][self.y] += 2
                self.dust -= 2
                self.energy -= 1
            else:
                self.energy -= 2
                self.dust += 1

        if self.energy <= 0 or self.dust > 200:
            self.die()

    def die(self):
        self.type = 'None'
        field_dust[self.x][self.y] += self.dust
        self.energy = 0
        self.dust = 0
        self.color = type_to_color[self.type]

    def grow(self):
        poses = [self.find_neighbor('None', 20, [])]
        while poses[-1] != None:
            poses.append(self.find_all_neighbors('None', 50, [], poses))
        if len(poses) > 1:
            self.energy -= 7
            new = choice(poses[:-1])
            new.type = choice_weighted(['Branch', 'Mouth', 'Duster', 'Outer'], self.weights)
            new.color = type_to_color[new.type]
            new.energy = 7
            if new.type == 'Branch':
                for s in shifter_square:
                    try:
                        field[new.x + s[0]][new.y + s[1]].br_neighbours += 1
                    except IndexError:
                        pass

    def find_neighbor(self, type, depth, checked):
        if depth <= 0:
            return None
        checked.append(self)
        try:
            for s in shifter:
                who = field[(self.x + s[0]) % 100][(self.y + s[1]) % 100]
                if who.type == type:
                    return who
                elif who not in checked and who.type == 'Branch':
                    who2 = who.find_neighbor(type, depth - 1, checked)
                    if who2 != None:
                        return who2
        except IndexError:
            print('000ps')
        return None

    def find_all_neighbors(self, type, depth, checked, found):
        checked.append(self)
        if depth <= 0:
            return None
        try:
            for s in shifter:
                who = field[(self.x + s[0]) % 100][(self.y + s[1]) % 100]
                if who.type == type and who not in found:
                    return who
                elif who not in checked and who.type == 'Branch':
                    who2 = who.find_all_neighbors(type, depth - 1, checked, found)
                    if who2 != None:
                        return who2
        except IndexError:
            print('oops')
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
    direction -= (random() - 0.5) / 0.1
    direction %= 4
    for i in range(100):
        for j in range(100):
            if randint(0, 1000000) == 0:
                field_mana[i][j] = 5000
            dif = randint(0, field_mana[i][j] // 10)
            if field[(i + shifter[int(direction)][0]) % 100][(j + shifter[int(direction)][1]) % 100] < 500:
                field[(i + shifter[int(direction)][0]) % 100][(j + shifter[int(direction)][1]) % 100] += min(dif,
                                                                                                             field[i][
                                                                                                                 j])
                field[i][j] -= min(dif, field[i][j])


flag_a = 0
flag_b = 0
flag_c = 1
running = True
while running:
    for events in event.get():
        if events.type == QUIT:
            running = False
        if events.type == KEYDOWN:
            if events.key == K_1:
                flag_a = 1 - flag_a
            if events.key == K_2:
                flag_b = 1 - flag_b
            if events.key == K_3:
                flag_c = 1 - flag_c
    tick_field(field_mana, direction_mana)
    tick_field(field_dust, direction_dust)
    for i in range(len(field)):
        for j in range(len(field[i])):
            field[i][j].tick()
            c0 = abs(min(254 * 4, field_mana[i][j]) // 4) * flag_a
            c1 = abs(min(254, field_dust[i][j] * 4)) * flag_b

            c = (c0, c1, 0)
            draw.rect(screen, c, Rect(i * k, j * k, k, k))
            if field[i][j].type != 'None':
                if flag_c:
                    draw.rect(screen, field[i][j].color, Rect(i * k, j * k, k, k))
            # if field[i][j].type == 'Core':
            #     text_surface = font.render(str(field[i][j].energy), True, (255, 255, 255))
            #     screen.blit(text_surface, (i*k, j*k))

    for i in range(100):
        draw.line(screen, (100, 100, 100), (i * k, 0), (i * k, HEIGHT))
        draw.line(screen, (100, 100, 100), (0, i * k), (WIDTH, i * k))

    display.flip()
    clock.tick(60)

print(time.get_ticks() / 100)
quit()
exit()
