import pygame,json
from random import randint
from sys import exit
from player import Player
from pipes import Pipe

## class

class Game:
    def __init__(self):
        pygame.init() 
        # initialization of important assets
        self.speed = 7
        self.width = 800
        self.height = 400
        self.screen = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("Flappy Bird")
        self.font = pygame.font.Font("font/flappyfont.TTF", 37)
        self.clock = pygame.time.Clock() 
        pygame_icon = pygame.image.load("sprites/bird.png")
        pygame.display.set_icon(pygame_icon)
        self.test_font = pygame.font.Font("font/Pixeltype.ttf",49)
        self.game_active = False # condition for the main game
        sky = pygame.image.load("sprites/background.png").convert_alpha()
        self.sky = pygame.transform.scale(sky, size = (self.width,self.height)) # sky bg , resizes the image to fit the screen
        base = pygame.image.load("sprites/base.png").convert_alpha()
        self.base = pygame.transform.scale(base, size = (self.width+100,self.height/4)) # ground, resizes the image to fit the screen
        self.scroll = -100 # speed of ground animation
        # Welcome screen  # loads the images of welcome screen and initializes rects
        title = pygame.image.load("sprites/title.png").convert_alpha()
        self.title = pygame.transform.scale(title, size = (self.width/2+20,self.height/2))
        self.title_rect = self.title.get_rect(center = (400,100))
        self.play  =  pygame.image.load("sprites/play.png").convert_alpha()
        self.play_rect = self.play.get_rect(center = (300,264))
        self.leaderboard  =  pygame.image.load("sprites/podium.png").convert_alpha()
        self.leader_rect = self.leaderboard.get_rect(bottomleft = (420,300))
        # player and pipes groups
        self.player_sprite = pygame.sprite.Group()
        self.player = Player(self.player_sprite) # stores the player object
        self.pipe_sprites = pygame.sprite.Group()  # stores all the pipe objects
        ## Timer
        self.pipe_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.pipe_timer,1400) # spawn timer for pipes
        ## score
        self.score = 0 
        self.high_score = 0
        self.low_score = 0 # lowest score on the leaderboard
        self.flag = False
        self.font_surf = self.font.render(str(self.score), False, (0,0,0)) # updates the score values
        self.font_rect = self.font_surf.get_rect(center= (400,70))
        self.high = self.font.render(f"HIGHT SCORE :  {self.high_score}",False, (249,249,249)) # renders the high score value on main screen
        self.high_rect = self.high.get_rect(center= (400,120))
        # leaderboard 
        self.text_flag = False 
        self.text = "" # input name for the leaderboard
        self.welcome_screen = True #condition for welcome screen
        self.board = {} # leaderboard 
        # sounds  
        self.bg_music = pygame.mixer.Sound("audio/bg.wav")
        self.die_sound = pygame.mixer.Sound("audio/die.wav")
        self.wing_sound =  pygame.mixer.Sound("audio/wing.wav")
        self.score_sound =  pygame.mixer.Sound("audio/point.wav")
        self.bg_music.set_volume(0.2)
        self.bg_music.play(loops=-1) # loops the bg sound



    def score_calculate(self): 

        if len(self.pipe_sprites):
            if self.player.rect.left > self.pipe_sprites.sprites()[0].rect.left:

                if self.player.rect.left < self.pipe_sprites.sprites()[0].rect.right:
                    self.flag = True  # when bird is in the middle of the pipes

            if self.flag == True: # if bird was in the middle of the pipes
                if self.player.rect.left > self.pipe_sprites.sprites()[0].rect.right:
                    self.score += 1 # increments score if bird crosses the pipes
                    self.score_sound.play() # plays sound
                    self.flag = False
        self.font_surf = self.font.render(str(self.score), False, (0,0,0))
        self.screen.blit(self.font_surf, self.font_rect) # updates the score

    def pipe_generate(self): # generates two pipe objects and stores them in self.pipe_sprites group
        pipe_gap = randint(-90, 70) # randomizes the the length of pipes
        self.upper_pipe=Pipe(self.pipe_sprites, 800, 200 + pipe_gap, 1)
        self.lower_pipe = Pipe(self.pipe_sprites, 800, 200 + pipe_gap, 0)
       
    def collision(self):
        if pygame.sprite.spritecollide(self.player, self.pipe_sprites, False, pygame.sprite.collide_mask) or self.player.rect.bottom >=374: # checks if player is colliding with pipes, or ground
            # uses pygame.mask for pixel perfect collisions
            self.die_sound.play() 
            self.game_active = False # ends the game
            self.text_flag= True # condition for leaderboard name
            self.welcome_screen = False
            self.check_high(self.score) # updates the self.high_score and self.low_score
        else :
            self.game_active = True
    def difficulty(self):  # increases the speed of the pipes 
        for sprite in self.pipe_sprites.sprites(): # goes through every pipe object in the pipe_sprites
            if self.score >=7:
                sprite.faster(1)
                self.speed = 10  # updates the speed of ground animation
            elif self.score > 14:
                sprite.faster(2)
                self.speed = 13
    def reset(self): # resets the values for the next game
        self.score = 0
        self.text = ""
        self.pipe_sprites.empty() # clears the pipe_sprites group
    def read_leaderboard(self): # open the board.json and update  self.board 
        try:
            with open("board.json","r") as file1:
                self.board = json.load(file1)
        except:
            self.board = {}
    def check_high(self,score): # updates the high score and low score
        if len(self.board):
            maxScore = max(self.board.values())
            if len(self.board)>=6: # if leaderboard does not have six values then low_score remains zero 
                self.low_score = min(self.board.values())
            else:
                self.low_score  = 0

            if score >= int(maxScore):
                self.high_score= score
            else:
                self.high_score = maxScore
            self.high = self.font.render(f"HIGHT SCORE :  {self.high_score}",False, (249,249,249)) # renders the high score
           
    def append_data(self): # adds new score in the leaderboard
        if len(self.text) == 4: # name must be four chars
            name = self.text
            if name not in self.board.keys(): # checks if name is already present in the board
                self.board[name]= self.score
            else:
                if self.score > self.board[name]: # if name is already present then checks if the self.score is highter than board score 
                    self.board[name] = self.score
            self.board = dict(reversed(sorted(self.board.items(),key = lambda x:x[1]))) # sorts the dict
            with open("board.json","w") as file1:
                json.dump(self.board, file1)
    def name(self):
        # display name of the user 
        if len(self.text)<=4:
            self.screen.blit(self.sky, (0,0)) # blits sky on the screen
            self.text_render = self.test_font.render(self.text, False, (249,249,249))
            pygame.draw.rect(self.screen, (200,200,200), (180,70,340,290),border_radius=40)
            self.title_render = self.test_font.render("ENTER NAME :", False, (0,0,0))
            self.screen.blit(self.title_render, (200,80))
            pygame.draw.rect(self.screen, (0,00,00), (290,130,100,40),border_radius=10)
            self.screen.blit(self.text_render, (300,140))
            
        else:    
            self.text_flag = False # sets the condition false if length of the name has reached four
        
    
        

    def display_board(self):
        # displays the leaderboard
        maxLen = 6 
        padding = 0 # space between each line
        index = 1
        self.screen.blit(self.sky,(0,0)) # blits sky in the background 

        pygame.draw.rect(self.screen, (200,200,200), (180,70,340,290),border_radius=40)
        new_score = self.test_font.render(f"NO.   NAME     SCORE", False, (0,0,0))
        self.screen.blit(new_score,(200,80))
        for keys in self.board:
            if index <= maxLen:
                new_score = self.test_font.render(f"{index:<10}{keys:<13}{self.board[keys]}", False, (0,0,0))
                self.screen.blit(new_score,(200,120+padding))
                padding +=40
                index +=1
                
    

    def menu(self):
        #displays the main menu and buttons , shows the high score
        mos = pygame.mouse.get_pos()
        down,temp,temp2 = pygame.mouse.get_pressed()
        if self.welcome_screen: # only shows the welcome screen if is the first time
            self.screen.blit(self.title, self.title_rect)
        else:
            self.score_calculate()
            self.screen.blit(self.high,self.high_rect)
        self.screen.blit(self.play, self.play_rect)
        self.screen.blit(self.leaderboard, self.leader_rect) # blits the icons
        if self.play_rect.collidepoint(mos): 
            if down: # starts the game if play button is clicked
                self.reset()
                self.game_active= True

    def main(self):
        check = False # condition for leaderboard display
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and  event.key == pygame.K_SPACE: # starts the game if space is pressed
                    if self.game_active == False:
                        self.game_active = True
                        self.reset()
                        
                     
                    else:
                        self.player.jump() # if game is active than bird jumps
                        self.wing_sound.play()
                if self.game_active:
                    if event.type == self.pipe_timer:
                        self.pipe_generate() # generates pipes
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.leader_rect.collidepoint(event.pos):
                            check = True # shows the leaderboard
 
                    if self.text_flag: # takes input from the user
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_BACKSPACE:
                                self.text = self.text[:-1] # deletes the last character
                            else:
                                self.text += event.unicode
                            


            self.screen.blit(self.sky,(0,0))
            self.read_leaderboard() # laods the leaderboard
            if self.game_active :
                check = False 
                self.scroll -= self.speed # animates the ground 
                if self.scroll <= -100:
                    self.scroll = -30
                # draws the player and pipes
                self.player_sprite.draw(self.screen)
                self.player_sprite.update()
                self.pipe_sprites.draw(self.screen)
                self.pipe_sprites.update()
                # game logic , score calculation and collision detection
                self.score_calculate()
                self.collision()
                self.difficulty()

            elif self.text_flag: # if game has ended and the score is greater tha lowest score on the leaderboard
                if self.score > self.low_score:
                    self.name()
                    self.append_data()
                else:
                    self.text_flag = False # moves on if score is not higher than the lowest score
                

            elif self.game_active == False and self.text_flag == False: # displays the main menu
                self.player_sprite.draw(self.screen)
                self.player_sprite.update()  
                self.player.reset() # resets the bird position
                self.menu()
           
                if check: self.display_board() # shows leaderboard
                
                
            self.screen.blit(self.base,(self.scroll,360)) # displays base all the time
            pygame.display.update()
            self.clock.tick(45)

game = Game()
game.main()
