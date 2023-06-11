import pygame,json
import pygame_textinput as pt
from random import randint
from sys import exit
from player import Player
from pipes import Pipe

## class

class Game:

    
    # surfaces
    def __init__(self):
        pygame.init()
        self.scroll = -100
        self.speed = 7
        self.width = 800
        self.height = 400
        self.screen = pygame.display.set_mode((800,400))
        pygame.display.set_caption("Flappy Bird")
        self.font = pygame.font.Font("font/flappyfont.TTF", 37)
        self.clock = pygame.time.Clock()
        pygame_icon = pygame.image.load("sprites/bird.png")
        pygame.display.set_icon(pygame_icon)
        
        self.test_font = pygame.font.Font("font/Pixeltype.ttf",49)
        self.game_active = False
        sky = pygame.image.load("sprites/background.png").convert_alpha()
        self.sky = pygame.transform.scale(sky, size = (self.width,self.height))
        # Welcome screen
        title = pygame.image.load("sprites/title.png").convert_alpha()
        self.title = pygame.transform.scale(title, size = (self.width/2+20,self.height/2))
        self.title_rect = self.title.get_rect(center = (400,100))
        self.play  =  pygame.image.load("sprites/play.png").convert_alpha()
        self.play_rect = self.play.get_rect(center = (300,264))
        self.leaderboard  =  pygame.image.load("sprites/podium.png").convert_alpha()
        self.leader_rect = self.leaderboard.get_rect(bottomleft = (420,300))



        base = pygame.image.load("sprites/base.png").convert_alpha()
        self.base = pygame.transform.scale(base, size = (self.width+100,self.height/4))
        self.player_sprite = pygame.sprite.Group()
        self.player = Player(self.player_sprite)
        self.score = 0
        self.pipe_sprites = pygame.sprite.Group()
        ## Timer
        self.pipe_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.pipe_timer,1400)
        ## score
        self.score = 0 
        self.high_score = 0
        self.low_score = 0
        self.flag = False
        self.font_surf = self.font.render(str(self.score), False, (0,0,0))
        self.font_rect = self.font_surf.get_rect(center= (400,70))
        self.high = self.font.render(f"HIGHT SCORE :  {self.high_score}",False, (249,249,249))
        self.high_rect = self.high.get_rect(center= (400,120))
        # text
        self.text_flag = False
        self.text = pt.TextInputVisualizer()
        self.welcome_screen = True
        ## leaderboarddd
        self.board = {}
    def score_calculate(self):
        if len(self.pipe_sprites):
            if self.player.rect.left > self.pipe_sprites.sprites()[0].rect.left:

                if self.player.rect.left < self.pipe_sprites.sprites()[0].rect.right:
                    self.flag = True

            if self.flag == True:
                if self.player.rect.left > self.pipe_sprites.sprites()[0].rect.right:
                    self.score += 1

                    self.flag = False
        self.font_surf = self.font.render(str(self.score), False, (0,0,0))
        self.screen.blit(self.font_surf, self.font_rect)
        #self.player_mask = pygame.sprite.Group()
        #self.mask = pygame.mask.from_surface(self.player.image)
        #self.player_mask.add(self.mask)

        ## player and obstacles objects
    def pipe_generate(self):
        pipe_gap = randint(-90, 70)
        self.upper_pipe=Pipe(self.pipe_sprites, 800, 200 + pipe_gap, 1)
        self.lower_pipe = Pipe(self.pipe_sprites, 800, 200 + pipe_gap, 0)
       
    def collision(self):
        if pygame.sprite.spritecollide(self.player, self.pipe_sprites, False, pygame.sprite.collide_mask) or self.player.rect.bottom >=374:
            self.game_active = False
            self.welcome_screen = False
            self.append_data()
            self.check_high(self.score)
            #self.display_board()
        else :
            self.game_active = True
    def difficulty(self):
        for sprite in self.pipe_sprites.sprites():
            if self.score >=7:
                sprite.faster(1)
                self.speed = 10 
            elif self.score > 14:
                sprite.faster(2)
                self.speed = 13
    def reset(self):
        self.score = 0
        self.pipe_sprites.empty()
    def read_leaderboard(self):
        try:
            with open("board.json","r") as file1:
                self.board = json.load(file1)
        except:
            self.board = {}
    def check_high(self,score):
        if len(self.board):
            maxScore = max(self.board.values())
            self.low_score = min(self.board.values())
            if score >= int(maxScore):
                self.high_score= score
            else:
                self.high_score = maxScore
            self.high = self.font.render(f"HIGHT SCORE :  {self.high_score}",False, (249,249,249))
           
    def append_data(self):
        if self.score > self.low_score:
            name = 1
            if name not in self.board.keys():
                self.board[name]= self.score
            self.board = dict(reversed(sorted(self.board.items(),key = lambda x:x[1])))
            with open("board.json","w") as file1:
                json.dump(self.board, file1)
    def name(self):
        self.text_flag= True
        keys= pygame.event.get()
        self.text.update(keys)
        self.screen.blit(self.text.surface, (100,200))
   
        

    def display_board(self):
        maxLen = 6
        padding = 0
        index = 1
        
        self.screen.blit(self.sky,(0,0))

        pygame.draw.rect(self.screen, (200,200,200), (180,70,340,290),border_radius=40)
        new_score = self.test_font.render(f"NO.   NAME     SCORE", False, (0,0,0))
        self.screen.blit(new_score,(200,80+padding))
        for keys in self.board:
            if index <= maxLen:
                new_score = self.test_font.render(f"{index:<10}{keys:<13}{self.board[keys]}", False, (0,0,0))
                self.screen.blit(new_score,(200,120+padding))
                padding +=40
                index +=1
                
    

    def menu(self):
        mos = pygame.mouse.get_pos()
        down,temp,temp2 = pygame.mouse.get_pressed()
        if self.welcome_screen: 
            self.screen.blit(self.title, self.title_rect)
        else:
            self.score_calculate()
            self.screen.blit(self.high,self.high_rect)
        self.screen.blit(self.play, self.play_rect)
        self.screen.blit(self.leaderboard, self.leader_rect)
        if self.play_rect.collidepoint(mos):
            if down:
                self.reset()
                self.game_active= True
        #elif self.leader_rect.collidepoint(mos):

            #self.display_board()

                ################################## DO ITTTT
                
    
       
        
    
    def main(self):
        check = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and  event.key == pygame.K_SPACE:
                    if self.game_active == False:
                        self.game_active = True
                        self.reset()
                        
                     
                    else:
                        self.player.jump()
                if self.game_active:
                    if event.type == self.pipe_timer:
                        self.pipe_generate()
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.leader_rect.collidepoint(event.pos):
                            check = True
                            


            self.screen.blit(self.sky,(0,0))
            self.read_leaderboard()
            if self.game_active:
                check = False
                self.scroll -= self.speed
                if self.scroll <= -100:
                    self.scroll = -30
                self.player_sprite.draw(self.screen)
                self.player_sprite.update()
                self.pipe_sprites.draw(self.screen)
                self.pipe_sprites.update()
                self.score_calculate()
                self.collision()
                self.difficulty()

            else:
                self.player_sprite.draw(self.screen)
                self.player_sprite.update()  
                self.player.reset()
                self.menu()
           
                if check: self.display_board()
                
                
            self.screen.blit(self.base,(self.scroll,360))
            pygame.display.update()
            self.clock.tick(45)

try:
    game = Game()
    game.main()
except Exception as e:
    print(e)
    raise
    pygame.quit()
    exit()
