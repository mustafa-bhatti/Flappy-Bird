import pygame
class Pipe(pygame.sprite.Sprite):
    # class for pipes
    def __init__(self,group,x,y,type):
        super().__init__(group)
        self.gap = 59 # gap between the pipes
        self.speed = 5 
        # loads the image
        pipe = pygame.image.load("sprites/pipe.png").convert_alpha()
        pipe_inverted = pygame.transform.rotate(pipe, angle = 180)
        
        if type == 1:
            # generates two types of pipe (inverted) 
            #type is mentioned in pipe_generate method
            self.image = pipe
            self.rect = self.image.get_rect(topleft= (x,y + self.gap))
        else:
            self.image = pipe_inverted
            self.rect = self.image.get_rect(bottomleft= (x,y - self.gap))
        self.mask = pygame.mask.from_surface(self.image) # mask for collision
    def faster(self,option):
        # changes the speed of the pipes
        if option == 1:
            self.speed = 7
        elif option == 2:
            self.speed == 8
    def update(self):
        # animates the pipes
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill() # kills the sprite if it goes out of the screen