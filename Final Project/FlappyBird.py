import random
import sys
import pygame
from pygame.locals import *

class FlappyBird:
    def __init__(self):
        pygame.init()
        self.CLOCK = pygame.time.Clock()
        self.FPS = 32
        self.WIDTH, self.HEIGHT =  289, 511
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        pygame_icon = pygame.image.load("sprites/bird.png")
        pygame.display.set_icon(pygame_icon)
        self.GROUND_Y = self.HEIGHT * 0.8
        self.GAME_SPRITES, self.GAME_SOUNDS = {}, {}
        self.PLAYER = "sprites/bird.png"
        self.BACKGROUND = "sprites/background.png"
        self.PIPE = "sprites/pipe.png"

    def load_images_and_sound(self):
        self.GAME_SPRITES["numbers"] = [
            pygame.image.load("sprites/0.png").convert_alpha(),
            pygame.image.load("sprites/1.png").convert_alpha(),
            pygame.image.load("sprites/2.png").convert_alpha(),
            pygame.image.load("sprites/3.png").convert_alpha(),
            pygame.image.load("sprites/4.png").convert_alpha(),
            pygame.image.load("sprites/5.png").convert_alpha(),
            pygame.image.load("sprites/6.png").convert_alpha(),
            pygame.image.load("sprites/7.png").convert_alpha(),
            pygame.image.load("sprites/8.png").convert_alpha(),
            pygame.image.load("sprites/9.png").convert_alpha(),
        ]
        self.GAME_SPRITES["message"] = pygame.image.load("sprites/message.png").convert_alpha()
        self.GAME_SPRITES["base"] = pygame.image.load("sprites/base.png").convert_alpha()
        self.GAME_SPRITES["pipe"] = [
            pygame.transform.rotate(pygame.image.load(self.PIPE).convert_alpha(), 180),
            pygame.image.load(self.PIPE).convert_alpha()
        ]
        self.GAME_SPRITES["background"] = pygame.image.load(self.BACKGROUND).convert()
        self.GAME_SPRITES["player"] = pygame.image.load(self.PLAYER).convert_alpha()
        self.GAME_SOUNDS["die"] = pygame.mixer.Sound("audio/die.wav")
        self.GAME_SOUNDS["hit"] = pygame.mixer.Sound("audio/hit.wav")
        self.GAME_SOUNDS["point"] = pygame.mixer.Sound("audio/point.wav")
        self.GAME_SOUNDS["swoosh"] = pygame.mixer.Sound("audio/swoosh.wav")
        self.GAME_SOUNDS["wing"] = pygame.mixer.Sound("audio/wing.wav")

    def welcome_screen(self):
        """
        Show welcome images on the screen
        """
        self.playerx = int(self.WIDTH/5)
        self.playery = int((self.HEIGHT - self.GAME_SPRITES["player"].get_height())/2)

        self.messagex = int((self.WIDTH - self.GAME_SPRITES["message"].get_width())/2)
        self.messagey = int((self.HEIGHT - self.GAME_SPRITES["message"].get_height())/2)

        self.base_x = 0

        while True:
            for event in pygame.event.get():
                # if user clicks on cross button close the game
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                # If the user presses space or up key, start the game for them
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    return

                else:
                    self.SCREEN.blit(self.GAME_SPRITES["background"], (0, 0))
                    self.SCREEN.blit(self.GAME_SPRITES["player"], (self.playerx, self.playery))
                    self.SCREEN.blit(self.GAME_SPRITES["message"], (self.messagex, self.messagey))
                    self.SCREEN.blit(self.GAME_SPRITES["base"], (self.base_x, self.GROUND_Y))
                    pygame.display.update()
                    self.CLOCK.tick(self.FPS)

    def main_game(self):
        self.score = 0
        self.playerx, self.playery = int(self.WIDTH/5), int(self.WIDTH/2)
        self.base_x = 0
        self.pipe_1 = self.random_pipe()
        self.pipe_2 = self.random_pipe()
        upper_pipe = [
            {"x" : self.WIDTH + 200, "y" : self.pipe_1[0]["y"]},
            {"x" : self.WIDTH + 200 + self.WIDTH/2, "y" : self.pipe_1[0]["y"]}
        ]
        lower_pipe = [
            {"x" : self.WIDTH + 200, "y" : self.pipe_2[1]["y"]},
            {"x" : self.WIDTH + 200 + self.WIDTH/2, "y" : self.pipe_2[1]["y"]}
        ]
        self.pipe_velX = -4
        self.player_vel_Y = -9
        self.player_max_vel_Y = 10
        self.player_min_vel_Y = -8
        self.player_acc_Y = 1
        self.player_flap_acc_v = -8
        self.player_flapped = False

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    if self.playery > 0:
                        self.player_vel_Y = self.player_flap_acc_v
                        self.player_flapped = True
                        self.GAME_SOUNDS['wing'].play()

            crashTest = self.isCollide(self.playerx, self.playery, upper_pipe, lower_pipe)
            if crashTest:
                return

            self.player_mid = self.playerx + self.GAME_SPRITES["player"].get_width()/2
            for pipe in upper_pipe:
                self.pipe_mid = pipe["x"] + self.GAME_SPRITES["pipe"][0].get_width()/2
                if self.pipe_mid <= self.player_mid < self.pipe_mid + 4:
                    self.score += 1
                    print(f"Your score is {self.score}")
                    self.GAME_SOUNDS["point"].play()

            if self.player_vel_Y < self.player_max_vel_Y and not self.player_flapped:
                self.player_vel_Y += self.player_acc_Y

            if self.player_flapped:
                self.player_flapped = False

            self.player_height = self.GAME_SPRITES["player"].get_height()
            self.playery = self.playery + min(self.player_vel_Y, self.GROUND_Y - self.playery - self.player_height)

            for upperPipe, lowerPipe in zip(upper_pipe, lower_pipe):
                upperPipe['x'] += self.pipe_velX
                lowerPipe['x'] += self.pipe_velX

            if 0 < upper_pipe[0]['x'] < 5:
                newpipe = self.random_pipe()
                upper_pipe.append(newpipe[0])
                lower_pipe.append(newpipe[1])

            if upper_pipe[0]['x'] < -self.GAME_SPRITES['pipe'][0].get_width():
                upper_pipe.pop(0)
                lower_pipe.pop(0)

            self.SCREEN.blit(self.GAME_SPRITES['background'], (0, 0))
            for upperPipe, lowerPipe in zip(upper_pipe, lower_pipe):
                self.SCREEN.blit(self.GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
                self.SCREEN.blit(self.GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

            self.SCREEN.blit(self.GAME_SPRITES['base'], (self.base_x, self.GROUND_Y))
            self.SCREEN.blit(self.GAME_SPRITES['player'], (self.playerx, self.playery))
            self.myDigits = [int(x) for x in list(str(self.score))]
            self.width = 0
            for digit in self.myDigits:
                self.width += self.GAME_SPRITES['numbers'][digit].get_width()
            self.gap = (self.WIDTH - self.width)/2

            for digit in self.myDigits:
                self.SCREEN.blit(self.GAME_SPRITES['numbers'][digit], (self.gap, self.HEIGHT*0.12))
                self.gap += self.GAME_SPRITES['numbers'][digit].get_width()
            pygame.display.update()
            self.CLOCK.tick(self.FPS)

    def isCollide(self, playerx, playery, upperPipes, lowerPipes):
        if playery > self.GROUND_Y-25 or playery < 0:
            self.GAME_SOUNDS["hit"].play()
            return True

        for pipe in upperPipes:
            self.pipeHeight = self.GAME_SPRITES['pipe'][0].get_height()
            if(playery < self.pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < self.GAME_SPRITES['pipe'][0].get_width()):
                self.GAME_SOUNDS['hit'].play()
                return True

        for pipe in lowerPipes:
            if (playery + self.GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < self.GAME_SPRITES['pipe'][0].get_width():
                self.GAME_SOUNDS['hit'].play()
                return True

        return False

    def random_pipe(self):
        self.pipe_height = self.GAME_SPRITES["pipe"][0].get_height()
        self.gap = int(self.HEIGHT/3)
        self.lower_y2 = self.gap + random.randrange(0, int(self.HEIGHT - self.GAME_SPRITES["base"].get_height() - 1.2 * self.gap))
        self.pipex = self.WIDTH + 10
        self.upper_y1 = self.HEIGHT + self.gap
        pipe = [
            {"x" : self.pipex, "y" : self.upper_y1},
            {"x" : self.pipex, "y" : self.lower_y2}
        ]
        return pipe

if __name__ == "__main__":
    game = FlappyBird()
    game.load_images_and_sound()

    while True:
        game.welcome_screen()
        game.main_game()
