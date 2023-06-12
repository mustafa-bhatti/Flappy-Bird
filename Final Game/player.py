import pygame

class Player(pygame.sprite.Sprite):
    # bird class
    def __init__(self,group):
        super().__init__(group)
        # loads the images
        bird =  pygame.transform.scale(pygame.image.load("sprites/bird1.png").convert_alpha(),size=(64,64))
        bird2 =  pygame.transform.scale(pygame.image.load("sprites/bird2.png").convert_alpha(),size=(64,64))
        self.index  = 0
        self.frame  = [bird,bird2] # for animation
        self.image = self.frame[self.index]
        jump = bird
        self.bird_jump = pygame.transform.rotate(jump, angle= 20) # changes the angle if bird flys up
        self.rect = self.image.get_rect(midbottom = (100,200))
        self.gravity = 0 
        self.mask = pygame.mask.from_surface(self.image) # mask for collisions
    def jump(self):
        self.gravity = -7 # bird jumps
    def movement(self):
        # controls the movement of the bird
        self.gravity += 0.4 # bird is always moving downward
        self.rect.bottom += self.gravity  # updates the y value
        if self.rect.bottom > 400: # makes sure bird does not move out the frame
            self.rect.bottom = 400
        elif self.rect.bottom <= 20:
            self.rect.bottom = 20 
        
    def player_animation(self):

        if self.gravity < 0:
            self.image = self.bird_jump # displays jump image
        else:
            self.index += 0.14 
            # alternates between two pictures 
            if self.index >= 2:
                self.index = 0
            self.image = self.frame[int(self.index)]
    def update(self):
        self.movement()
        self.player_animation()
    def reset(self):
        # resets the position of the bird
        self.gravity = 0
        self.rect.midbottom=(100,200)
