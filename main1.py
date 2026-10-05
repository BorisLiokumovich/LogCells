import time

from pygame import *
from random import *

# from datetime import *
#

init()
k = 9
Y = 100
X = 200
WIDTH, HEIGHT = X * k, Y * k
# display.set_icon(transform.scale(image.load(""), (32, 32)))
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("LogCells1")
clock = time.Clock()
font = font.Font(None, 17)

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

def nearby_color(color, color_shift):
    return (color + (randint(0, 1) * 2 - 1) * randint(10, color_shift)) % 255


# genome
class Cell():
    def __init__(self, x, y, genome):
        self.x = x
        self.y = y
        self.genome = genome  # [1, (0, 0, 30), [1, 2, 3, 4, 5], [2, 3, 4, 5, 6], ...]
        self.color = self.genome[1]

        self.eat = self.genome[2][5]
        self.death_time = self.genome[2][6]
        self.energy_losing = self.genome[2][7]
        self.energy = 10
        self.dust = 0

        self.grown = False
        # жрать потреблять подыхать

    def tick(self):
        if self.genome[0] > -1:
            if self.energy > 16:  # and not self.grown:
                self.grown = True
                self.grow()

            if field_mana[self.x][self.y] > 0:
                self.energy += min(field_mana[self.x][self.y], self.eat)
                field_mana[self.x][self.y] -= min(field_mana[self.x][self.y], self.eat)
            if self.energy > 10:
                for s in shifter:
                    c = field[(self.x + s[0]) % X][(self.y + s[1]) % Y]
                    if c.color == self.color and c.energy < self.energy:
                        c.energy += self.energy // 5
                        self.energy -= self.energy // 5
            self.energy -= self.energy_losing
            self.dust += 1
            if self.energy <= 0 or self.dust > self.death_time * 20:
                self.die()

    def die(self):
        self.grown = False
        self.genome[0] = -1
        self.energy = 0
        # field_dust[self.x][self.y] = self.dust
        self.dust = 0
        self.color = (255, 255, 255)

    def grow(self):
        for i in range(len(shifter_cen)):
            cell = field[(self.x + shifter_cen[i][0]) % X][(self.y + shifter_cen[i][1]) % Y]
            new_gen = self.genome[2 + self.genome[0]][i]

            if new_gen < 0:
                cell.die()
                self.energy -= 4
            elif new_gen >= 10:
                continue
            elif cell.genome[0] == -1 or i == 4:
                cell.genome = self.genome[:]  # **
                if random() < 0.02 * (1 - debug1):  # мутация
                    cell.genome[2 + randint(0, 9)][randint(0, 4)] = randint(-5, 20)
                    color_shift = 20
                    cell.genome[1] = (nearby_color(self.color[0], color_shift),
                                      nearby_color(self.color[1], color_shift),
                                      nearby_color(self.color[2], color_shift))
                cell.genome[0] = new_gen
                cell.color = cell.genome[1]
                cell.eat = cell.genome[2 + cell.genome[0]][5]
                cell.death_time = cell.genome[2 + cell.genome[0]][6]
                cell.energy_losing = cell.genome[2 + cell.genome[0]][7]
                cell.dust = 0
                cell.energy = self.energy // 2
                self.energy //= 2


def create_genome():
    genome = [-1, (randint(0, 255), randint(0, 255), randint(0, 255))]
    for z in range(10):
        gen = []
        for z0 in range(8):
            gen.append(randint(-1, 20))
        genome.append(gen)
    return genome


debug1 = 0
field = []
for i in range(X):
    field.append([])
    for j in range(Y):
        genome = create_genome()
        if random() < 0.1 and not debug1:
            genome[0] = 0
        field[i].append(Cell(i, j, genome))

if debug1 or 1:
    field[X // 2][Y // 2].genome =[0, (42, 188, 78), [-2, 15, 10, 17, 15, 9, 19, 0], [0, 17, 14, 3, 5, 11, 10, 14], [-4, 2, 17, 0, 1, 19, 6, 3], [0, -5, 12, 13, 20, 20, 17, 6], [12, 11, 16, 6, -2, 2, 18, 9], [-3, 6, 18, -5, 5, 12, 11, 12], [20, 3, 3, -5, 2, 18, 17, 7], [5, -5, 18, -1, 16, 3, 14, 10], [7, 19, 0, 18, 20, 7, 5, 10], [-1, -1, 11, -1, -1, 19, 13, 7]]
field_mana = []
for i in range(X):
    field_mana.append([])
    for j in range(Y):
        field_mana[i].append(randint(100, 1000))

field_dust = []
for i in range(X):
    field_dust.append([])
    for j in range(Y):
        field_dust[i].append(0)

direction_mana = 2
direction_dust = 0


def tick_field(field, direction):
    direction -= (random() - 0.5) / 0.1
    direction %= 4
    for i in range(X):
        for j in range(Y):
            if randint(0, 10000) == 0:
                field_mana[i][j] = 5000
            dif = randint(0, field_mana[i][j] // 10)
            if field[(i + shifter[int(direction)][0]) % X][(j + shifter[int(direction)][1]) % Y] < 500:
                field[(i + shifter[int(direction)][0]) % X][(j + shifter[int(direction)][1]) % Y] += min(dif,
                                                                                                         field[i][
                                                                                                             j])
                field[i][j] -= min(dif, field[i][j])


flag_a = 0
flag_b = 0
flag_c = 1
update = 1
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
            if events.key == K_SPACE:
                update = 1 - update
        if events.type == MOUSEBUTTONDOWN:
            if events.button == 1:
                if field[events.pos[0] // k][events.pos[1] // k].genome[0]>-1:
                    print(field[events.pos[0] // k][events.pos[1] // k].genome)
            # event.button: 1 - левая, 2 - средняя (колесо), 3 - правая

    if update:
        tick_field(field_mana, direction_mana)
        # tick_field(field_dust, direction_dust)
        for i in range(len(field)):
            for j in range(len(field[i])):
                field[i][j].tick()
                c0 = abs(min(254 * 4, field_mana[i][j]) // 4) * flag_a
                c1 = abs(min(254, field_dust[i][j] * 4)) * flag_b
                c = (c0, c1, 0)
                draw.rect(screen, c, Rect(i * k, j * k, k, k))

                if flag_c and field[i][j].genome[0] > -1:
                    draw.rect(screen, field[i][j].color, Rect(i * k, j * k, k, k))
                    # text_surface = font.render(str(field[i][j].genome[0]), True, (200, 200, 200))
                    # screen.blit(text_surface, (i * k, j * k))

        # for i in range(max(X, Y)):
        #     draw.line(screen, (100, 100, 100), (i * k, 0), (i * k, HEIGHT))
        #     draw.line(screen, (100, 100, 100), (0, i * k), (WIDTH, i * k))

        display.flip()
        clock.tick(60)

# print(time. / 100)
quit()
exit()
