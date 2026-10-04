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
        self.energy = 10
        self.dust = 0
        self.death_time = randint(50, 1000)

    def tick(self):
        if self.genome[0] > -1:
            if self.energy > 16:
                self.grow()

            if field_mana[self.x][self.y] > 0:
                self.energy += min(field_mana[self.x][self.y], 6)
                field_mana[self.x][self.y] -= min(field_mana[self.x][self.y], 6)
            self.energy -= 2
            self.dust += 1
            if self.energy <= 0 or self.dust > self.death_time:
                self.die()

    def die(self):
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
            if new_gen >= 10:
                continue
            if cell.genome[0] == -1 or i == 4:
                cell.genome = self.genome[:]  # **
                if random() < 0.02 * (1 - debug1):  # мутация
                    cell.genome[2 + randint(0, 9)][randint(0, 4)] = randint(-1, 20)
                    color_shift = 20
                    cell.genome[1] = (nearby_color(self.color[0], color_shift),
                                      nearby_color(self.color[1], color_shift),
                                      nearby_color(self.color[2], color_shift))
                cell.genome[0] = new_gen
                cell.color = cell.genome[1]

                cell.death_time = self.death_time
                cell.dust = 0
                cell.energy = self.energy // 2
                self.energy //= 2


def create_genome():
    genome = [0, (randint(0, 255), randint(0, 255), randint(0, 255))]
    for z in range(10):
        gen = []
        for z0 in range(5):
            gen.append(randint(-1, 20))
        genome.append(gen)
    return genome


debug1 = 0
field = []
for i in range(X):
    field.append([])
    for j in range(Y):
        if random() < 0.001 and not debug1:
            genome = create_genome()
        else:
            genome = [-1, (randint(0, 255), randint(0, 255), randint(0, 255))]

        field[i].append(Cell(i, j, genome))
if debug1 or 1:
    field[X // 2][Y // 2].genome = [0, (0, 255, 0), [1, 11, 1, 11, 0],[2, 11, 2, 11, 0],[3, 11, 3, 11, 0],[0, 0, 0, 0, 4],[11, 11, 11, 11, -1],[1, 11, 1, 11, 0],[1, 11, 1, 11, 0],[1, 11, 1, 11, 0],[1, 11, 1, 11, 0],[1, 11, 1, 11, 0]
                                    ]
    # field[3*X // 4][Y // 4].genome = [0, (221, 31, 0), [0,0,0,0,1],[11,11,11,11,11]]
    # [6, (151, 23, 82), [14, 8, -1, 6, 8], [10, 10, 20, 14, 18], [0, 0, 13, 8, 0], [5, 4, 2, 12, 12], [17, 15, 1, 5, 5],
    #  [12, 5, 16, 20, 3], [19, 8, 16, 18, 19], [2, 3, 9, 8, 0], [17, 8, 11, 17, 12], [11, 8, 12, 3, 10]]
    # [2, (91, 205, 4), [16, 1, 5, 1, -1], [20, 7, 4, 10, -1], [7, 17, 8, 20, 10], [9, 17, 5, 10, 2], [16, 19, 11, 2, 1],
    #  [10, 12, 15, 13, 8], [12, 18, 9, 17, 8], [20, 7, 19, 15, 10], [3, 15, 16, 5, 20], [12, 5, 2, 3, 13]]
    # [8, (91, 205, 4), [2, 9, 1, 9, -1], [5, 7, 4, 16, 15], [3, 17, 8, 9, 6], [9, 2, 5, 10, 12], [7, 3, 17, 2, 1],
    #  [3, 12, 15, 13, 8], [12, 10, 15, 17, 17], [20, 5, 17, 5, 13], [7, 10, 16, 5, 20], [8, 5, 1, 3, 13]]
    # [6, (71, 223, 240), [16, 9, 10, 15, 10], [5, 7, 15, 16, 15], [3, 13, 17, 3, 20], [9, 2, -1, 15, 17],
    #  [10, 3, 17, 2, 16], [10, 6, 15, 5, 9], [19, 10, 15, 17, 12], [10, 13, 17, 1, 13], [7, 10, 15, 16, 18],
    #  [0, 20, 1, 3, 19]]
    # [7, (99, 221, 223), [17, 10, 8, 11, 8], [1, 14, 7, 11, 1], [2, 7, 5, 2, 18], [10, 7, 17, 11, 13], [12, 1, 9, 17, 5],
    #  [8, 2, 12, 15, 4], [11, 6, 14, 10, 12], [5, 7, 5, 0, 10], [-1, 6, 14, 11, 5], [18, 0, 4, 17, 2]]
    # [3, (73, 26, 56), [7, 20, 11, 20, 20], [13, 3, 12, 4, 8], [10, 19, 9, 20, 7], [7, 17, 1, 11, 14], [0, 9, 8, 10, 6],
    #  [2, 5, 10, 4, 19], [20, 4, 9, 13, 19], [8, 20, 20, 14, 2], [15, 14, 17, 8, 15], [18, 20, 19, 17, 0]]
    # [4, (150, 147, 88), [20, 17, 11, 1, 8], [19, 14, -1, 12, -1], [19, 10, 5, 4, 5], [3, 10, 7, 6, 2],
    #  [14, 17, 4, 19, 15], [10, 7, -1, 16, 8], [11, 4, 15, 18, 20], [18, 4, 16, 6, 20], [9, 4, 4, 14, 2],
    #  [6, 10, 15, 19, 12]]
    # [8, (73, 26, 56), [7, 20, 19, 20, 20], [13, 0, 12, 4, 8], [10, 19, 9, 20, 7], [7, 17, 1, 11, 14], [0, 9, 8, 10, 6],
    #  [2, 5, 10, 4, 19], [20, 4, 9, 13, 19], [8, 20, 20, 14, 2], [15, 14, 17, 8, 15], [18, 20, 19, 17, 0]]
    # [9, (229, 234, 5), [10, 15, 3, 0, 7], [5, 15, 5, 4, 16], [14, 7, 11, 11, 4], [-1, 18, 12, 1, 12],
    #  [17, 14, 6, 6, 19], [12, 12, 18, 20, 16], [0, 1, 19, 12, 3], [15, 9, 1, 4, 1], [4, 9, 3, 19, 14],
    #  [12, 10, 9, 14, 16]]

    # [5, (163, 9, 207), [16, 8, 6, 3, 0], [-1, 20, 3, 4, 13], [12, 15, 11, 18, 1], [-1, 2, 20, 2, 2], [16, 15, 18, 9, 2], [4, 11, 19, 14, 20], [19, 17, 8, 3, 15], [11, 10, 3, 20, 16], [16, 15, 8, 13, 4], [7, 12, 12, 7, 15]]
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
