from pygame import *
from random import *

init()
k = 9
WIDTH, HEIGHT = 100 * k, 100 * k
# display.set_icon(transform.scale(image.load(""), (32, 32)))
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("LogCells1")
clock = time.Clock()


class Cell():
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

        pass


field = []
for i in range(100):
    field.append([])
    for j in range(100):
        field[i].append(Cell(i, j, randint(0, 1)))

running = True
while running:
    for events in event.get():
        if events.type == QUIT:
            running = False
    for i in range(len(field)):
        for j in range(len(field[i])):
            c = field[i][j].type * 255
            draw.rect(screen, (c, c, c), Rect(i * k, j * k, k, k))
    for i in range(100):
        draw.line(screen, (150, 150, 150), (i * k, 0), (i * k, HEIGHT))
        draw.line(screen, (150, 150, 150), (0, i * k), (WIDTH, i * k))
    # square = pygame.Rect(x, y, side, side)
    # pygame.draw.rect(screen, color, square)
    # pygame.

    display.flip()
    clock.tick(60)

quit()
exit()
