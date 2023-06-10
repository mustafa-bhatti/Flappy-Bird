import pygame
from random import randint
from sys import exit
from player import Player

## class
class Pipe(pygame.sprite.Sprite):
    def __init__(self,group,x,y,type):
        super().__init__(group)
        self.gap = 60
        pipe = pygame.image.load("sprites/pipe.png").convert_alpha()
        pipe_inverted = pygame.transform.rotate(pipe, angle = 180)
        
        if type == 1:
            self.image = pipe
            self.rect = self.image.get_rect(topleft= (x,y + self.gap))
        else:
            self.image = pipe_inverted
            self.rect = self.image.get_rect(bottomleft= (x,y - self.gap))
    def update(self):
        self.rect.x -= 4
        if self.rect.right < 0:
            self.kill()

class Game:

    
    # surfaces
    def __init__(self):
        pygame.init()
        self.scroll = -100
        self.speed = 4
        self.width = 800
        self.height = 400
        self.screen = pygame.display.set_mode((800,400))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        pygame_icon = pygame.image.load("sprites/bird.png")
        pygame.display.set_icon(pygame_icon)
        self.test_font = pygame.font.Font("font/Pixeltype.ttf",49)
        self.game_active = False
        sky = pygame.image.load("sprites/background.png").convert_alpha()
        self.sky = pygame.transform.scale(sky, size = (self.width,self.height))

        base = pygame.image.load("sprites/base.png").convert_alpha()
        self.base = pygame.transform.scale(base, size = (self.width+100,self.height/4))
        self.player_sprite = pygame.sprite.Group()
        self.player = Player(self.player_sprite)
        self.score = 0
        self.pipe_sprites = pygame.sprite.Group()
        self.pipe_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.pipe_timer,1400)
        ## player and obstacles objects
    def pipe_generate(self):
        pipe_gap = randint(-90, 70)
        self.upper_pipe=Pipe(self.pipe_sprites, 900, 200 + pipe_gap, 1)
        self.lower_pipe = Pipe(self.pipe_sprites, 900, 200 + pipe_gap, 0)
        
    def collision(self):
        if pygame.sprite.groupcollide(self.player_sprite, self.pipe_sprites, False, False):
            self.pipe_sprites.empty()
            self.player_sprite.empty()
            return False
            self.reset()
        elif self.player.rect.top <= 0 or self.player.rect.bottom >=360:
            return False
            self.reset()
        else :
            return True
        self.player = Player(self.player_sprite)
        print(self.player.gravity)
    
    def main(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and  event.key == pygame.K_SPACE:
                    if self.game_active == False:
                        self.game_active = True
                        self.score = 0
                    else:
                        self.player.jump()
                if self.game_active:
                    if event.type == self.pipe_timer:
                        self.pipe_generate()
                        print(1)


            self.screen.blit(self.sky,(0,0))
            

            if self.game_active:
                self.scroll -= self.speed
                if self.scroll <= -100:
                    self.scroll = -30
                
                self.player_sprite.draw(self.screen)
                self.player_sprite.update()
                self.pipe_sprites.draw(self.screen)
                self.pipe_sprites.update()
                self.game_active = self.collision()
            else:
                pass
            self.screen.blit(self.base,(self.scroll,360))
            pygame.display.update()
            self.clock.tick(45)
bg = pygame.Surface((800,400))
game = Game()
try:

    game.main()
except Exception as e:
    print(e)
    raise
    pygame.quit()
    exit()
