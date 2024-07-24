import pygame
from sys import exit  # sys is built into python, exit terminates all running programs
from random import randint

# from enemies import get_fly


pygame.init()  # always call this first

screen_x = 800
screen_y = 400
screen = pygame.display.set_mode((screen_x, screen_y))  # tuple(width,height) of game window (display surface)
pygame.display.set_caption("PyGame_0")


# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player0_surf = pygame.image.load("Sprites/player0.png").convert_alpha()
        player1_surf = pygame.image.load("Sprites/player1.png").convert_alpha()
        player2_surf = pygame.image.load("Sprites/player2.png").convert_alpha()
        playerjump_surf = pygame.image.load("Sprites/playerjump.png").convert_alpha()

        self.player_walk = [player0_surf, player1_surf, player2_surf, player1_surf, playerjump_surf]
        self.player_index = 0

        self.image = self.player_walk[0]
        self.rect = self.image.get_rect(topleft=(100, 100))
        self.grav = 0

        self.jumpSound = pygame.mixer.Sound("Audio/jump.mp3")
        self.jumpSound.set_volume(0.2)

    def animState(self):
        if self.rect.bottom < 350:
            self.image = self.player_walk[-1]
        else:
            self.player_index = (self.player_index + 0.1) % (len(self.player_walk) - 1)
            self.image = self.player_walk[int(self.player_index)]

    def playerInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 350:
            self.grav = -20
            self.jumpSound.play()

    def applyGrav(self):
        self.grav += 1
        self.rect.bottom += self.grav
        if self.rect.bottom > 350:
            self.rect.bottom = 350

    def update(self):
        self.playerInput()
        self.applyGrav()
        self.animState()


playerGroup = pygame.sprite.GroupSingle(Player())


# Obstacle
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "fly":
            fly0_surf = pygame.image.load("Sprites/enemy20.png").convert_alpha()
            fly1_surf = pygame.image.load("Sprites/enemy21.png").convert_alpha()
            self.animFrames = [fly0_surf, fly1_surf]
            yPos = 200
        else:
            enemy10_surf = pygame.image.load("Sprites/enemy10.png").convert_alpha()
            enemy11_surf = pygame.image.load("Sprites/enemy11.png").convert_alpha()
            self.animFrames = [enemy10_surf, enemy11_surf]
            yPos = 300

        self.moveSpd = 5

        self.animIndex = 0
        self.image = self.animFrames[0]
        self.rect = self.image.get_rect(topleft=(screen_x + randint(100, 300), yPos))

    def animState(self):
        self.animIndex = (self.animIndex + 0.1) % len(self.animFrames)
        self.image = self.animFrames[int(self.animIndex)]

    def update(self):
        self.animState()
        self.rect.left -= self.moveSpd
        self.destroy()

    def destroy(self):
        if self.rect.right < 0:
            self.kill()


obstacleGroup = pygame.sprite.Group()


def display_score():
    score_temp = (pygame.time.get_ticks() - start_time) // 1000
    score_surf_temp = font.render(str(score_temp), False, (31, 31, 31))
    score_rect_temp = score_surf_temp.get_rect(center=(screen_x / 2, screen_y / 2))
    screen.blit(score_surf_temp, score_rect_temp)
    return score_temp


def spriteColl():
    if pygame.sprite.spritecollide(playerGroup.sprite, obstacleGroup, False):
        obstacleGroup.empty()
        return False
    else:
        return True


clock = pygame.time.Clock()  # Clock obj
font = pygame.font.Font(None, 50)
game_active = False
start_time = 0
score = 0

sky_surf = pygame.image.load(
    "Sprites/sky.jpg").convert()  # loads image, converts to something python works better with AKA better performance
ground_surf = pygame.image.load(
    "Sprites/ground.png").convert_alpha()  # deals with alpha values as well, AKA no visual artefacts

# Timer
obst_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obst_timer, 1000)

enemy1_anim_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy1_anim_timer, 300)
fly_anim_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_anim_timer, 300)

while True:  # makes window stay forever, otherwise it only stays for 1 frame
    for event in pygame.event.get():  # EVENT LOOP
        if event.type == pygame.QUIT:  # GAME EXIT CONDITION, pressed x button on window
            pygame.quit()  # un-inits, make sure to terminate program else error trying access display while not init
            exit()  # imported from sys, terminates program

        if game_active:
            if event.type == pygame.KEYDOWN:
                print("KEYDOWN")

            if (event.type == pygame.MOUSEBUTTONDOWN) and (playerGroup.sprite.rect.bottom >= 350):
                if playerGroup.sprite.rect.collidepoint(event.pos):
                    player_grav = -12

            if event.type == obst_timer:
                if not randint(0, 3):
                    obstacleGroup.add(Obstacle("fly"))
                else:
                    obstacleGroup.add(Obstacle("enemy1"))
                print()

        else:
            if event.type == pygame.KEYDOWN:
                playerGroup.sprite.rect.top = 0
                player_grav = 0
                game_active = True
                start_time = pygame.time.get_ticks()

    if game_active:
        screen.blit(sky_surf, (0, 0))  # Block Image Transfer, put 1 surface on another
        screen.blit(ground_surf, (0, 0))  # Block Image Transfer, put 1 surface on another

        playerGroup.update()
        playerGroup.draw(screen)

        obstacleGroup.update()
        obstacleGroup.draw(screen)

        score = display_score()

        game_active = spriteColl()

    else:
        screen.fill("#FFFF00")

        player_start = pygame.transform.scale(playerGroup.sprite.player_walk[-1], (300, 300))
        player_start_rect = player_start.get_rect(center=(screen_x / 2, screen_y / 2))
        screen.blit(player_start, player_start_rect)

        game_title = pygame.transform.scale2x(font.render("PyGame - 0", False, (63, 63, 63)))
        game_title_rect = game_title.get_rect(center=(screen_x / 2, 100))
        screen.blit(game_title, game_title_rect)

        game_instruc = pygame.transform.scale2x(font.render("Press any key to start", False, (63, 63, 63)))
        game_instruc_rect = game_instruc.get_rect(center=(screen_x / 2, 300))
        screen.blit(game_instruc, game_instruc_rect)

        if score > 0:
            score_surf = pygame.transform.scale2x(font.render("SCORE: " + str(score), False, (127, 127, 127)))
            score_rect = score_surf.get_rect(center=(screen_x / 2, screen_y / 2))
            screen.blit(score_surf, score_rect)

    # draw elements
    # update elements

    pygame.display.update()  # updates window, call at end
    clock.tick(60)  # makes sure loop runs once every 1/60 seconds
