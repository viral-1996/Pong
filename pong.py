import sys
import pygame
import time
import random

pygame.init()
clock = pygame.time.Clock()


gameIcon = pygame.image.load('pong.jpg')
pygame.display.set_icon(gameIcon)

class ball:
    x = 0
    y = 0
    radius = 7
    xvel = 2 * random.choice((-1,1))
    yvel = 2
    speed=1


class color:
    black = (0, 0, 0)
    white = (255, 255, 255)
    gray = (128, 128, 128)


class paddle:
    x = 0
    y = 0
    width = 10
    height = 75
    thickness = 0
    y_change = 0
    y_vel = 5


class screen:
    width = 600
    height = 400


def check_boundary(paddle, s):
    if (paddle.y < 0 or paddle.y + paddle.height > s.height):
        paddle.y -= paddle.y_change

def text_objects(text, font):
    textSurface = font.render(text, True, c.white)
    return textSurface, textSurface.get_rect()

def message_display(text):
    global score

    score1 = pygame.font.Font('freesansbold.ttf',20)
    TextSurf, TextRect = text_objects(score[0], score1)
    TextRect.center = ((s.width/5),(s.height/10))
    gameDisplay.blit(TextSurf, TextRect)
    #pygame.display.update()

    score2 = pygame.font.Font('freesansbold.ttf',20)
    TextSurf, TextRect = text_objects(score[1], score2)
    TextRect.center = ((s.width/5*4),(s.height/10))
    gameDisplay.blit(TextSurf, TextRect)
    #pygame.display.update()

    largeText = pygame.font.Font('freesansbold.ttf',40)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((s.width/2),(s.height/4*3))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(3)
    return 1

def button(msg,x,y,w,h,ic,action=None):
    mouse = pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    #print(click)

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
        if click[0]==1 and action !=None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)


def quitgame():
    pygame.quit()
    quit()

def paused():
    global pause
    while pause:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    unpaused()
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    quitgame()
                
        gameDisplay.fill(c.black)
        largeText = pygame.font.Font('freesansbold.ttf',50)
        TextSurf, TextRect = text_objects("Paused", largeText)
        TextRect.center = ((s.width/2),(s.height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("Continue",100,300,100,50,c.black,unpaused)
        button("Quit",400,300,100,50,c.black,quitgame)
        
        pygame.display.update()
        clock.tick(3000)

def unpaused():
    global pause
    pause = False

def update_ball_pos(b, s, p1, p2):
    global score
    if b.y - b.radius < 0:
        b.yvel = - b.yvel
        b.y += int(b.yvel)
    elif b.y + b.radius > s.height:
        b.y -= int(b.yvel)
        b.yvel = - b.yvel
    #paddle1
    elif b.x - b.radius < p1.x + p1.width:
        if b.y > p1.y and b.y < p1.y + p1.height:
            b.xvel = - b.xvel
            b.x += int(b.xvel)
        else:
            b.yvel=2*random.choice((-1,1))
            b.xvel=2*random.choice((-1,1))
            p1.y_vel=5
            p2.y_vel=5
            score=(score[0],str(int(score[1])+1))
            return message_display("Player 2 Wins")
    #paddle2
    elif b.x + b.radius > s.width - p2.width - 10:
        if b.y > p2.y and b.y < p2.y + p2.height:
            b.x -= int(b.xvel)
            b.xvel = - b.xvel
        else:
            b.xvel=2*random.choice((-1,1))
            b.yvel=2*random.choice((-1,1))
            p1.y_vel=5
            p2.y_vel=5
            score=(str(int(score[0])+1),score[1])
            return message_display("Player 1 wins")
    else:
        b.x += int(b.xvel)
        b.y += int(b.yvel)


def game_intro():
    intro = True

    while intro:
        for event1 in pygame.event.get():
            # print(event)
            if event1.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event1.type == pygame.KEYDOWN:
                if event1.key == pygame.K_RETURN:
                    game_loop()
                if event1.key == pygame.K_ESCAPE or event1.key == pygame.K_q:
                    quitgame()

        gameDisplay.fill(c.black)
        largeText = pygame.font.Font('freesansbold.ttf',50)
        TextSurf, TextRect = text_objects("Pong", largeText)
        TextRect.center = ((s.width/2),(s.height/2))
        gameDisplay.blit(TextSurf, TextRect)
        button("Play",100,300,100,50,c.black,game_loop)
        button("Quit",400,300,100,50,c.black,quitgame)

        pygame.display.update()
        clock.tick(3000)
        

        
def render(c,p1,p2,b,s):

    gameDisplay.fill(c.black)
    # paddle1
    pygame.draw.rect(gameDisplay, c.white, (p1.x, p1.y, p1.width, p1.height), p1.thickness)
    # paddle2
    pygame.draw.rect(gameDisplay, c.white, (p2.x, p2.y, p2.width, p2.height), p2.thickness)
    # ball
    pygame.draw.circle(gameDisplay, c.white, (b.x, b.y), b.radius, 0)
    # line
    pygame.draw.line(gameDisplay, c.gray, (s.width/2,0), (s.width/2,s.height))
    #print(clock.get_fps())
    pygame.display.update()

def game_loop():
    global pause
    pause=False
    gameExit = False
    global score
    score = ("0","0")
    speedevent = pygame.USEREVENT+1
    renderevent = pygame.USEREVENT+1
    pygame.time.set_timer(speedevent,10) # eventid, milliseconds
    pygame.time.set_timer(renderevent,8) # 125fps

    # initial values
    b.x = int(s.width / 2)
    b.y = int(s.height / 2)
    p1.x = 10
    p1.y = s.height / 2 - p1.height / 2
    p2.x = s.width - 10 - p2.width
    p2.y = s.height / 2 - p2.height / 2
    p1.y_change = 0
    p2.y_change = 0

    while not gameExit:
        pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    p1.y_change = -p1.y_vel
                if event.key == pygame.K_s:
                    p1.y_change = p1.y_vel
                if event.key == pygame.K_UP:
                    p2.y_change = -p1.y_vel
                if event.key == pygame.K_DOWN:
                    p2.y_change = p1.y_vel
                if event.key == pygame.K_p:
                    pause=True
                paused()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    p1.y_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    p2.y_change = 0

            if event.type == speedevent:
                b.xvel*=1.0005
                b.yvel*=1.0005
                p1.y_vel*=1.0002
                p2.y_vel*=1.0002

            if event.type == renderevent:
                render(c, p1, p2, b, s)

        # updating position
        p1.y += p1.y_change
        p2.y += p2.y_change
        check_boundary(p1, s)
        check_boundary(p2, s)
        if update_ball_pos(b, s, p1, p2):
            b.x = int(s.width/2)
            b.y = int(s.height/2)


s = screen()
c = color()
b = ball()
p1 = paddle()
p2 = paddle()

gameDisplay = pygame.display.set_mode((s.width, s.height))

game_intro()
game_loop()