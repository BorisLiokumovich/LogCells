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
font = font.Font(None, 18)

shifter = [[1, 0], [0, -1], [-1, 0], [0, 1]]
shifter_cen = [[1, 0], [0, -1], [-1, 0], [0, 1], [0, 0]]
shifter_square = [[1, 0], [0, -1], [-1, 0], [0, 1], [1, 1], [1, -1], [-1, 1], [-1, -1]]


# def choice_weighted(poses, weights):
#     r = randint(0, sum(weights))
#     i = -1
#     while r > 0:
#         i += 1
#         r -= weights[i]
#     return poses[i]
# def constrain(val,min,max):
#     return max(min(val,max),min)

# genome
class Cell():
    def __init__(self, x, y, genome):
        self.x = x
        self.y = y
        self.genome = genome  # [1, (0, 0, 30), [1, 2, 3, 4, 5], [2, 3, 4, 5, 6], ...]
        self.color = self.genome[1]
        self.energy = 10
        self.dust = 0
        self.death_time = randint(50, 1200)

    def tick(self):
        if self.genome[0] != -1:
            if self.energy > 16:
                self.grow()

            if field_mana[self.x][self.y] > 0:
                self.energy += min(field_mana[self.x][self.y], 5)
                field_mana[self.x][self.y] -= min(field_mana[self.x][self.y], 5)
            self.energy -= 1
            self.dust += 1
            if self.energy <= 0 or self.dust > self.death_time:
                self.die()

    def die(self):
        self.genome[0] = -1
        self.energy = 0
        self.dust = 0
        self.color = (0, 0, 0)

    def grow(self):
        for i in range(len(shifter)):
            cell = field[(self.x + shifter_cen[i][0]) % 100][(self.y + shifter_cen[i][1]) % 100]
            try:
                new_gen = self.genome[2 + self.genome[0]][i]
            except IndexError:
                print(self.genome)

            if new_gen == -1:
                cell.die()
                self.energy -= 4
            if new_gen >= 10:
                continue
            if cell.genome[0] < 0:
                cell.genome = self.genome  # **
                if random() < 0.001:  # мутация
                    cell.genome[2 + randint(0, 9)][randint(0, 4)] = randint(0, 20)
                    color_shift = 20
                    cell.genome[1] = ((self.color[0] + randint(-color_shift, color_shift)) % 255,
                                      (self.color[1] + randint(-color_shift, color_shift)) % 255,
                                      (self.color[2] + randint(-color_shift, color_shift)) % 255)
                cell.genome[0] = new_gen
                cell.color = cell.genome[1]
                cell.dust = 0
                cell.energy = 4
                self.energy -= 4


def create_genome():
    genome = [0, (randint(0, 255), randint(0, 255), randint(0, 255))]
    for z in range(10):
        gen = []
        for z0 in range(5):
            gen.append(randint(0, 20))
        genome.append(gen)
    print(genome)
    return genome


field = []
for i in range(100):
    field.append([])
    for j in range(100):
        if random() < 0.1:
            genome = create_genome()
        else:
            genome = [-1, (randint(0, 255), randint(0, 255), randint(0, 255))]

        field[i].append(Cell(i, j, genome))

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
            if randint(0, 10000) == 0:
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
    # tick_field(field_dust, direction_dust)
    for i in range(len(field)):
        for j in range(len(field[i])):
            field[i][j].tick()
            c0 = abs(min(254 * 4, field_mana[i][j]) // 4) * flag_a
            c1 = abs(min(254, field_dust[i][j] * 4)) * flag_b

            c = (c0, c1, 0)
            draw.rect(screen, c, Rect(i * k, j * k, k, k))

            if flag_c and field[i][j].genome[0] != -1:
                draw.rect(screen, field[i][j].color, Rect(i * k, j * k, k, k))
            text_surface = font.render(str(field[i][j].genome[0]), True, (200, 200, 200))
            screen.blit(text_surface, (i * k, j * k))

    for i in range(100):
        draw.line(screen, (100, 100, 100), (i * k, 0), (i * k, HEIGHT))
        draw.line(screen, (100, 100, 100), (0, i * k), (WIDTH, i * k))

    display.flip()
    clock.tick(60)

# print(time. / 100)
quit()
exit()
