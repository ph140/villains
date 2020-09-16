import random
import time
import pygame

pygame.init()

q = 0
game_over = False
tick_speed = 20

# D I S P L A Y
display_width = 800
display_height = 480
grid_step = 20


# S P R I T E
sprite_start_x = 20
sprite_start_y = 20
food_start_x = 120
food_start_y = 120


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

    def caught(cls, target):
        if cls.x == target.x and cls.y == target.y:
            return True
        else:
            return False

    def attack(cls, target):
        if cls.x > target.x:
            xretning = random.randint(-1, 0)
        elif cls.x == target.x:
            xretning = 0
        else:
            xretning = random.randint(0, 1)

        if cls.y > target.y:
            yretning = random.randint(-1, 0)
        elif cls.y == target.y:
            yretning = 0
        else:
            yretning = random.randint(0, 1)

        cls.y += (grid_step * yretning)
        cls.x += (grid_step * xretning)
        cls.overstep()

    def move(cls):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    cls.y -= 20

                if event.key == pygame.K_DOWN:
                    cls.y += 20

                if event.key == pygame.K_LEFT:
                    cls.x -= 20

                if event.key == pygame.K_RIGHT:
                    cls.x += 20
        cls.overstep()


# Adding sprite and food
sprite = figur(sprite_start_x, sprite_start_y, grid_step, grid_step)
food = figur(food_start_x, food_start_y, grid_step, grid_step)
villains = []


# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)


clock = pygame.time.Clock()


def newfood():
    food.x = random.randrange(0, display_width-grid_step, grid_step)
    food.y = random.randrange(0, display_height-grid_step, grid_step)


def newvillain():
    villain_x = random.randrange(0, display_width-grid_step, grid_step)
    villain_y = random.randrange(0, display_height-grid_step, grid_step)
    villains.append(figur(villain_x+grid_step, villain_y+grid_step, 20, 20))


def text(txt_msg, txt_clr, txt_x, txt_y, txt_size,):
    font = pygame.font.SysFont('arial', txt_size)
    txt = font.render(txt_msg, True, txt_clr)
    gameDisplay.blit(txt, (txt_x, txt_y))


newvillain()
newfood()


while True:

    gameDisplay = pygame.display.set_mode((display_width, display_height))
    bg = pygame.image.load("stars.jpg")
    gameDisplay.blit(bg, (0, 0))
    # vill_img = pygame.image.load("alien.png")

    pygame.draw.rect(gameDisplay, red, [
                     sprite.x, sprite.y, sprite.width, sprite.height])
    pygame.draw.rect(gameDisplay, white, [
                     food.x, food.y, food.width, food.height])
    for i in villains:
        pygame.draw.rect(gameDisplay, blue, [i.x, i.y, i.width, i.height])
        # gameDisplay.blit(vill_img, [i.x, i.y, i.width, i.height])

    # event_listener()
    sprite.move()
    # sprite.overstep()

    # if food.x == sprite.x and food.y == sprite.y:
    if sprite.caught(food) == True:
        sprite.score += 1
        if sprite.score % 5 == 0 and sprite.score != 0:
            newvillain()
            tick_speed += 4
        newfood()

    for i in range(len(villains)):
        if q % 10 == 0:
            villains[i].attack(sprite)
            villains[i].overstep()
        if villains[i].caught(sprite) == True:
            game_over = True

    q += 1

    pygame.display.update()
    clock.tick(tick_speed)

    # G A M E  O V E R !
    while game_over:
        gameDisplay.fill(black)
        text('Game Over', white, 90, 60, 30)
        text('Du fikk '+str(sprite.score) + " poeng", white, 200, 200, 30)
        text("Trykk 'S' for å starte en ny runde", white, 340, 60, 15)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    sprite.score = 0
                    q = 0
                    tick_speed = 20
                    villains.clear()
                    newvillain()
                    game_over = False
                if event.key == pygame.K_q:
                    pygame.quit()
        time.sleep(0.05)
