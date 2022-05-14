import pygame
import random
import time


class Egg:
    def __init__(self, x, y, life, key_pressed, game):
        self.game = game
        self.key_now = key_pressed
        self.position = (x, y)
        self.current_life = life
        self.max_life = life
        self.images = self.image_choice()
        self.queue = False

    def image_choice(self):
        images = []

        if self.key_now == 274:
            images.append(self.game.head_bottom)

        elif self.key_now == 275:
            images.append(self.game.head_right)

        elif self.key_now == 276:
            images.append(self.game.head_left)

        elif self.key_now == 273:
            images.append(self.game.head_top)

        return images

    def image_body(self, key_after):
        k = {273: 0,
             274: 1,
             275: 2,
             276: 3
        }

        t = [[[self.game.vertical, self.game.queue_top], ['//'], [self.game.bottom_right, self.game.queue_right], [self.game.bottom_left, self.game.queue_left]],
             [['//'], [self.game.vertical, self.game.queue_bottom], [self.game.top_right, self.game.queue_right], [self.game.top_left, self.game.queue_left]],
             [[self.game.top_left, self.game.queue_top], [self.game.bottom_left, self.game.queue_bottom], [self.game.horizontal, self.game.queue_right], ['//']],
             [[self.game.top_right, self.game.queue_top], [self.game.bottom_right, self.game.queue_bottom], ['//'], [self.game.horizontal, self.game.queue_left]]]

        image = t[k[self.key_now]][k[key_after]]
        self.images += image

    def move(self):
        self.current_life -= 1


class Game:
    def __init__(self):
        self.life = 4
        self.x = 10
        self.y = 10
        self.snake = []
        self.snake_group = pygame.sprite.Group()
        self.pressed = {275: True}
        self.key_pressed = 275
        self.is_playing = False
        self.slow_base = 200
        self.slow = self.slow_base
        self.load_image()
        self.start = time.time()
        self.last = False
        self.position_food = self.generate_food()

    def update(self, screen):
        if self.slow > 0:
            self.slow -= 1
        else:
            if time.time()-self.start > 0.37:
                self.slow_base -= 20
            elif time.time()-self.start < 0.33:
                self.slow_base += 20
            self.start = time.time()
            self.movement()
            for element in self.snake:
                element.move()
            self.check_collision_wall()
            self.generate_egg(self.x, self.y, self.life)
            self.check_miam()

            for element in self.snake:
                if element.current_life == 0:
                    self.snake.remove(element)
                elif element.current_life == element.max_life-1:
                    element.image_body(self.key_pressed)
                    if element.images[1] == '//':
                        self.is_playing = False

            for element in self.snake[1:]:
                if element.position == (self.x, self.y):
                    self.last = True

            self.slow = self.slow_base

        if self.is_playing:
            screen.blit(self.pizza, self.position_food)
            for element in self.snake:
                if element.current_life == element.max_life:
                    screen.blit(element.images[0], (element.position[0], element.position[1]))
                elif element.current_life <= 1 or element.queue == True:
                    screen.blit(element.images[2], (element.position[0], element.position[1]))
                    element.queue = True
                else:
                    screen.blit(element.images[1], (element.position[0], element.position[1]))
            if self.last:
                time.sleep(0.3)
                self.is_playing = False

    def reset(self):
        self.life = 4
        self.x = 10
        self.y = 10
        self.snake = []
        self.position_food = self.generate_food()
        for element in self.pressed:
            self.pressed[element] = False
        self.pressed = {275: True}
        self.key_pressed = 275
        self.is_playing = True
        self.last = False

    def movement(self):
        for element in self.pressed.keys():
            if self.pressed[element]:
                if element == 274:
                    self.y += 20
                elif element == 275:
                    self.x += 20
                elif element == 276:
                    self.x -= 20
                elif element == 273:
                    self.y -= 20

    def generate_egg(self, x, y, life):
        egg = Egg(x, y, life,self.key_pressed, self)
        self.snake.insert(0,egg)

    def generate_food(self):
        food_good = False
        while not food_good:
            x_food = random.randint(0, 18)*20+10
            y_food = random.randint(0, 13)*20+10
            if len(self.snake) > 0:
                for element in self.snake:
                    if element.position == (x_food, y_food):
                        food_good = False
                        break
                    else:
                        food_good = True
            else:
                food_good = True
        self.food = True
        return (x_food, y_food)

    def check_miam(self):
        if self.position_food == self.snake[0].position:
            self.grow()
            self.position_food = self.generate_food()

    def load_image(self):
        self.head_top = pygame.image.load('files/head_top.png')
        self.head_bottom = pygame.image.load('files/head_bottom.png')
        self.head_left = pygame.image.load('files/head_left.png')
        self.head_right = pygame.image.load('files/head_right.png')

        self.queue_top = pygame.image.load('files/queue_top.png')
        self.queue_bottom = pygame.image.load('files/queue_bottom.png')
        self.queue_left = pygame.image.load('files/queue_left.png')
        self.queue_right = pygame.image.load('files/queue_right.png')

        self.horizontal = pygame.image.load('files/horizontal.png')
        self.vertical = pygame.image.load('files/vertical.png')

        self.top_left = pygame.image.load('files/top_left.png')
        self.top_right = pygame.image.load('files/top_right.png')
        self.bottom_left = pygame.image.load('files/bottom_left.png')
        self.bottom_right = pygame.image.load('files/bottom_right.png')

        self.pizza = pygame.image.load('files/pizza.png')

    def grow(self):
        self.life += 1
        for element in self.snake:
            element.current_life += 1
            element.max_life += 1

    def check_collision_wall(self):
        if self.x+10 > 390 or self.y+10 > 290 or self.x-10 < 0 or self.y - 10 < 0:
            self.is_playing = False


pygame.init()

clock = pygame.time.Clock()
FPS = 5

pygame.display.set_caption("Snake")
screen_size_x = 400
screen_size_y = 300
screen = pygame.display.set_mode((screen_size_x, screen_size_y))
background = pygame.image.load('files/background.png')

play_button = pygame.image.load('files/play_button.png')
play_button_rect = play_button.get_rect()
play_button_rect.x = 100
play_button_rect.y = 112
game = Game()
running = True

# boucle tant que running est vrai
while running:

    # appliquer l'arriere plan de notre jeu
    #pygame.draw.rect(screen, (40, 40, 40), [0, 0, screen_size_x, screen_size_y]) # Jouer avec la disposition de l'image
    screen.blit(background, (0, 0))
    if game.is_playing:
        game.update(screen)
    else:
        screen.blit(play_button, play_button_rect)
    pygame.display.flip()

    # si le joueur ferme la fenetre
    for event in pygame.event.get():
        # que l'evenement est fermeture de fenetre
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                for key in game.pressed.keys():
                    game.pressed[key] = False
                game.pressed[event.key] = True
                game.key_pressed = event.key

            if event.key == pygame.K_BACKSPACE:
                if not game.is_playing:
                    game.reset()
                    game.is_playing = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                # mettre le jeu en mode "lancé"
                if not game.is_playing:
                    game.reset()
                    game.is_playing = True

    # clock.tick(FPS)