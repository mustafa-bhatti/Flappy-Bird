import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self,group):
        super().__init__(group)
        bird =  pygame.transform.scale(pygame.image.load("sprites/bird1.png").convert_alpha(),size=(64,64))
        bird2 =  pygame.transform.scale(pygame.image.load("sprites/bird2.png").convert_alpha(),size=(64,64))
        self.index  = 0
        self.frame  = [bird,bird2]
        self.image = self.frame[self.index]
        jump = bird
        self.bird_jump = pygame.transform.rotate(jump, angle= 20)
        self.rect = self.image.get_rect(midbottom = (100,200))
        self.gravity = 0 
        self.flapped = False
        self.mask = pygame.mask.from_surface(self.image)
    def jump(self):
        self.gravity = -7
    def movement(self):

       #     """         for event in pygame.event.get():
        #    if event.type == pygame.KEYDOWN:
        #        if event.key == pygame.K_SPACE: """
        #self.gravity = -10
        #self.flapped = True
        #print(111)
        
        self.gravity += 0.4
        self.rect.bottom += self.gravity 

        if self.rect.bottom > 400:
            self.rect.bottom = 400
        elif self.rect.bottom <= 20:
            self.rect.bottom = 20 
        
    def player_animation(self):

        if self.gravity < 0:
            self.image = self.bird_jump
        else:
            self.index += 0.14
            if self.index >= 2:
                self.index = 0
            self.image = self.frame[int(self.index)]
    def update(self):
        #self.movement()
        self.movement()
        self.player_animation()
    def reset(self):
        self.gravity = 0
        self.rect.midbottom=(100,200)
