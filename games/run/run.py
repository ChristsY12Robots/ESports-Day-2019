#!python35
import pygame
import random
import sys
import time
import os
sys.path.insert(0 , 'J:\menu')
import profile

username = os.getlogin()
round_score = 0
timer = 0
width,height = 800,600
pygame.init()
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
red = (255,0,0)
yellow = (255,230,0)
yellow2 = (255,188,0)
orange = (255,128,0)
orange2 = (255,77,0)

collision_detected = False
gameloop = True
board = pygame.display.set_mode((width,height)) #Creates the board
pygame.display.set_caption("Run") #Used to set the title of the board window
smoothx,smoothy = 0,0 # SmoothX and SmoothY will be added to the player coordinates to allow constant motion when a user clicks one of the arrow keys
fps = pygame.time.Clock() #A pygame function that is used to control the amount of cycles per second
level = 1
scoreboard = 0
num_scrap = 0
smallfont = pygame.font.SysFont('Verdana', 15) #Assigns the font verdana when displaying the score
largefont = pygame.font.SysFont('Verdana', 40)
background = pygame.image.load("RunBackground.jpg")
start_button = pygame.image.load("RunStartButton.png")
quit_button = pygame.image.load("RunQuitButton.png")
scorebackground = pygame.image.load("scorebackground.jpg")
superchargetext = pygame.image.load("supercharge.png")
instructions = pygame.image.load("RunInstructions.jpg")

menu = True

#RUNNING IMAGES OF PROBOTS
right_run_frame_1 = pygame.image.load("rsz_run1.png")
right_run_frame_2 = pygame.image.load("rsz_run2.png")
right_run_frame_3 = pygame.image.load("rsz_run3.png")
right_run_frame_4 = pygame.image.load("rsz_run4.png")
right_run_frame_5 = pygame.image.load("rsz_run5.png")
right_run_frame_6 = pygame.image.load("rsz_run6.png")
right_run_frame_7 = pygame.image.load("rsz_run7.png")
right_run_frame_8 = pygame.image.load("rsz_run8.png")

left_run_frame_1 = pygame.transform.flip(right_run_frame_1, True, False)
left_run_frame_2 = pygame.transform.flip(right_run_frame_2, True, False)
left_run_frame_3 = pygame.transform.flip(right_run_frame_3, True, False)
left_run_frame_4 = pygame.transform.flip(right_run_frame_4, True, False)
left_run_frame_5 = pygame.transform.flip(right_run_frame_5, True, False)
left_run_frame_6 = pygame.transform.flip(right_run_frame_6, True, False)
left_run_frame_7 = pygame.transform.flip(right_run_frame_7, True, False)
left_run_frame_8 = pygame.transform.flip(right_run_frame_8, True, False)

dead_robot = pygame.image.load('deadrobot.png')

class user:    
    def __init__(self,x,y):
        self.type = 'player'
        self.lives = 5 #Amount of lives the user has 
        self.x = x #Players x coordinate
        self.y = y #Players y coordinate
        self.width = 10 #Player Sprite Width
        self.height = 10 #Player Sprite Height
        
    def draw(self):
        #This restricts the user from leaving the board as it constantly updates the user coordinates to the edge values
        if self.x <= 0:
            self.x = 0 + (self.width/2)
        if self.x >= width - self.width:
            self.x = width - (self.width)
        if self.y <= 0:
            self.y = 0 + (self.height/2)
        if self.y >= height - self.height:
            self.y = height - (self.height)
        #Applies smoothx and smoothy to the player coordinates so the player can move when a user holds down a key
        self.x += smoothx
        self.y += smoothy
        pygame.draw.rect(board,white,(self.x,self.y,self.width,self.height)) #Displays the user sprite

    def lives(self):
        #Used to check and update the lives of a user
        if self.lives != 0: #If the lives of the player are not 0 it minuses one as this function is triggered when a collision occurs with a bot
            self.lives -= 1
        #This will send each bot to the remove_bots method in the robot class
        for bot in bots:
            robot.remove_bots(bot)
        if self.lives == 0:
            gameloop = False #Stop the gameloop if the user no longer has any lives
        lives_remaining()        
        
        

class robot:
    def __init__(self):
        self.type = 'robot'
        self.orientation = ''
        self.index = 0
        #x and y are randomly generated
        x = list(range(0, width))
        y = list(range(0,height))
        safe_x = []
        safe_y = []
        for number in x:
            if number not in range(275,525):
                safe_x.append(number)
        for number in y:
            if number not in range(175,425):
                safe_y.append(number)
        self.x = random.choice(safe_x) #x is assigned from outside the safe radius
        self.y = random.choice(safe_y)#y is assigned from outside the safe radius
        for i in range(10):
            try:
                safe_x.remove(self.x + i)
                safe_x.remove(self.x - i)
                safe_y.remove(self.y + i)
                safe_y.remove(self.y - i)
            except ValueError:
                pass

        self.colour = red # Sets the colours of bots to red      
        self.ground = False # Ground is used to make a bot stationary when it turns into a scrap pile
        self.width = 10
        self.height = 10

    def draw_bots(self):
        self.index += 1
        #Displays the bots
        '''pygame.draw.rect(board,self.colour,(self.x,self.y,self.width,self.height))'''
        if self.index >= 9:
            self.index = 1
        if self.ground == True:
            board.blit(dead_robot, [self.x,self.y])
        if self.ground != True:            
            if self.orientation == 'right':            
                if self.index == 1:
                    board.blit(right_run_frame_1, [self.x, self.y])
                if self.index == 2:
                    board.blit(right_run_frame_2, [self.x, self.y])
                if self.index == 3:
                    board.blit(right_run_frame_3, [self.x, self.y])        
                if self.index == 4:
                    board.blit(right_run_frame_4, [self.x, self.y])
                if self.index == 5:
                    board.blit(right_run_frame_5, [self.x, self.y])
                if self.index == 6:
                    board.blit(right_run_frame_6, [self.x, self.y])
                if self.index == 7:
                    board.blit(right_run_frame_7, [self.x, self.y])
                if self.index == 8:
                    board.blit(right_run_frame_8, [self.x, self.y])
                    
            if self.orientation == 'left':            
                if self.index == 1:
                    board.blit(left_run_frame_1, [self.x, self.y])
                if self.index == 2:
                    board.blit(left_run_frame_2, [self.x, self.y])
                if self.index == 3:
                    board.blit(left_run_frame_3, [self.x, self.y])        
                if self.index == 4:
                    board.blit(left_run_frame_4, [self.x, self.y])
                if self.index == 5:
                    board.blit(left_run_frame_5, [self.x, self.y])
                if self.index == 6:
                    board.blit(left_run_frame_6, [self.x, self.y])
                if self.index == 7:
                    board.blit(left_run_frame_7, [self.x, self.y])
                if self.index == 8:
                    board.blit(left_run_frame_8, [self.x, self.y])
                
    def remove_bots(self):
        #Removes the bots when the player collides with a robot and then it calls the function generate_bots to replace them with new ones
        del bots[:]
        generate_bots()
        
    def pathfinding(self):
        #Compares the x values and y values with the player and moves towards it accordingly
        #E.G playerx = 5 botx = 2 if playerx > botx botx +=1
        speed = 3
        if timer > 1000:
            speed = 5
        if self.x <= 0:
            self.x = 0 + (self.width/2)
        if self.x >= width - self.width:
            self.x = width - (self.width)
        if self.y <= 0:
            self.y = 0 + (self.height/2)
        if self.y >= height - self.height:
            self.y = height - (self.height)
        if self.ground != True:
            if player.x > self.x:
                self.orientation = 'right'
                self.x += speed
            if player.x < self.x:
                self.orientation = 'left'
                self.x -= speed
            if player.y > self.y:
                self.y += speed
            if player.y < self.y:
                self.y -= speed
                
    def scrap_pile(self,other):
        global num_scrap
        self.ground = True #Makes the bot stationary
        self.colour = blue #Makes the scrap pile blue
        if other in bots:
            bots.remove(other)  #Removes one of the bots when two collide together so one scrap pile is created     
        self.type = 'scrap'

        
class collision:
    def __init__():
        super().__init__()
        
    def bot_collision_detection(self, other):
        collision_detected = False
        #checks each region of the bot to see if it collided with another bot
        if other.x + other.width >= self.x >= other.x and other.y + other.height >= self.y >= other.y:
            collision_detected = True
        if other.x + other.width >= self.x + self.width >= other.x and other.y + other.height >= self.y >= other.y:
            collision_detected = True
        if other.x + other.width >= self.x >= other.x and other.y + other.height >= self.y + self.height >= other.y:
            collision_detected = True
        if other.x + other.width >= self.x + self.width>= other.x and other.y + other.height >= self.y  + self.height >= other.y:
            collision_detected = True
        if collision_detected == True:
            robot.scrap_pile(self,other)
            
    def user_collision_detection(self, other):
        #checks each region of the bot to see if it collided with another bot
        collision_detected = False
        if other.x + other.width >= self.x >= other.x and other.y + other.height >= self.y >= other.y:
            collision_detected = True
        if other.x + other.width >= self.x + self.width >= other.x and other.y + other.height >= self.y >= other.y:
            collision_detected = True
        if other.x + other.width >= self.x >= other.x and other.y + other.height >= self.y + self.height >= other.y:
            collision_detected = True
        if other.x + other.width >= self.x + self.width>= other.x and other.y + other.height >= self.y  + self.height >= other.y:
            collision_detected = True
        if collision_detected == True:
            user.lives(self)

def generate_bots():
    player.x, player.y =int(width/2),int(height/2) #updates the player position back to the centre
    global bots
    global timer
    timer = 0
    if level == 1:
        bots = [robot() for x in range(3)] #Creates 5 bot instances when level is 1
    if level == 2:
        bots = [robot() for x in range(5)]
    if level == 3:
        bots = [robot() for x in range(7)] #Creates 10 bot instances when level is 2
    if level == 4:
        bots = [robot() for x in range(11)] #Creates 10 bot instances when level is 3
    if level == 5:
        bots = [robot() for x in range(13)] #Creates 10 bot instances when level is 4
    if level == 6:
        bots = [robot() for x in range(15)]
    if level > 6:
        winning_screen()


def score(score):
    #Displays the Score
    text = smallfont.render('Score: ' + str(score), True, white)
    board.blit(text, [0,0])

def display_lives():
    if player.lives == 0:
        winning_screen()
    #Displays the Lives
    else:
        text = smallfont.render('Lives: ' + str(player.lives), True, white)
        board.blit(text, [0, 15])


def countdown():
    global round_score
    round_score = scoreboard
    for x in range(3, 0, -1):
        board.fill(black)
        text = smallfont.render('Level ' + str(level), True, white)
        num_of_bots = smallfont.render('Number of Robots: ' + str(len(bots)), True, white)
        numbers = smallfont.render('Starting In ' + str(x), True, white)
        board.blit(text, [width/2- 50, height/2 - 50])
        board.blit(num_of_bots, [width/2- 100, height/2 - 25])
        board.blit(numbers, [width/2- 75, height/2])        
        pygame.display.flip()        
        time.sleep(1)

def lives_remaining():
    global scoreboard
    global round_score
    scoreboard = round_score
    board.fill(black)
    text = smallfont.render('Lives Remaining: ' + str(player.lives), True, white)
    board.blit(text, [width/2- 90, height/2 - 50])
    pygame.display.flip()        
    time.sleep(3)

def create_environment():
    generate_bots()
    countdown()

def super_charge_bar():
    board.blit(superchargetext,[width/2 - 52, 0])
    bar_width = 0.14 * timer
    if timer < 500:
        pygame.draw.rect(board,yellow,(325,20,bar_width,10))
    if timer >= 500 and timer < 750:
        pygame.draw.rect(board,yellow2,(325,20,bar_width,10))
    if timer >= 750 and timer < 875:
        pygame.draw.rect(board,orange,(325,20,bar_width,10))
    if timer >= 875 and timer < 1000:
        pygame.draw.rect(board,orange2,(325,20,bar_width,10))
    if timer >= 1000:
        pygame.draw.rect(board,red,(325,20,140,10))        
        
def run_instructions():
    clicked = False
    while clicked == False:
        click = pygame.mouse.get_pressed()
        board.blit(instructions,[0,0])
        pygame.display.update() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                create_environment()
                clicked = True
    
def start_menu():
    global menu
    while menu == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 125 + 172 > mouse[0] > 150 and 448 + 69 > mouse[1] > 448 and click[0] == 1:
            menu = False
            run_instructions()
            break
        if 502 + 172 > mouse[0] > 502 and 448 + 69 > mouse[1] > 448 and click[0] == 1:
            menu = False
            pygame.quit()
            quit()
        board.blit(background,(0,0))
        board.blit(start_button,(125,448))
        board.blit(quit_button,(502,448))
        pygame.display.update()


player = user(int(width/2),int(height/2))    
start_menu()

def winning_screen():
    global gameloop
    global fps
    gameloop = False
    score_display = scoreboard
    score_display = score_display + (player.lives * 500)
    scoretext = largefont.render(str(score_display), True, white)
    x_shift = len(str(score_display)) * 11.5
    board.blit(scorebackground, [0,0])
    board.blit(scoretext, [width/2- x_shift, height/2])    
    pygame.display.update()
    save(score_display)
    time.sleep(2)
    pygame.display.quit()
    quit()
    pygame.quit()


def save(score_display):
    user_profile = profile.User_Profile(username)
    user_profile.update_score(score_display)
    user_profile.add_game_record('Run')
    #user_profile.save()
    
#MAIN GAME LOOP
while gameloop == True:
    num_scraps = 0

    fps.tick(60) #Sets FPS to 60
    
    for event in pygame.event.get(): #Checks each event
        if event.type == pygame.QUIT: #If one of the events are quit (when the user clicks the X in the top right corner) the window closes
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if  event.key == pygame.K_w:
                smoothy = -5
            elif  event.key == pygame.K_s:
                smoothy = 5
            elif  event.key == pygame.K_a:
                smoothx = -5
            elif  event.key == pygame.K_d:
                smoothx = 5
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w and smoothy < 0:
                smoothy = 0
            elif event.key == pygame.K_s and smoothy > 0:
                smoothy = 0
            elif event.key == pygame.K_a and smoothx < 0:
                smoothx = 0
            elif event.key ==pygame.K_d and smoothx > 0:
                smoothx = 0                  
                
        
    board.fill(black) #Fills the board with black
    for bot in bots:
        #For every bot it draws it and runs the pathfinding function to move towards the user
        robot.draw_bots(bot)
        robot.pathfinding(bot)
        #Checks for collisions between bots and bots as well as user and bots
        for x in bots:
            if bot != x:
                collision.bot_collision_detection(bot,x)
                collision.user_collision_detection(player,x)
    scoreboard += 1 #Adds one to the scoreboard each time
    score(scoreboard)
    display_lives()
    for bot in bots:
        if bot.type == 'scrap':
            num_scraps += 1
    if num_scraps == len(bots):
        level += 1
        generate_bots()
        countdown()
    timer += 1
    player.draw()
    super_charge_bar()
    pygame.display.update()

pygame.quit()
quit()           
