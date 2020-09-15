import random
import pygame
pygame.init()

q = 0
display_width = 800
display_height = 500
grid_step = 20
tick_speed = 20


class figur():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.score = 0

    def overstep(cls):
        if cls.x < 0:
            cls.x = display_width-grid_step
        if cls.x == display_width:
            cls.x = 0
        if cls.y < 0:
            cls.y = display_height-grid_step
        if cls.y == display_height:
            cls.y = 0

    def caught(cls, villain):
        if cls.x == villain.x and cls.y == villain.y:
            return True
        else:
            return False

    def move(cls, sprite):
        if cls.x > sprite.x:
            if random.randint(1, 6) > 5:
                xretning = random.randint(0, 1)
            else:
                xretning = -1
        else:
            if random.randint(1, 6) > 5:
                xretning = random.randint(-1, 0)
            else:
                xretning = 1

        if cls.y > sprite.y:
            if random.randint(1, 6) > 5:
                yretning = random.randint(0, 1)
            else:
                yretning = -1
        else:
            if random.randint(1, 6) > 5:
                yretning = random.randint(-1, 0)
            else:
                yretning = 1

        cls.y += (grid_step * yretning)
        cls.x += (grid_step * xretning)


sprite = figur(100, 100, 20, 20)
food = figur(random_x, random_y, 20, 20)
villains = []


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)


clock = pygame.time.Clock()


def newfood():
    food.x = random.randrange(0, display_width-grid_step, grid_step)
    food.y = random.randrange(0, display_height-grid_step, grid_step)


def newvillain():
    villains.append(figur(random_x+grid_step, random_y+grid_step, 20, 20))


def text(txt_msg, txt_clr, txt_x, txt_y, txt_size,):
    font = pygame.font.SysFont('arial', txt_size)
    txt = font.render(txt_msg, True, txt_clr)
    gameDisplay.blit(txt, (txt_x, txt_y))


main = True
newvillain()

while main == True:
    game_over = False

    gameDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.draw.rect(gameDisplay, red, [
                     sprite.x, sprite.y, sprite.width, sprite.height])
    pygame.draw.rect(gameDisplay, white, [
                     food.x, food.y, food.width, food.height])
    for i in villains:
        pygame.draw.rect(gameDisplay, blue, [i.x, i.y, i.width, i.height])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main = False

        'CONTROLS'
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                sprite.y -= 20

            if event.key == pygame.K_DOWN:
                sprite.y += 20

            if event.key == pygame.K_LEFT:
                sprite.x -= 20

            if event.key == pygame.K_RIGHT:
                sprite.x += 20
    if food.x == sprite.x and food.y == sprite.y:
        sprite.score += 1
        if sprite.score % 5 == 0 and sprite.score != 0:
            newvillain()
            tick_speed += 5
        newfood()

    p = 0
    for i in villains:
        if q % 10 == 0:
            villains[p].move(sprite)
            villains[p].overstep()
        if sprite.caught(villains[p]) == True:
            game_over = True
        p += 1
    sprite.overstep()
    q += 1

    # G A M E  O V E R !
    while game_over:
        gameDisplay.fill(black)
        text('Game Over', white, 90, 60, 30)
        text('Du fikk '+str(sprite.score) + " poeng", white, 200, 200, 30)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    sprite.score = 0
                    q = 0
                    villains.clear()
                    for i in range(2):
                        newvillain()
                    tick_speed = 20
                    game_over = False

    pygame.display.update()
    clock.tick(tick_speed)
