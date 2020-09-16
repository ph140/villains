import random
import time
import pygame

pygame.init()


# D I S P L A Y
grid_step = 20
display_width = 800
display_height = 480


class settings():
    def __init__(self):
        self.over = True
        self.tick_speed = 20
        self.counts = 0


class figur():
    def __init__(self, position, width, height):
        self.x = position[0]
        self.y = position[1]
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
                    cls.y -= grid_step

                if event.key == pygame.K_DOWN:
                    cls.y += grid_step

                if event.key == pygame.K_LEFT:
                    cls.x -= grid_step

                if event.key == pygame.K_RIGHT:
                    cls.x += grid_step
        cls.overstep()


def newfood():
    food.x = randomposition()[0]
    food.y = randomposition()[1]


def newvillain():
    villains.append(figur(randomposition(), grid_step, grid_step))


def text(txt_msg, txt_clr, txt_x, txt_y, txt_size,):
    font = pygame.font.SysFont('arial', txt_size)
    txt = font.render(txt_msg, True, txt_clr)
    gameDisplay.blit(txt, (txt_x, txt_y))


def randomposition():
    position = []
    position.append(random.randrange(0, display_width, grid_step))
    position.append(random.randrange(0, display_height, grid_step))
    return position


def randomcolor():
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))


# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)


# S P R I T E
food_pos = randomposition()
sprite_pos = randomposition()

# Adding sprite and food
sprite = figur(sprite_pos, grid_step, grid_step)
food = figur(food_pos, grid_step, grid_step)
game = settings()
villains = []


def startgame():
    game.over = False
    game.counts = 0
    game.tick_speed = 20
    sprite.score = 0
    villains.clear()
    newvillain()


startgame()
clock = pygame.time.Clock()


while True:
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    bg = pygame.image.load("stars.jpg")
    gameDisplay.blit(bg, (0, 0))

    pygame.draw.rect(gameDisplay, red, [
                     sprite.x, sprite.y, sprite.width, sprite.height])
    pygame.draw.rect(gameDisplay, randomcolor(), [
                     food.x, food.y, food.width, food.height])
    for i in villains:
        pygame.draw.rect(gameDisplay, blue, [i.x, i.y, i.width, i.height])

    # Makes the sprite move
    sprite.move()

    if sprite.caught(food) == True:
        # Checks if sprite caught food
        sprite.score += 1
        if sprite.score % 5 == 0 and sprite.score != 0:
            # Adds a new villain and increses the tick speed, everytime the
            # sprite catches 5 food
            newvillain()
            game.tick_speed += 4
        # Add a new food
        newfood()

    for i in range(len(villains)):
        if game.counts % 10 == 0:
            # Moves the villains and checks if they catches the sprite
            villains[i].attack(sprite)
        if villains[i].caught(sprite) == True:
            game.over = True

    game.counts += 1

    pygame.display.update()
    clock.tick(game.tick_speed)

    # G A M E  O V E R !
    while game.over:
        gameDisplay.fill(black)
        text('Game Over', white, 90, 60, 30)
        text('Du fikk '+str(sprite.score) + " poeng", white, 200, 200, 30)
        text("Trykk 'S' for å starte en ny runde", white, 340, 60, 15)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Press "s" to start again and "q" to quit
                if event.key == pygame.K_s:
                    startgame()
                if event.key == pygame.K_q:
                    pygame.quit()
        time.sleep(0.05)
