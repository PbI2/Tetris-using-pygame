
import pygame, sys, random, time
from pygame.locals import *
FPS=30
WINDOWWIDTH = 1400
WINDOWHEIGHT = 768
BLOCK_GAP = 1
#註 : 與 reference1.py 不同的地方會有 diff: 標記在前
BOARDWIDTH = 300 + 9 * BLOCK_GAP
BOARDHEIGHT = 600 + 19 * BLOCK_GAP
BOARD_SPACE = (WINDOWWIDTH - BOARDWIDTH * 2)/3
BOARD_UP = (WINDOWHEIGHT - BOARDHEIGHT)/2
RECT_BOARD1 = pygame.Rect(BOARD_SPACE, BOARD_UP, BOARDWIDTH, BOARDHEIGHT)
RECT_BOARD2 = pygame.Rect(BOARD_SPACE * 2 + BOARDWIDTH, BOARD_UP, BOARDWIDTH, BOARDHEIGHT)

BLOCK_SIZE =(BOARDWIDTH - 9 * BLOCK_GAP) / 10

#colors
BLACK   = (  0,  0,  0)
WHITE   = (255,255,255)
RED     = (255,  0,  0) 
GREEN   = (  0,255,  0)
BLUE    = (  0,  0,255)
YELLOW  = (255,255,  0)
AQUA    = (  0,255,255)
MAGENTA = (255,  0,255)
ORANGE = (255,127,0)
PURPLE = (128,0,128)

BACK_GROUND_COLOR = BLACK
dropfrequency = 0.25
movesidewayfrequency = 0.15
movedownfrequency = 0.1
rotatefrequency = 0.1
class BLOCK:
    def __init__(self, x, y, color = BACK_GROUND_COLOR ):
        self.x = x 
        self.y = y
        self.state = '0'
        self.color = BACK_GROUND_COLOR
        self.left1 = BOARD_SPACE + self.x * (BLOCK_SIZE + BLOCK_GAP)
        self.left2 = BOARD_SPACE * 2 + BOARDWIDTH + self.x * (BLOCK_SIZE + BLOCK_GAP)
        self.up = BOARD_UP + self.y * (BLOCK_SIZE + BLOCK_GAP)
        self.rect1 = (self.left1, self.up, BLOCK_SIZE, BLOCK_SIZE)
        self.rect2 = (self.left2, self.up, BLOCK_SIZE, BLOCK_SIZE)
    def clear(self):
        self.state = '0'
        self.color = BACK_GROUND_COLOR
    def __str__(self):
        return f'[{self.x}, {self.y}]'
AboveLine = 0       
# diff: we need to set up two block board to run       
Allblocks1=[[BLOCK(i,j) for i in range(10)] for j in range(-AboveLine,20)]
Allblocks2=[[BLOCK(i,j) for i in range(10)] for j in range(-AboveLine,20)]
def AllColumnSign(Allblocksign): # transfer the row to the column
    empty2 = []
    for j in range(len(Allblocksign[0])):
        empty = []
        for i in range(len(Allblocksign)):
            empty.append(Allblocksign[i][j])
        empty2.append(empty)
    return empty2

#[...-3,...-2,...-1,[[0, 0], [1, 0],..., [9, 0]][[0, 1],...[9, 1]]...]
#O,I,J,L,S,T,Z
TetrisColorDict = {'I':AQUA, 'J':BLUE, 'L':ORANGE, 'O':YELLOW, 'S':GREEN, 'T':PURPLE, 'Z':RED}
TetrisRotationtypeDict = {'I':2, 'J':4, 'L':4, 'O':1, 'S':2, 'T':4, 'Z':2}
class Tetris:
    def __init__(self, shape):
        self.shape = shape
        self.center = [4,0]
        self.rotationstate = 0    
        self.color = TetrisColorDict[self.shape]    

    def centerx(self):
        return self.center[0]
    def centery(self):
        return self.center[1]
    def rotationtype(self):
        return TetrisRotationtypeDict[self.shape]
    def position(self):

        if self.shape == 'I':
            if self.rotationstate >= 2:
                self.rotationstate = self.rotationstate % 2
            search = {0:[[self.centerx(),self.centery()-2], [self.centerx(),self.centery()-1], [self.centerx(),self.centery()], [self.centerx(),self.centery()+1]],
                      1:[[self.centerx()+2,self.centery()], [self.centerx()+1,self.centery()], [self.centerx(),self.centery()], [self.centerx()-1,self.centery()]]}

            return search[self.rotationstate]
        if self.shape == 'O':
            return [
        [self.centerx(),self.centery()],
        [self.centerx()+1,self.centery()],
        [self.centerx(),self.centery()+1],
        [self.centerx()+1,self.centery()+1]
        ]
        if self.shape == 'J':
            if self.rotationstate >= 4:
                self.rotationstate = self.rotationstate % 4
            search = {0:[[self.centerx(),self.centery()-1], [self.centerx(),self.centery()], [self.centerx(),self.centery()+1], [self.centerx()-1,self.centery()+1]],
                      1:[[self.centerx()+1,self.centery()], [self.centerx(),self.centery()], [self.centerx()-1,self.centery()], [self.centerx()-1,self.centery()-1]],
                      2:[[self.centerx(),self.centery()-1], [self.centerx(),self.centery()], [self.centerx(),self.centery()+1], [self.centerx()+1,self.centery()-1]],
                      3:[[self.centerx()-1,self.centery()], [self.centerx(),self.centery()], [self.centerx()+1,self.centery()], [self.centerx()+1,self.centery()+1]],
                     }

            return search[self.rotationstate]

        if self.shape == 'L':
            if self.rotationstate >= 4:
                self.rotationstate = self.rotationstate % 4
            search = {0:[[self.centerx(),self.centery()-1], [self.centerx(),self.centery()], [self.centerx(),self.centery()+1], [self.centerx()+1,self.centery()+1]],
                      1:[[self.centerx()+1,self.centery()], [self.centerx(),self.centery()], [self.centerx()-1,self.centery()], [self.centerx()-1,self.centery()+1]],
                      2:[[self.centerx(),self.centery()-1], [self.centerx(),self.centery()], [self.centerx(),self.centery()+1], [self.centerx()-1,self.centery()-1]],
                      3:[[self.centerx()-1,self.centery()], [self.centerx(),self.centery()], [self.centerx()+1,self.centery()-1], [self.centerx()+1,self.centery()]],
                     }

            return search[self.rotationstate]
        if self.shape == 'S':
            if self.rotationstate >= 2:
                self.rotationstate = self.rotationstate % 2
            search = {0:[[self.centerx(),self.centery()-1], [self.centerx(),self.centery()], [self.centerx()+1,self.centery()], [self.centerx()+1,self.centery()+1]],
                      1:[[self.centerx()-1,self.centery()], [self.centerx(),self.centery()-1], [self.centerx(),self.centery()], [self.centerx()+1,self.centery()-1]]}

            return search[self.rotationstate]

        if self.shape == 'T':
            if self.rotationstate >= 4:
                self.rotationstate = self.rotationstate % 4
            search = {0:[[self.centerx()-1,self.centery()], [self.centerx(),self.centery()-1], [self.centerx(),self.centery()], [self.centerx()+1,self.centery()]],
                      1:[[self.centerx(),self.centery()-1], [self.centerx(),self.centery()], [self.centerx()+1,self.centery()], [self.centerx(),self.centery()+1]],
                      2:[[self.centerx()+1,self.centery()], [self.centerx(),self.centery()], [self.centerx(),self.centery()+1], [self.centerx()-1,self.centery()]],
                      3:[[self.centerx(),self.centery()-1], [self.centerx(),self.centery()], [self.centerx()-1,self.centery()], [self.centerx(),self.centery()+1]],
                     }

            return search[self.rotationstate]
        if self.shape == 'Z':
            if self.rotationstate >= 2:
                self.rotationstate = self.rotationstate % 2

            search = {0:[[self.centerx(),self.centery()-1], [self.centerx(),self.centery()], [self.centerx()-1,self.centery()], [self.centerx()-1,self.centery()+1]],
                      1:[[self.centerx()-1,self.centery()], [self.centerx(),self.centery()], [self.centerx(),self.centery()+1], [self.centerx()+1,self.centery()+1]]}


            return search[self.rotationstate]



def istop(InputTetris):
    check = InputTetris.position()
    i = 0
    while i < len(check): 
        if [check[i][0],check[i][1]-1] in check:
            check.remove([check[i][0],check[i][1]])
        else:
            i+=1

    return check
def topmost(InputTetris):
    result = istop(InputTetris)
    empty = []
    for i in range(len(result)):
        empty.append(result[i][1])
    return min(empty)
def canRotate(number, InputTetris): # diff: we need to rely on the input number to decide which board we should run
    if InputTetris.shape == 'O':
        return True
    else:
        InputTetris.rotationstate = (InputTetris.rotationstate + 1) % InputTetris.rotationtype()
        check = InputTetris.position()
        if number == 1:
            Allblocks = Allblocks1
        else:
            Allblocks = Allblocks2
        # to simulate whether it is possible for the block to rotate
        for i in range(len(check)):   
            if check[i][1] >= 20: # out of the boundary
                InputTetris.center[1] -= bottom(InputTetris) - 19 #lift up once or twice
                check2 = InputTetris.position()
                for i in range(len(check2)):
                    if Allblocks[check2[i][1]+AboveLine][check2[i][0]].state == '1' : #touch other blocks
                        InputTetris.center[1] +=1
                        return False
            elif check[i][0] >= 10: # touch the right boundary
                InputTetris.center[0] -= rightmost(InputTetris) - 9 # move left
                check2 = InputTetris.position()
                for i in range(len(check2)) :
                    if Allblocks[check2[i][1]+AboveLine][check2[i][0]].state == '1' : #touch other blocks
                        if InputTetris.shape == 'I':
                            InputTetris.center[0] -=1 
                            check3 = InputTetris.position()
                            for i in range(len(check3)) :
                                if Allblocks[check3[i][1]+AboveLine][check3[i][0]].state == '1' : #touch other blocks
                                    InputTetris.center[0] +=2
                                    return False
                            return True
                        else:
                            InputTetris.center[0] +=1
                            return False
                return True
            elif check[i][0] < 0: # touch the left bouundary
                InputTetris.center[0] += -leftmost(InputTetris) 
                check2 = InputTetris.position()
                for i in range(len(check2)):
                    if Allblocks[check2[i][1]+AboveLine][check2[i][0]].state == '1' :
                        if InputTetris.shape == 'I': 
                            InputTetris.center[0] +=1 #try again
                            check3 = InputTetris.position()
                            for i in range(len(check3)) :
                                if Allblocks[check3[i][1]+AboveLine][check3[i][0]].state == '1' : #touch other blocks
                                    InputTetris.center[0] -=2
                                    return False
                            return True
                        else:
                            InputTetris.center[0] -=1
                            return False
                return True
            elif Allblocks[check[i][1]+AboveLine][check[i][0]].state == '1' : # overlap with other blocks
                if check[i] in isleft(InputTetris):
                    InputTetris.center[0] +=1
                    check2 = InputTetris.position()
                    for i in range(len(check2)) :
                        if check2[i][0] >= 10:
                            InputTetris.center[0] -=1
                            return False
                        elif Allblocks[check2[i][1]+AboveLine][check2[i][0]].state == '1' :#we need to consider the "I" block case
                            if InputTetris.shape == 'I':
                                InputTetris.center[0] +=1
                                check3 = InputTetris.position()
                                for i in range(len(check3)) :
                                    if check3[i][0] >= 10:
                                        InputTetris.center[0] -=2
                                        return False
                                    elif Allblocks[check3[i][1]+AboveLine][check3[i][0]].state == '1' :
                                        InputTetris.center[0] -=2
                                        return False
                            else:
                                InputTetris.center[0] -=1
                                return False
                    return True
                elif check[i] in isright(InputTetris):
                    InputTetris.center[0] -=1
                    check2 = InputTetris.position()
                    for i in range(len(check2)) :
                        if check2[i][0] < 0:
                            InputTetris.center[0] +=1
                            return False
                        elif Allblocks[check2[i][1]+AboveLine][check2[i][0]].state == '1' :
                            if InputTetris.shape == 'I':
                                InputTetris.center[0] -=1
                                check3 = InputTetris.position()
                                for i in range(len(check3)) :
                                    if check3[i][0] < 0:
                                        InputTetris.center[0] +=2
                                        return False
                                    elif Allblocks[check3[i][1]+AboveLine][check3[i][0]].state == '1' :
                                        InputTetris.center[0] +=2
                                        return False
                            else:
                                InputTetris.center[0] +=1
                                return False
                    return True
                else: # only 'I' block could possibly reach here

                    if check[i][0] < InputTetris.center[0]:
                        InputTetris.center[0] +=2
                        check3 = InputTetris.position()
                        for i in range(len(check3)) :
                            if check3[i][0] >= 10:
                                InputTetris.center[0] -=2
                                return False
                            elif Allblocks[check3[i][1]+AboveLine][check3[i][0]].state == '1' :
                                InputTetris.center[0] -=2
                                return False
                        return True 
                    else:

                        InputTetris.center[0] -=2
                        check3 = InputTetris.position()
                        for i in range(len(check3)) :
                            if check3[i][0] < 0:
                                InputTetris.center[0] +=2
                                return False
                            elif Allblocks[check3[i][1]+AboveLine][check3[i][0]].state == '1' :
                                InputTetris.center[0] +=2
                                return False
                        return True

        return True
# to find what part of the block is the left side of the block
def isbottom(InputTetris):
    check = InputTetris.position()
    solvedict = {}
    empty = []
    for i in range(len(check)):
        if check[i][0] not in empty:
            empty.append(check[i][0])
            solvedict[check[i][0]] = [check[i][1]]
        else:
            solvedict[check[i][0]] += [check[i][1]]
    result = []
    for i in range(len(empty)):
        result.append([empty[i], max(solvedict[empty[i]])])
    return result
def bottom(InputTetris):
    result = isbottom(InputTetris)
    empty = []
    for i in range(len(result)):
        empty.append(result[i][1])
    return max(empty)
def canDrop(number, InputTetris, Allblocks): # diff: we need to rely on the input number to decide which board we should run
    check = InputTetris.position()
    '''
    if number == 1:
        Allblocks = Allblocks1
    else:
        Allblocks = Allblocks2
        '''
    for i in range(len(check)):
        if check[i][1] >= 19:
            return False
        elif check[i] in isbottom(InputTetris):
            if Allblocks[check[i][1]+AboveLine+1][check[i][0]].state == '1':
                return False
    return True    
def MoveDownSide(number, InputTetris, Allblocks):# diff: we need to rely on the input number to decide which board we should run
    check = InputTetris.position()

    if canDrop(number, InputTetris, Allblocks):
        InputTetris.center[1] +=1 
def Drop(number, InputTetris, Allblocks):# diff: we need to rely on the input number to decide which board we should run

    if canDrop(number, InputTetris, Allblocks):
        InputTetris.center[1] +=1
# In fact, these two functions above are the same, just named differently for their intentions
def isleft(InputTetris):
    check = InputTetris.position()
    solvedict = {}
    empty = []
    for i in range(len(check)):
        if check[i][1] not in empty:
            empty.append(check[i][1])
            solvedict[check[i][1]] = [check[i][0]]
        else:
            solvedict[check[i][1]] += [check[i][0]]
    result = []
    for i in range(len(empty)):
        result.append([min(solvedict[empty[i]]),empty[i]])
    return result
def leftmost(InputTetris):
    result = isleft(InputTetris)
    empty = []
    for i in range(len(result)):
        empty.append(result[i][0])
    return min(empty)
def canMoveLeftside(number, InputTetris):# diff: we need to rely on the input number to decide which board we should run
    check = InputTetris.position()
    if number == 1:
        Allblocks = Allblocks1
    else:
        Allblocks = Allblocks2
    for i in range(len(check)):
        if check[i][0] <= 0:
            return False
        elif check[i] in isleft(InputTetris):
            if Allblocks[check[i][1]+AboveLine][check[i][0]-1].state == '1':
                return False        
    return True
def MoveLeftSide(number, InputTetris):# diff: we need to rely on the input number to decide which board we should run

    if canMoveLeftside(number, InputTetris):
        InputTetris.center[0] -= 1
def isright(InputTetris):# diff: we need to rely on the input number to decide which board we should run
    check = InputTetris.position()
    solvedict = {}
    empty = []
    for i in range(len(check)):
        if check[i][1] not in empty:
            empty.append(check[i][1])
            solvedict[check[i][1]] = [check[i][0]]
        else:
            solvedict[check[i][1]] += [check[i][0]]
    result = []
    for i in range(len(empty)):
        result.append([max(solvedict[empty[i]]),empty[i]])
    return result
def rightmost(InputTetris):
    result = isright(InputTetris)
    empty = []
    for i in range(len(result)):
        empty.append(result[i][0])
    return max(empty)
def canMoveRightside(number,InputTetris):# diff: we need to rely on the input number to decide which board we should run
    check = InputTetris.position()
    if number == 1:
        Allblocks = Allblocks1
    else:
        Allblocks = Allblocks2
    for i in range(len(check)):
        if check[i][0] >= 9:
            return False
        elif check[i] in isright(InputTetris):
            if Allblocks[check[i][1]+AboveLine][check[i][0]+1].state == '1':
                return False 
    return True
def MoveRightSide(number,InputTetris):# diff: we need to rely on the input number to decide which board we should run

    if canMoveRightside(number,InputTetris):
        InputTetris.center[0]+= 1
def MoveDownDirectly(number, InputTetris, Allblocks):# diff: we need to rely on the input number to decide which board we should run

    while canDrop(number, InputTetris, Allblocks) == True:
        InputTetris.center[1] +=1

#'I','J','L','O', 'S', 'T', 'Z'
def main():
    global DISPLAYSURF, Allblocks1, Allblocks2, score1, score2, memory1, memory2, punishment1, punishment2, showtime, image
    pygame.init()
    score1 = 0
    score2 = 0
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Tetris')

    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    DISPLAYSURF.fill(BACK_GROUND_COLOR)
    image = {}
    for shape in ['I','J','L','O', 'S', 'T', 'Z']:
        image[shape] = pygame.image.load(f'image\Tetris{shape}.png')
        image[shape].convert()


    all_the_choice1 = [random.choice(['I','J','L','O', 'S', 'T', 'Z']) for i in range(2000)]
    all_the_choice2 = all_the_choice1
    StartGameAnimation()

    if random.randint(0, 1) == 0:
        pygame.mixer.music.load('tetrisb.mid')
    else:
        pygame.mixer.music.load('tetrisc.mid')
    pygame.mixer.music.play(-1, 0.0)
    
    start_ticks = pygame.time.get_ticks()

    thefirsttwochoice1 = [random.choice(['I','J','L','O', 'S', 'T', 'Z']), random.choice(['I','J','L','O', 'S', 'T', 'Z'])]
    thefirsttwochoice1 = all_the_choice1[:2]
    thefirstone1 = thefirsttwochoice1[0] 
    thesecondone1 = thefirsttwochoice1[1]
    droppingblock1 = Tetris(thefirstone1)
    all_the_choice1 = all_the_choice1[2:]
    print('next1 =', thesecondone1)
    hold1 = None
    print('hold1 =', hold1)
    print('score1 =', score1)
    record1 = False
    lastdrop1 = None
    count1 = 1

    moveleft1 = False
    moveright1 = False
    movedown1 = False
    space1 = False
    rightshift1 = False
    rotate1 = False
    lastMoveSidewaysTime1 = time.time()
    lastRotateTime1 = time.time()
    lastMoveDownTime1 = time.time()
    punishment1 = 0 # it is a transformation of the score2. When the punishment1 is above 15, the player1 would be 'punished' by dropping a special block 
    memory1 = [] #diff: to store the previous eliminated lines, which is used to detect combo
    trial_1 = computer(droppingblock1, Allblocks1)[0]

    print('-----')
    thefirsttwochoice2 = [random.choice(['I','J','L','O', 'S', 'T', 'Z']), random.choice(['I','J','L','O', 'S', 'T', 'Z'])]
    thefirsttwochoice2 = all_the_choice2[:2]
    thefirstone2 = thefirsttwochoice2[0] 
    thesecondone2 = thefirsttwochoice2[1]
    droppingblock2 = Tetris(thefirstone2)
    all_the_choice2 = all_the_choice2[2:]
    print('next2 =', thesecondone2)
    hold2 = None
    print('hold2 =', hold2)
    print('score2 =', score2)
    record2 = False
    lastdrop2 = None

    moveleft2 = False
    moveright2 = False
    movedown2 = False
    space2 = False
    rightshift2 = False
    rotate2 = False
    lastMoveSidewaysTime2 = time.time()
    lastRotateTime2 = time.time()
    lastMoveDownTime2 = time.time()
    punishment2 = 0
    memory2 = []
    count2 = 1
    sound = True
    return_to_page = False
    perform = False
    _unhold = computer(droppingblock2, Allblocks2)
    _hold = computer(Tetris(thesecondone2), Allblocks2)
    trial_2 = thefinaltrial(_unhold, _hold)
    if 'SHIFT' in trial_2:
        thechoice = random.choice(['I','J','L','O', 'S', 'T', 'Z'])
        thechoice = all_the_choice2[0]
        thefirsttwochoice2 = thefirsttwochoice2[1:] + [thechoice]
        all_the_choice2 = all_the_choice2[1:]

    seconds = (pygame.time.get_ticks()-start_ticks)/1000
    showtime = 120 - seconds

    DrawBoard(1, thesecondone1, hold1, score1, punishment2)
    DrawBoard(2, thesecondone2, hold2, score2, punishment1)

    pause = False
    gameover = False
    countdown = 120
    perform = False
    player_1_win = False
    player_2_win = False
    while topmost(droppingblock1) < 0:
        droppingblock1.center[1] +=1
    while topmost(droppingblock2) < 0:
        droppingblock2.center[1] +=1
    while True:

        if not gameover and not pause :
            seconds = int((pygame.time.get_ticks()-start_ticks)/1000)
            showtime = countdown - seconds
            if showtime <= 0:
                showtime = 0
                
                gameover = True
        timer_board()


        for event in pygame.event.get():
            # When QUIT or press the esc key, quit the game
            if event.type == KEYUP:
                if event.key == K_m:
                    if sound == True:
                        pygame.mixer.music.stop()
                        sound = False
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                        sound = True
                elif event.key ==K_p:
                    if pause == False:
                        pause = True
                    #pause
                    else:
                        pause = False
                        start_ticks = pygame.time.get_ticks()
                        '''
                elif event.key == K_SPACE:
                    space2 = False
                elif event.key == K_UP:
                    rotate2 = False
                elif event.key == K_LEFT:
                    moveleft2 = False
                elif event.key == K_RIGHT:
                    moveright2 = False
                elif event.key == K_DOWN:
                    movedown2= False
                    '''
                elif event.key == K_ESCAPE:
                    #pygame.quit()
                    #sys.exit()
                    return_to_page = True
                    break
                
                    '''
                elif event.key == K_RSHIFT:
                    rightshift2 = False
                    '''
            
            elif event.type == QUIT :
                pygame.quit()
                #sys.exit()
                return_to_page = True
                break
            elif pause == True:
                break
                '''
            elif event.type == KEYDOWN:
                if event.key == K_LEFT :
                    MoveLeftSide(2, droppingblock2)
                    moveleft2= True
                    moveright2= False
                    lastMoveSidewaysTime2 = time.time() 
                elif event.key == K_RIGHT:
                    MoveRightSide(2, droppingblock2)
                    lastMoveSidewaysTime2 = time.time()
                    moveright2 = True
                    moveleft2 = False
                elif event.key == K_UP:
                    #rotation

                    rotate2 = True
                    if not canRotate(2, droppingblock2):
                        if droppingblock2.rotationstate == 0:
                            droppingblock2.rotationstate = droppingblock2.rotationtype() - 1
                        else:
                            droppingblock2.rotationstate -= 1

                    lastRotatetime2 = time.time()      
                elif event.key == K_DOWN:
                    MoveDownSide(2, droppingblock2, Allblocks2)
                    movedown2 = True
                    lastMoveDownTime2 = time.time()
                    #accelerate the speed
                elif event.key == K_SPACE:
                    space2 = True
                    MoveDownDirectly(2, droppingblock2, Allblocks2)

                    for location in range(len(droppingblock2.position())):
                        rowlocation = droppingblock2.position()[location][1]
                        columnlocation = droppingblock2.position()[location][0]
                        Allblocks2[rowlocation+AboveLine][columnlocation].state = '1'        
                        Allblocks2[rowlocation+AboveLine][columnlocation].color = droppingblock2.color

                    DrawBoard(2, thesecondone2, hold2, score2, punishment1) 
                    if droppingblock2.color == WHITE:
                        Punishing(droppingblock2, Allblocks2) # do the punishment here

                    number, CompleteRow = FindCompleteRow(2, Allblocks2)
                    completerow = CompleteRow[:]
                    score2 += len(completerow)

                    punishmentscoring(number, completerow) 
                    EliminateRowBlocks((number, CompleteRow))
                    #print(memory2) 
                    thechoice = random.choice(['I','J','L','O', 'S', 'T', 'Z'])
                    thefirsttwochoice2 = thefirsttwochoice2[1:]+[thechoice]
                    thefirstone2 = thefirsttwochoice2[0]
                    thesecondone2 = thefirsttwochoice2[1]
                    droppingblock2 = Tetris(thefirstone2)
                    if PunishmentExecution(1) == True:
                        droppingblock2.color = WHITE
                    while topmost(droppingblock2) < 0:
                        droppingblock2.center[1] +=1
                    print('next2 =', thesecondone2)
                    if hold2 == None:
                        print('hold2 =', hold2)
                    else:
                        print('hold2 =', hold2.shape)
                    record2 = False
                    print('score2 =', score2)
                    #DrawBoard(2, thesecondone2, hold2, score2, punishment2)
                    #just move to the bottom without animation
                elif event.key == K_RSHIFT:
                    if record2 == False:
                        rightshift2 = True   

                '''
        if return_to_page:
            break
        if gameover == True:
            if not perform:
                if score1 > score2:
                    WinnerAnimation(1, True)
                elif score2 > score1:
                    WinnerAnimation(2, True)
                else:
                    WinnerAnimation(0, True) 
                perform = True
                DrawBoard(2, thesecondone2, hold2, score2, punishment1)
                DrawBoard(1, thesecondone1, hold1, score1, punishment2)
            else:
                if player_1_win :
                    WinnerAnimationFunish(1)
                elif player_2_win:
                    WinnerAnimationFunish(2)
                else:
                    if score1 > score2:
                        WinnerAnimationFunish(1)
                    elif score2 > score1:
                        WinnerAnimationFunish(2)
                    else:
                        WinnerAnimationFunish(0) 
            
            continue
        if pause == True:
            countdown = showtime
            continue
        if showtime < 10:
            timer_board(FONTCOLOR = RED)
        #draw on the AllBlock
        i = 0
        while len(trial_1) > 0:
            if trial_1[i] == 'Q' :
                #pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            elif trial_1[i] == 'L' :
                MoveLeftSide(1, droppingblock1)
                moveleft1 = True
                moveright1 = False
                lastMoveSidewaysTime1 = time.time() 
                trial_1 = trial_1[1:]
                break
            elif trial_1[i] == 'R':
                MoveRightSide(1, droppingblock1)
                lastMoveSidewaysTime1 = time.time()
                moveright1 = True
                moveleft1 = False
                trial_1 = trial_1[1:]
                break
            elif trial_1[i] == 'U':
                #rotation
                rotate1 = True
                if not canRotate(1, droppingblock1):
                    if droppingblock1.rotationstate == 0:
                        droppingblock1.rotationstate = droppingblock1.rotationtype() - 1
                    else:
                        droppingblock1.rotationstate -= 1
                lastRotateTime1 = time.time()
                trial_1 = trial_1[1:]
                break
            elif trial_1[i] == 'D':
                MoveDownSide(1, droppingblock1, Allblocks1)
                movedown1 = True
                lastMoveDownTime1 = time.time()
                trial_1 = trial_1[1:]
                break
                #accelerate the speed
            elif trial_1[i] == 'S':
                space1 = True
                MoveDownDirectly(1, droppingblock1, Allblocks1)

                for location in range(len(droppingblock1.position())):
                    rowlocation = droppingblock1.position()[location][1]
                    columnlocation = droppingblock1.position()[location][0]
                    Allblocks1[rowlocation+AboveLine][columnlocation].state = '1'        
                    Allblocks1[rowlocation+AboveLine][columnlocation].color = droppingblock1.color

                #print('Allblocks1')
                #print( [[Allblocks1[j][i].state for i in range(10)] for j in range(-AboveLine,20)])


                if droppingblock1.color == WHITE:
                    Punishing(droppingblock1, Allblocks1)

                lastdrop1 = time.time()
                #print('Allblocks1')
                #print( [[Allblocks1[j][i].state for i in range(10)] for j in range(-AboveLine,20)])
                number, CompleteRow = FindCompleteRow(1, Allblocks1)
                completerow = CompleteRow[:]
                if len(completerow) > 0:
                    last_score1 = score1
                    last_punishment1 = punishment1

                score1 += len(completerow)

                punishmentscoring(number, completerow) 
                EliminateRowBlocks((number, CompleteRow))

                #print('Allblocks1')
                #print( [[Allblocks1[j][i].state for i in range(10)] for j in range(-AboveLine,20)])
                thechoice = random.choice(['I','J','L','O', 'S', 'T', 'Z'])
                thechoice = all_the_choice1[0]
                all_the_choice1 = all_the_choice1[1:]
                count1 += 1
                print('count1', count1)
                thefirsttwochoice1 = thefirsttwochoice1[1:]+[thechoice]
                thefirstone1 = thefirsttwochoice1[0]
                thesecondone1 = thefirsttwochoice1[1]
                droppingblock1 = Tetris(thefirstone1)

                if PunishmentExecution(2) == True:
                    droppingblock1.color = WHITE
                    last_punishment2 = punishment2
                    DrawBoard(1, thesecondone1, hold1, score1, last_punishment2, PUNISHCOLOR = BACK_GROUND_COLOR)
                    punishment2 -= 15
                if len(completerow) > 0:
                    DrawBoard(2, thesecondone2, hold2, score2, last_punishment1, PUNISHCOLOR = BACK_GROUND_COLOR)
                    DrawBoard(1, thesecondone1, hold1, last_score1, punishment2, SCORECOLOR = BACK_GROUND_COLOR)
                DrawBoard(2, thesecondone2, hold2, score2, punishment1)
                DrawBoard(1, thesecondone1, hold1, score1, punishment2)    
                while topmost(droppingblock1) < 0:
                    droppingblock1.center[1] +=1
                if option_check(droppingblock1, Allblocks1) == False:
                    print('gameover, player 2 wins!')
                    for i in range(10):
                        Game_Over_Animation(Allblocks1)
                        DrawBoard(1,thesecondone1, hold1, score1, punishment2)
                        DrawBoard(2,thesecondone2, hold2, score2, punishment1)
                        pygame.time.delay(100)

                    WinnerAnimation(2, False)
                    player_2_win = True
                    gameover = True
                    perform = True
                    break
                else: 
                    trial_1 = computer(droppingblock1, Allblocks1)[0]
                    print('trial_1:',trial_1)

                    print('next =', thesecondone1)
                    if hold1 == None:
                        print('hold =', hold1)
                    else:
                        print('hold =', hold1.shape)
                    record1 = False
                    print('score =', score1)
                    #just move to the bottom without animation
                    droppingblock1.center[0] = 4
                    break
            elif trial_1[i] == 'START':
                trial_1 = trial_1[1:]
                break
            elif trial_1[i] == 'SHIFT':
                trial_1 = trial_1[1:]
                rightshift1 = True
                break

        if gameover == True:
            continue
        if pause == True:
            countdown = showtime
            continue
        if showtime < 10:
            timer_board(FONTCOLOR = RED)

        i = 0  
        while len(trial_2) > 0:
            if trial_2[i] == 'Q' :
                #pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            elif trial_2[i] == 'L' :
                MoveLeftSide(2, droppingblock2)
                moveleft2 = True
                moveright2 = False
                lastMoveSidewaysTime2 = time.time() 
                trial_2 = trial_2[1:]
                break
            elif trial_2[i] == 'R':
                MoveRightSide(2, droppingblock2)
                lastMoveSidewaysTime2 = time.time()
                moveright2 = True
                moveleft2 = False
                trial_2 = trial_2[1:]
                break
            elif trial_2[i] == 'U':
                #rotation
                rotate2 = True
                if not canRotate(2, droppingblock2):
                    if droppingblock2.rotationstate == 0:
                        droppingblock2.rotationstate = droppingblock2.rotationtype() - 1
                    else:
                        droppingblock2.rotationstate -= 1
                lastRotateTime2 = time.time()
                trial_2 = trial_2[1:]
                break
            elif trial_2[i] == 'D':
                MoveDownSide(2, droppingblock2, Allblocks2)
                movedown2 = True
                lastMoveDownTime2 = time.time()
                trial_2 = trial_2[1:]
                break
                #accelerate the speed
            elif trial_2[i] == 'S':
                space2 = True
                MoveDownDirectly(2, droppingblock2,  Allblocks2)

                for location in range(len(droppingblock2.position())):
                    rowlocation = droppingblock2.position()[location][1]
                    columnlocation = droppingblock2.position()[location][0]
                    Allblocks2[rowlocation+AboveLine][columnlocation].state = '1'        
                    Allblocks2[rowlocation+AboveLine][columnlocation].color = droppingblock2.color
                #print('Allblocks2')
                #print( [[Allblocks2[j][i].state for i in range(10)] for j in range(-AboveLine,20)])


                if droppingblock2.color == WHITE:
                    Punishing(droppingblock2, Allblocks2)
                lastdrop2 = time.time()    
                #print('Allblocks2')
                #print( [[Allblocks2[j][i].state for i in range(10)] for j in range(-AboveLine,20)])
                number, CompleteRow = FindCompleteRow(2, Allblocks2)
                completerow = CompleteRow[:]
                if len(completerow) > 0:
                    last_score2 = score2
                    last_punishment2 = punishment2
                score2 += len(completerow)

                punishmentscoring(number, completerow) 
                EliminateRowBlocks((number, CompleteRow))

                #print('Allblocks2')
                #print( [[Allblocks2[j][i].state for i in range(10)] for j in range(-AboveLine,20)])
                thechoice = random.choice(['I','J','L','O', 'S', 'T', 'Z'])
                thechoice = all_the_choice2[0]
                all_the_choice2 = all_the_choice2[1:]
                count2 += 1
                print('count2', count2)
                thefirsttwochoice2 = thefirsttwochoice2[1:]+[thechoice]
                thefirstone2 = thefirsttwochoice2[0]
                thesecondone2 = thefirsttwochoice2[1]
                droppingblock2 = Tetris(thefirstone2)
                record2 = False

                if PunishmentExecution(1) == True:
                    droppingblock2.color = WHITE
                    last_punishment1 = punishment1
                    DrawBoard(2, thesecondone2, hold2, score2, last_punishment1, PUNISHCOLOR = BACK_GROUND_COLOR)
                    punishment1 -= 15
                if len(completerow) > 0:
                    DrawBoard(2, thesecondone2, hold2, last_score2, punishment1, SCORECOLOR = BACK_GROUND_COLOR)
                    DrawBoard(1, thesecondone1, hold1, score1, last_punishment2, PUNISHCOLOR = BACK_GROUND_COLOR)
                DrawBoard(2, thesecondone2, hold2, score2, punishment1)
                DrawBoard(1, thesecondone1, hold1, score1, punishment2) 
                if hold2 == None:
                    droppingblock_2 = Tetris(thesecondone2)
                else:
                    droppingblock_2 = hold2
                droppingblock_2.center[0] = 4
                droppingblock_2.center[1] = 0

                while topmost(droppingblock2) < 0:
                    droppingblock2.center[1] +=1  

                while topmost(droppingblock_2) < 0:
                    droppingblock_2.center[1] +=1

                if option_check(droppingblock2, Allblocks2):   
                    if option_check(droppingblock_2, Allblocks2):
                        _unhold = computer(droppingblock2, Allblocks2)
                        _hold = computer(droppingblock_2, Allblocks2)
                        trial_2 = thefinaltrial(_unhold, _hold)
                        if 'SHIFT' in trial_2:
                            #trial_2 = ['START'] + trial_2
                            print('trial_2:', trial_2)
                            break
                    else:
                        trial_2 = computer(droppingblock2, Allblocks2)[0]
                else:
                    if option_check(droppingblock_2, Allblocks2) == True:
                        trial_2 = computer(droppingblock_2, Allblocks2)[0]
                        trial_2.insert(1, 'SHIFT')
                        #trial_2 = ['START'] + trial_2
                        print('trial_2:', trial_2)
                        break
                    else:
                        print('gameover, player 1 wins!')
                        for i in range(10):
                            Game_Over_Animation(Allblocks2)
                            DrawBoard(1,thesecondone1, hold1, score1, punishment2)
                            DrawBoard(2,thesecondone2, hold2, score2, punishment1)
                            pygame.time.delay(100)
                        WinnerAnimation(1, False)
                        player_1_win = True
                        perform = True
                        gameover = True
                        break
                print('trial_2:',trial_2)
                print('next2 =', thesecondone2)
                if hold2 == None:
                    print('hold2 =', hold2)
                else:
                    print('hold2 =', hold2.shape)

                print('score2 =', score2)
                #just move to the bottom without animation
                #trial_2 = trial_2[1:]
                droppingblock2.center[0] = 4
                break
            elif trial_2[i] == 'START':
                trial_2 = trial_2[1:]
                break
            elif trial_2[i] == 'SHIFT':
                trial_2 = trial_2[1:]
                rightshift2 = True
                break

        if gameover == True:
            continue
        if pause == True:
            countdown = showtime
            continue
        if showtime < 10:
            timer_board(FONTCOLOR = RED)

        if rightshift2 == True:
            if hold2 == None: 
                test = Tetris(thefirsttwochoice2[1])
                test.center = droppingblock2.center
                print('hold')
                if holdtest(2, test, droppingblock2)==True:
                    hold2 = droppingblock2
                    fixedpoint2 = hold2.center
                    thechoice = random.choice(['I','J','L','O', 'S', 'T', 'Z'])
                    thechoice = all_the_choice2[0]
                    all_the_choice2 = all_the_choice2[1:]
                    thefirsttwochoice2 = thefirsttwochoice2[1:]+[thechoice]
                    thefirstone2 = thefirsttwochoice2[0]
                    thesecondone2 = thefirsttwochoice2[1]
                    droppingblock2 = Tetris(thefirstone2)
                    droppingblock2.center = fixedpoint2
                    print('next2 =', thesecondone2)
                    print('hold2 =', hold2.shape)
                    print('score2 =', score2)
                    rightshift2 = False
                    record2 = True
            else:
                print('hold')
                if holdtest(2, hold2, droppingblock2)==True:
                    fixedpoint2 = droppingblock2.center
                    hold2, droppingblock2 = droppingblock2, hold2
                    droppingblock2.center = fixedpoint2
                    rightshift2 = False
                    record2 = True
                else:
                    rightshift2 = False
                    record2 = True
                    print('hold2 error')
                print('next2 =', thesecondone2)
                print('hold2 =', hold2.shape)
                print('score2 =', score2)



        if rightshift1 == True:
            if hold1 == None:
                test = Tetris(thefirsttwochoice1[1])
                test.center = droppingblock1.center
                if holdtest(1, test, droppingblock1)==True:
                    print('hold')
                    hold1 = droppingblock1
                    fixedpoint1 = hold1.center
                    thechoice = random.choice(['I','J','L','O', 'S', 'T', 'Z'])
                    thefirsttwochoice1 = thefirsttwochoice1[1:]+[thechoice]
                    thefirstone1 = thefirsttwochoice1[0]
                    thesecondone1 = thefirsttwochoice1[1]
                    droppingblock1 = Tetris(thefirstone1)
                    droppingblock1.center = fixedpoint1
                    print('next1 =', thesecondone1)
                    print('hold1 =', hold1.shape)
                    print('score1 =', score1)
                    rightshift1 = False
                    record1 = True
            else:
                print('hold')
                if holdtest(1, hold1, droppingblock1)==True:
                    fixedpoint1 = droppingblock1.center
                    hold1, droppingblock1 = droppingblock1, hold1
                    droppingblock1.center = fixedpoint1
                    rightshift1 = False
                    record1 = True
                else:
                    print('hold1 error')
                print('next1 =', thesecondone1)
                print('hold1 =', hold1.shape)
                print('score1 =', score1)

            '''
        if (moveleft2 or moveright2) and time.time() - lastMoveSidewaysTime2 > movesidewayfrequency:
            if moveleft2:
                MoveLeftSide(2, droppingblock2)
            elif moveright2:
                MoveRightSide(2, droppingblock2)
            lastMoveSidewaysTime2 = time.time()

        if movedown2 and time.time() - lastMoveDownTime2 > movedownfrequency :
            MoveDownSide(2, droppingblock2, Allblocks2)
            lastMoveDownTime2 = time.time()

        if rotate2 and time.time() - lastRotateTime2 > rotatefrequency :
            print('yes')
            if not canRotate(2, droppingblock2):
                if droppingblock2.rotationstate == 0:
                    droppingblock2.rotationstate = droppingblock2.rotationtype() - 1
                else:
                    droppingblock2.rotationstate -= 1
            lastRotateTime2 = time.time()   
            '''
            '''

        if (moveleft1 or moveright1) and time.time() - lastMoveSidewaysTime1 > movesidewayfrequency:
            if moveleft1:
                MoveLeftSide(1, droppingblock1)
            elif moveright2:
                MoveRightSide(1, droppingblock1)
            lastMoveSidewaysTime1 = time.time()

        if movedown1 and time.time() - lastMoveDownTime1 > movedownfrequency :
            MoveDownSide(1, droppingblock1)
            lastMoveDownTime1 = time.time()
            '''
            '''
        if rotate1 and time.time() - lastRotateTime1 > rotatefrequency :
            if not canRotate(1, droppingblock1):
                if droppingblock1.rotationstate == 0:
                    droppingblock1.rotationstate = droppingblock1.rotationtype() - 1
                else:
                    droppingblock1.rotationstate -= 1
            lastRotateTime1 = time.time()    
          '''
        print('droppingblock1', droppingblock1.position())
        print('droppingblock2', droppingblock2.position())
        for location in range(len(droppingblock1.position())):
            rowlocation = droppingblock1.position()[location][1]
            columnlocation = droppingblock1.position()[location][0]
            Allblocks1[rowlocation+AboveLine][columnlocation].state = '1'        
            Allblocks1[rowlocation+AboveLine][columnlocation].color = droppingblock1.color
        for location in range(len(droppingblock2.position())):
            rowlocation = droppingblock2.position()[location][1]
            columnlocation = droppingblock2.position()[location][0]
            Allblocks2[rowlocation+AboveLine][columnlocation].state = '1'        
            Allblocks2[rowlocation+AboveLine][columnlocation].color = droppingblock2.color


        DrawBoard(1, thesecondone1, hold1, score1, punishment2)
        DrawBoard(2, thesecondone2, hold2, score2, punishment1)
        #print('Allblocks1')
       # print([[Allblocks1[j][i].state for i in range(10)] for j in range(-AboveLine,20)])
        #print('Allblocks2')
        #print([[Allblocks2[j][i].state for i in range(10)] for j in range(-AboveLine,20)])
        #check if the dropping block is descended to the bottom
        if canDrop(1, droppingblock1, Allblocks1) == False:

            if time.time() - lastdrop1 > 0.5 :
                if droppingblock1.color == WHITE:
                        Punishing(droppingblock1, Allblocks1)

                number, CompleteRow = FindCompleteRow(1, Allblocks1)
                completerow = CompleteRow[:]
                if len(completerow) > 0:
                    last_score1 = score1
                    last_punishment1 = punishment1

                score1 += len(completerow)

                punishmentscoring(number, completerow) 
                EliminateRowBlocks((number, CompleteRow))

                #print('Allblocks1')
                #print( [[Allblocks1[j][i].state for i in range(10)] for j in range(-AboveLine,20)])
                thechoice = random.choice(['I','J','L','O', 'S', 'T', 'Z'])
                thechoice = all_the_choice1[0]
                all_the_choice1 = all_the_choice1[1:]
                count1 += 1
                print('count1', count1)
                thefirsttwochoice1 = thefirsttwochoice1[1:]+[thechoice]
                thefirstone1 = thefirsttwochoice1[0]
                thesecondone1 = thefirsttwochoice1[1]
                droppingblock1 = Tetris(thefirstone1)

                if PunishmentExecution(2) == True:
                    droppingblock1.color = WHITE
                    last_punishment2 = punishment2
                    DrawBoard(1, thesecondone1, hold1, score1, last_punishment2, PUNISHCOLOR = BACK_GROUND_COLOR)
                    punishment2 -= 15
                if len(completerow) > 0:
                    DrawBoard(2, thesecondone2, hold2, score2, last_punishment1, PUNISHCOLOR = BACK_GROUND_COLOR)
                    DrawBoard(1, thesecondone1, hold1, last_score1, punishment2, SCORECOLOR = BACK_GROUND_COLOR)
                DrawBoard(2, thesecondone2, hold2, score2, punishment1)
                DrawBoard(1, thesecondone1, hold1, score1, punishment2) 
                while topmost(droppingblock1) < 0:
                    droppingblock1.center[1] +=1
                if option_check(droppingblock1, Allblocks1) == False:
                    print('gameover, player 2 wins!')
                    for i in range(10):
                        Game_Over_Animation(Allblocks1)
                        DrawBoard(1,thesecondone1, hold1, score1, punishment2)
                        DrawBoard(2,thesecondone2, hold2, score2, punishment1)
                        pygame.time.delay(100)
                    player_2_win = True    
                    WinnerAnimation(2, False)
                    perform = True
                    gameover = True

                trial_1 = computer(droppingblock1, Allblocks1)[0]
                count1 += 1
                print('count1:', count1)
                droppingblock1.center[0] = 4

                print('next =', thesecondone1)
                if hold1 == None:
                    print('hold =', hold1)
                else:
                    print('hold =', hold1.shape)
                record1 = False
                print('score =', score1)
            # change to the new one
            else:
                for location in range(len(droppingblock1.position())):
                    rowlocation = droppingblock1.position()[location][1]
                    columnlocation = droppingblock1.position()[location][0]
                    Allblocks1[rowlocation+AboveLine][columnlocation].state = '0'        
                    Allblocks1[rowlocation+AboveLine][columnlocation].color = BACK_GROUND_COLOR
        else:

            for location in range(len(droppingblock1.position())):
                rowlocation = droppingblock1.position()[location][1]
                columnlocation = droppingblock1.position()[location][0]
                Allblocks1[rowlocation+AboveLine][columnlocation].state = '0'        
                Allblocks1[rowlocation+AboveLine][columnlocation].color = BACK_GROUND_COLOR
            if lastdrop1 == None:
                Drop(1, droppingblock1, Allblocks1)
                lastdrop1 = time.time()
            else:
                if time.time() - lastdrop1 > 0.5:
                    Drop(1, droppingblock1, Allblocks1)
                    lastdrop1 = time.time() 

        if gameover == True:
            continue
        if pause == True:
            countdown = showtime
            continue
        if showtime < 10:
            timer_board(FONTCOLOR = RED)
        if canDrop(2, droppingblock2, Allblocks2) == False:

            if time.time() - lastdrop2 > 0.5 :
                if droppingblock2.color == WHITE:
                    Punishing(droppingblock2, Allblocks2)

                number, CompleteRow = FindCompleteRow(2, Allblocks2)
                completerow = CompleteRow[:]
                if len(completerow) > 0:
                    last_score2 = score2
                    last_punishment2 = punishment2
                score2 += len(completerow)

                punishmentscoring(number, completerow) 
                EliminateRowBlocks((number, CompleteRow))

                #print('Allblocks2')
                #print( [[Allblocks2[j][i].state for i in range(10)] for j in range(-AboveLine,20)])
                thechoice = random.choice(['I','J','L','O', 'S', 'T', 'Z'])
                thechoice = all_the_choice2[0]
                all_the_choice2 = all_the_choice2[1:]
                count2 += 1
                print('count2', count2)
                thefirsttwochoice2 = thefirsttwochoice2[1:]+[thechoice]
                thefirstone2 = thefirsttwochoice2[0]
                thesecondone2 = thefirsttwochoice2[1]
                droppingblock2 = Tetris(thefirstone2)
                record2 = False

                if PunishmentExecution(1) == True:
                    droppingblock2.color = WHITE
                    last_punishment1 = punishment1
                    DrawBoard(2, thesecondone2, hold2, score2, last_punishment1, PUNISHCOLOR = BACK_GROUND_COLOR)
                    punishment1 -= 15
                if len(completerow) > 0:
                    DrawBoard(2, thesecondone2, hold2, last_score2, punishment1, SCORECOLOR = BACK_GROUND_COLOR)
                    DrawBoard(1, thesecondone1, hold1, score1, last_punishment2, PUNISHCOLOR = BACK_GROUND_COLOR)
                DrawBoard(2, thesecondone2, hold2, score2, punishment1)
                DrawBoard(1, thesecondone1, hold1, score1, punishment2) 
                if hold2 == None:
                    droppingblock_2 = Tetris(thesecondone2)
                else:
                    droppingblock_2 = hold2

                while topmost(droppingblock2) < 0:
                    droppingblock2.center[1] +=1  

                while topmost(droppingblock_2) < 0:
                    droppingblock_2.center[1] +=1
                droppingblock_2.center[0] = 4
                droppingblock_2.center[1] = 0
                record2  = False 
                if option_check(droppingblock2, Allblocks2):   
                    if option_check(droppingblock_2, Allblocks2):
                        _unhold = computer(droppingblock2, Allblocks2)
                        _hold = computer(droppingblock_2, Allblocks2)
                        trial_2 = thefinaltrial(_unhold, _hold)
                        if 'SHIFT' in trial_2:
                            #trial_2 = ['START'] + trial_2
                            print('trial_2:', trial_2)

                    else:
                        trial_2 = computer(droppingblock2, Allblocks2)[0]
                else:
                    if option_check(droppingblock_2, Allblocks2) == True:
                        trial_2 = computer(droppingblock_2, Allblocks2)[0]
                        trial_2.insert(1, 'SHIFT')
                        #trial_2 = ['START'] + trial_2
                        print('trial_2:', trial_2)

                    else:
                        for i in range(10):
                            Game_Over_Animation(Allblocks2)
                            DrawBoard(1,thesecondone1, hold1, score1, punishment2)
                            DrawBoard(2,thesecondone2, hold2, score2, punishment1)
                            pygame.time.delay(100)

                        WinnerAnimation(1, False)
                        perform = True
                        gameover = True
                        player_1_win = True
                        print('gameover, player 1 wins!')
                        
                droppingblock_2.center[0] = 4
                droppingblock2.center[0] = 4
                print('trial_2:',trial_2)
                print('next2 =', thesecondone2)
                if hold2 == None:
                    print('hold2 =', hold2)
                else:
                    print('hold2 =', hold2.shape)
                print('score2 =', score2)
            # change to the new one
            else:
                for location in range(len(droppingblock2.position())):
                    rowlocation = droppingblock2.position()[location][1]
                    columnlocation = droppingblock2.position()[location][0]
                    Allblocks2[rowlocation+AboveLine][columnlocation].state = '0'        
                    Allblocks2[rowlocation+AboveLine][columnlocation].color = BACK_GROUND_COLOR 
        else:

            for location in range(len(droppingblock2.position())):
                rowlocation = droppingblock2.position()[location][1]
                columnlocation = droppingblock2.position()[location][0]
                Allblocks2[rowlocation+AboveLine][columnlocation].state = '0'        
                Allblocks2[rowlocation+AboveLine][columnlocation].color = BACK_GROUND_COLOR
            if lastdrop2 == None:
                Drop(2, droppingblock2, Allblocks2)
                lastdrop2 = time.time()
            else:
                if time.time() - lastdrop2 > 0.5:
                    Drop(2, droppingblock2, Allblocks2)
                    lastdrop2 = time.time()

        pygame.display.update()

        FPSCLOCK.tick(FPS)

def holdtest(number, hold, droppingblock):# diff: we need to rely on the input number to decide which board we should run 
    check = hold
    check.center = droppingblock.center   
    while topmost(check) < 0:
        check.center[1] +=1
    checkposition = check.position()
    print(checkposition)
    if number == 1:
        Allblocks = Allblocks1
    else:
        Allblocks = Allblocks2
    for i in range(len(checkposition)):
        if checkposition[i][0] > 9 or checkposition[i][0] < 0:
            return False
        elif checkposition[i][1] > 19:
            return False
        elif Allblocks[checkposition[i][1]+AboveLine][checkposition[i][0]].state == '1':
            return False
    return True       
def timer_board(FONTCOLOR = WHITE, BACKCOLOR = BACK_GROUND_COLOR, TEXT_FONT = 40):
    global showtime

    fontObj = pygame.font.Font('freesansbold.ttf', TEXT_FONT)
    textSurfaceObjTime = fontObj.render(str(showtime + 1), True, BACKCOLOR,BACKCOLOR)
    textRectObjTime = textSurfaceObjTime.get_rect()
    textRectObjTime.center = (WINDOWWIDTH/2,40)
    DISPLAYSURF.blit(textSurfaceObjTime, textRectObjTime)

    fontObj = pygame.font.Font('freesansbold.ttf', TEXT_FONT)
    textSurfaceObjTime = fontObj.render(str(showtime), True, FONTCOLOR,BACKCOLOR)
    textRectObjTime = textSurfaceObjTime.get_rect()
    textRectObjTime.center = (WINDOWWIDTH/2,40)
    DISPLAYSURF.blit(textSurfaceObjTime, textRectObjTime)


    pygame.display.update()
#Redraw the game board
'''DIDN'T DRAW y<0'''
def DrawBoard(number, thesecondone, hold, score, punishment, SCORECOLOR = WHITE, PUNISHCOLOR = WHITE, BACKCOLOR = BACK_GROUND_COLOR, TEXT_FONT = 35):
    global BLOCK_GAP, BOARDWIDTH, BOARD_SPACE, BOARD_UP, RECT_BOARD1, RECT_BOARD2, BLOCK_SIZE
    if number == 1:
        Allblocks = Allblocks1
        Coord_centerx = BOARD_SPACE + BOARDWIDTH + 30 
        Coord_centery = BOARD_UP + 40
    else:
        Allblocks = Allblocks2
        Coord_centerx = (BOARD_SPACE + BOARDWIDTH)*2 + 30
        Coord_centery = BOARD_UP + 40
    for raw_index in range(AboveLine,len(Allblocks)):
        for block in Allblocks[raw_index]:
            if number == 1:
                pygame.draw.rect(DISPLAYSURF, block.color, block.rect1)
            else:
                pygame.draw.rect(DISPLAYSURF, block.color, block.rect2)

    if hold:
        if number == 1:
            pygame.draw.rect(DISPLAYSURF, BACK_GROUND_COLOR, (BOARD_SPACE-4*BLOCK_SIZE-6, BOARD_UP, 4*BLOCK_SIZE, 4*BLOCK_SIZE))

            DISPLAYSURF.blit(image[hold.shape], (BOARD_SPACE-4*BLOCK_SIZE-6, BOARD_UP))
        else:
            pygame.draw.rect(DISPLAYSURF, BACK_GROUND_COLOR, (BOARD_SPACE*2+BOARDWIDTH-4*BLOCK_SIZE-6, BOARD_UP, 4*BLOCK_SIZE, 4*BLOCK_SIZE))


            DISPLAYSURF.blit(image[hold.shape], (BOARD_SPACE*2+BOARDWIDTH-4*BLOCK_SIZE-6, BOARD_UP))


    #next block
    if number == 1:
        pygame.draw.rect(DISPLAYSURF, BACK_GROUND_COLOR, (BOARD_SPACE+BOARDWIDTH+6, BOARD_UP, 4*BLOCK_SIZE, 4*BLOCK_SIZE))
        DISPLAYSURF.blit(image[thesecondone], (BOARD_SPACE+BOARDWIDTH+6, BOARD_UP))
    else:
        pygame.draw.rect(DISPLAYSURF, BACK_GROUND_COLOR, (BOARD_SPACE*2+BOARDWIDTH*2+6, BOARD_UP, 4*BLOCK_SIZE, 4*BLOCK_SIZE))
        DISPLAYSURF.blit(image[thesecondone], (BOARD_SPACE*2+BOARDWIDTH*2+6, BOARD_UP))

    fontObj = pygame.font.Font('freesansbold.ttf', TEXT_FONT)

    textSurfaceObj3 = fontObj.render(f'score:', True, WHITE,BACKCOLOR)
    textRectObj3 = textSurfaceObj3.get_rect()
    textRectObj3.center = (Coord_centerx + 45,Coord_centery + 160)
    DISPLAYSURF.blit(textSurfaceObj3, textRectObj3)

    textSurfaceObj3_1 = fontObj.render(f'{score}', True, SCORECOLOR,BACKCOLOR)
    textRectObj3_1 = textSurfaceObj3_1.get_rect()
    textRectObj3_1.topleft = textRectObj3.topright
    DISPLAYSURF.blit(textSurfaceObj3_1, textRectObj3_1)

    textSurfaceObj4 = fontObj.render(f'punish:', True, WHITE,BACKCOLOR)
    textRectObj4 = textSurfaceObj4.get_rect()
    textRectObj4.center = (Coord_centerx + 55,Coord_centery + 200)
    DISPLAYSURF.blit(textSurfaceObj4, textRectObj4)

    textSurfaceObj4_1 = fontObj.render(f'{punishment}', True, PUNISHCOLOR,BACKCOLOR)
    textRectObj4_1 = textSurfaceObj4_1.get_rect()
    textRectObj4_1.topleft = textRectObj4.topright
    DISPLAYSURF.blit(textSurfaceObj4_1, textRectObj4_1)

    textSurfaceObj5 = fontObj.render(f'HOLD', True, WHITE,BACKCOLOR)
    textRectObj5 = textSurfaceObj5.get_rect()
    textRectObj5.center = (BOARD_SPACE - 2 * BLOCK_SIZE - 6 , Coord_centery + 120)
    DISPLAYSURF.blit(textSurfaceObj5, textRectObj5)
    textRectObj5.center = (BOARD_SPACE * 2  +  BOARDWIDTH - 2 * BLOCK_SIZE - 3 , Coord_centery + 120)
    DISPLAYSURF.blit(textSurfaceObj5, textRectObj5)
    
    textSurfaceObj6 = fontObj.render(f'NEXT', True, WHITE,BACKCOLOR)
    textRectObj6 = textSurfaceObj6.get_rect()
    textRectObj6.center = (BOARD_SPACE + BOARDWIDTH + 2 * BLOCK_SIZE + 6 , Coord_centery + 120)
    DISPLAYSURF.blit(textSurfaceObj6, textRectObj6)
    textRectObj6.center = (BOARD_SPACE * 2 + BOARDWIDTH * 2 + 2 * BLOCK_SIZE + 9  , Coord_centery + 120)
    DISPLAYSURF.blit(textSurfaceObj6, textRectObj6)
    pygame.display.update()

#DISPLAY_TIME == 0 means it won't be removed 

def StartGameAnimation():
    pygame.draw.rect(DISPLAYSURF, RED, (BOARD_SPACE-3, BOARD_UP-3, BOARDWIDTH+6, BOARDHEIGHT+6),3)
    pygame.draw.rect(DISPLAYSURF, RED, ((BOARD_SPACE * 2 + BOARDWIDTH-3), BOARD_UP-3, BOARDWIDTH+6, BOARDHEIGHT+6),3)
    
    #next
    pygame.draw.rect(DISPLAYSURF, RED, (BOARD_SPACE+BOARDWIDTH+3, BOARD_UP-3, 4*BLOCK_SIZE+6, 4*BLOCK_SIZE+6),3)
    pygame.draw.rect(DISPLAYSURF, RED, (BOARD_SPACE*2+BOARDWIDTH*2+3, BOARD_UP-3, 4*BLOCK_SIZE+6, 4*BLOCK_SIZE+6),3)
    
    #hold
    pygame.draw.rect(DISPLAYSURF, RED, (BOARD_SPACE-4*BLOCK_SIZE-9, BOARD_UP-3, 4*BLOCK_SIZE+6, 4*BLOCK_SIZE+6),3)
    pygame.draw.rect(DISPLAYSURF, RED, (BOARD_SPACE*2+BOARDWIDTH-4*BLOCK_SIZE-9, BOARD_UP-3, 4*BLOCK_SIZE+6, 4*BLOCK_SIZE+6),3)
    
    TEXT_Animation(RECT_BOARD1.centerx, RECT_BOARD1.centery, RECT_BOARD2.centerx, RECT_BOARD2.centery, 'READY', DISPLAY_TIME=2000)
    TEXT_Animation(RECT_BOARD1.centerx, RECT_BOARD1.centery, RECT_BOARD2.centerx, RECT_BOARD2.centery, '3', DISPLAY_TIME=1000)
    TEXT_Animation(RECT_BOARD1.centerx, RECT_BOARD1.centery, RECT_BOARD2.centerx, RECT_BOARD2.centery, '2', DISPLAY_TIME=1000)
    TEXT_Animation(RECT_BOARD1.centerx, RECT_BOARD1.centery, RECT_BOARD2.centerx, RECT_BOARD2.centery, '1', DISPLAY_TIME=1000)

def TEXT_Animation(Coord_centerx1, Coord_centery1, Coord_centerx2, Coord_centery2, TEXTmsg, TEXT_FONT = 32, FRONTCOLOR = RED, BACKCOLOR = BACK_GROUND_COLOR, DISPLAY_TIME = 0):

    fontObj = pygame.font.Font('freesansbold.ttf', TEXT_FONT)
    textSurfaceObj = fontObj.render(TEXTmsg, True, FRONTCOLOR,BACKCOLOR)
    textRectObj1 = textSurfaceObj.get_rect()
    textRectObj1.center = (Coord_centerx1,Coord_centery1)
    textRectObj2= textSurfaceObj.get_rect()
    textRectObj2.center = (Coord_centerx2,Coord_centery2)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj1)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj2)
    pygame.display.update()

    if DISPLAY_TIME != 0:
        pygame.time.delay(DISPLAY_TIME)
        pygame.draw.rect(DISPLAYSURF, BACK_GROUND_COLOR, textRectObj1)
        pygame.draw.rect(DISPLAYSURF, BACK_GROUND_COLOR, textRectObj2)
        pygame.display.update()

#return a list with complete row(index by its coordinate.y)
#empty list means there isn't any complete row 
def FindCompleteRow(number, Allblocks):# diff: we need to rely on the input number to decide which board we should run

    CompleteRow = []
    for row_index in range(len(Allblocks)):
        state_one_count = 0
        for block in Allblocks[row_index]:
            if block.state == '1':
                state_one_count += 1
        if state_one_count == len(Allblocks[row_index]):
            CompleteRow.append(row_index)

    #print(CompleteRow)
    return number, CompleteRow
#eliminate complete row blocks and drop the upper blocks
def Simulate_FindCompleteRow(number, Allblocksign):

    CompleteRow = []
    for row_index in range(len(Allblocksign)):
        state_one_count = 0
        for block in Allblocksign[row_index]:
            if block == '1':
                state_one_count += 1
        if state_one_count == len(Allblocksign[row_index]):
            CompleteRow.append(row_index)

    #print(CompleteRow)
    return number, CompleteRow

def EliminateRowBlocks(numberCompleteRow):
    number = numberCompleteRow[0]
    CompleteRow = numberCompleteRow[1]
    if number == 1:
        Allblocks = Allblocks1
    else:
        Allblocks = Allblocks2
    count = 0
    def BlocksDropInRow(number,finish_row):
        #let every block in row 's color and state copy the upper one
        if number == 1:
            Allblocks = Allblocks1
        else:
            Allblocks = Allblocks2
        for row_index in range(finish_row,0,-1):
            for block_index in range(len(Allblocks[row_index])):
                Allblocks[row_index][block_index].color = Allblocks[row_index-1][block_index].color
                Allblocks[row_index][block_index].state = Allblocks[row_index-1][block_index].state
        #let raw0 be state0 and backgroundcolor
        for block in Allblocks[0]:
            block.clear() 

    while len(CompleteRow) != 0 :
        #eliminate the most bottom row
        for block in Allblocks[max(CompleteRow) + count]:
            block.clear()
        #let upper blocks drop
        BlocksDropInRow(number, max(CompleteRow)+count)
        CompleteRow.remove(max(CompleteRow))
        count += 1
        #print(memory2)
    pygame.display.update()
def punishmentscoring(number, CompleteRow):
    global memory1, memory2, punishment1, punishment2
    print(CompleteRow)
    print(memory2)
    if number == 1:
        punishment = punishment1
        memory = memory1
    else:
        punishment = punishment2
        memory = memory2
    if len(CompleteRow)== 1:
        punishment += 1
    elif len(CompleteRow) == 2 :
        punishment += 3
    elif len(CompleteRow) == 3 :
        punishment += 6
    elif len(CompleteRow) == 4 :
        punishment += 10
    if len(CompleteRow) != 0:
        if len(memory) > 0:
            count = 1
            i = -1
            while len(memory[i]) != 0 :
                punishment += count
                count+=1
                i -= 1
                if i < -len(memory):
                    break
    memory.append(CompleteRow)
    if number == 1:
        punishment1 = punishment
        memory1 = memory
    else:
        punishment2 = punishment
        memory2 = memory

    #print(memory2)
def PunishmentExecution(number):
    global punishment1, punishment2
    if number == 1:
        punishment = punishment1
    else:
        punishment = punishment2
    if punishment >= 15:

        return True
    else:
        return False
def Punishing(InputTetris, Allblocks):
    emptyarea = surrounding(InputTetris)
    #print(emptyarea)
    for i in range(len(emptyarea)):
        if Allblocks[emptyarea[i][1]+AboveLine][emptyarea[i][0]].state == '1' :
            Allblocks[emptyarea[i][1]+AboveLine][emptyarea[i][0]].state = '0'

        if Allblocks[emptyarea[i][1]+AboveLine][emptyarea[i][0]].color != BACK_GROUND_COLOR :
            Allblocks[emptyarea[i][1]+AboveLine][emptyarea[i][0]].color = BACK_GROUND_COLOR
def Simulate_Punishing(InputTetris, Allblocksign):
    emptyarea = surrounding(InputTetris)
    #print(emptyarea)
    for i in range(len(emptyarea)):
        if Allblocksign[emptyarea[i][1]+AboveLine][emptyarea[i][0]] == '1' :
            Allblocksign[emptyarea[i][1]+AboveLine][emptyarea[i][0]] = '0'

def surrounding(InputTetris):
    check = InputTetris.position()
    empty = set()
    substract = set()
    for i in range(len(check)):
        if check[i][0] > 0:
            empty.add((check[i][0]-1, check[i][1]))
        if check[i][0] < 9:
            empty.add((check[i][0]+1, check[i][1]))
        if check[i][1] > 0:
            empty.add((check[i][0], check[i][1]-1))
        if check[i][1] < 19:
            empty.add((check[i][0], check[i][1]+1))
        substract.add((check[i][0], check[i][1]))
    empty -= substract
    empty2 = []
    for i in empty:
        empty2.append(i)
    empty3 = []
    for i in range(len(empty2)):
        empty3.append([empty2[i][0], empty2[i][1]])
    return empty3
def option_check(InputTetris, Allblocks):
    check = InputTetris.position()
    print('mark', check)
    for i in range(len(check)):
        if Allblocks[check[i][1]][check[i][0]].state == '1':
            return False
    return True
def computer(InputTetris, Allblocks):
    global WHITE
    SimulateTetris = InputTetris
    SimulateAllblocks = Allblocks
    SimulateAllblocksign = [[Allblocks[j][i].state for i in range(10)] for j in range(20 + AboveLine)]
    SimulateTetris.center[1] = 0
    SimulateTetris.center[0] = 4
    while topmost(SimulateTetris) < 0:
        SimulateTetris.center[1] += 1
    keep_y = SimulateTetris.center[1]
    keep_x = SimulateTetris.center[0]
    record_left = False
    record_right = False
    competitionlist = {}
    _all = []
    count = 0
    while count <= SimulateTetris.rotationtype() - 1:
        _trials = []
        _leftmost = SimulateTetris.center[0] - leftmost(SimulateTetris)
        _rightmost = -(rightmost(SimulateTetris) - SimulateTetris.center[0]) + 10
        spare = []

        for j in range(_leftmost, _rightmost):
            SimulateTetris.center[0] = j
            SimulateTetris.center[1] = keep_y
            move = j - keep_x
            spare.append(move) # to test the number of steps 
            #SimulateAllblocks = Allblocks
            SimulateAllblocksign = [[SimulateAllblocks[j][i].state for i in range(10)] for j in range(20 + AboveLine)]
            SimulateColumnSign = AllColumnSign(SimulateAllblocksign)
            #print(SimulateColumnSign)

            #print(check)
            if option_check(SimulateTetris, SimulateAllblocks) == False:
                _trials.append(-200000)
                if j < 4:
                    record_left = True
                elif j > 4:
                    record_right = True
                continue
            else:            
                while canDrop(1, SimulateTetris, SimulateAllblocks) == True:
                    SimulateTetris.center[1] += 1
                check = SimulateTetris.position()
                for location in range(len(check)):
                    rowlocation = check[location][1]
                    columnlocation = check[location][0]
                    SimulateAllblocks[rowlocation+AboveLine][columnlocation].state = '1'
                    SimulateAllblocksign[rowlocation+AboveLine][columnlocation] = '1'

                SimulateColumnSign = AllColumnSign(SimulateAllblocksign) 
                #keep1 = SimulateAllblocks
                #keep2 = SimulateAllblocksign
                #keep3 = SimulateColumnSign
                #print(SimulateColumnSign)
                if SimulateTetris.color == WHITE:
                    #print('pass')
                    Simulate_Punishing(SimulateTetris, SimulateAllblocksign)
                    SimulateColumnSign = AllColumnSign(SimulateAllblocksign)
                    #print(SimulateColumnSign)
                else:
                    SimulateColumnSign = AllColumnSign(SimulateAllblocksign)
                #print(SimulateColumnSign)

                value = evaluate(SimulateAllblocksign, SimulateColumnSign, SimulateTetris)
                #print(value)
                _trials.append(value)

                #SimulateAllblocks = keep1
                #SimulateAllblocksign = keep2
                #SimulateColumnSign = keep3
                for location in range(len(check)):
                    rowlocation = check[location][1]
                    columnlocation = check[location][0]
                    SimulateAllblocks[rowlocation+AboveLine][columnlocation].state = '0'
                    SimulateAllblocksign[rowlocation+AboveLine][columnlocation] = '0'


                #print(SimulateColumnSign)    
                SimulateTetris.center[1] = keep_y
                SimulateTetris.center[0] = keep_x

        correction = list(range(_leftmost, _rightmost))
        center = correction.index(4)
        if record_left:
            left_trial = _trials[:center]
            left_trial.reverse()
            locate_200000 = left_trial.index(-200000)
            for i in range(locate_200000, len(left_trial)):
                left_trial[i] = -200000
            left_trial.reverse()
            _trials[:center] = left_trial
            record_left = False
        if record_right:
            right_trial = _trials[center + 1:]
            locate_200000 = right_trial.index(-200000)
            for i in range(locate_200000, len(right_trial)):
                right_trial[i] = -200000
            _trials[center + 1:] = right_trial
            record_right = False
        #print(spare)
        _all.append(max(_trials))
        location = champions(_trials, max(_trials)) 
        #print(location)#1,3,7  in _trials
        secondround = []
        for i in range(len(location)):
            secondround.append(abs(spare[location[i]])) #3,1,3
        location2 = champions(secondround, min(secondround)) # find the location 2
        decide = random.choice(location2)
        #print(decide)
        the_step = ['START'] + ['U'] * count
        the_input = spare[location[decide]]
        if the_input < 0:
            the_step += ['L'] * abs(the_input)
        else:
            the_step += ['R'] * the_input
        competitionlist[count] = the_step
        #print(the_step)
        count += 1
        if InputTetris.shape != 'O':
            if SimulateTetris.rotationstate != SimulateTetris.rotationtype() - 1:
                SimulateTetris.rotationstate += 1
                #print(SimulateTetris.rotationstate, '---')
        print('-----')

    #print(competitionlist)       
    finallocation = champions(_all, max(_all))
    #print(finallocation)
    if len(finallocation) >= 2 :
        finalround = []
        finalroundwork = []
        for i in range(len(finallocation)):
            finalroundwork.append(competitionlist[finallocation[i]])
            finalround.append(len(competitionlist[finallocation[i]]))
        ultimate = champions(finalround, min(finalround))
        #print(finalround)
        #print(finalroundwork)
        decide2 = random.choice(ultimate)
        the_work = finalroundwork[decide2] + ['S'] 
        InputTetris.rotationstate = 0
        return [the_work, max(_all)]
    else:
        the_work = competitionlist[finallocation[0]] +  ['S']  
        InputTetris.rotationstate = 0
        return [the_work, max(_all)]

def thefinaltrial(unhold, hold):
    if unhold[1] >= hold[1]:
        return unhold[0]
    else:
        result = hold[0]
        result.insert(1, 'SHIFT')
        return result
def champions(lists, number):
    if lists.count(number) == 1:
        return [lists.index(number)]
    else:
        location = []
        count = 0
        index = 0
        while count < lists.count(number):
            location.append(lists.index(number, index))
            index = lists.index(number, index) + 1
            count += 1
        return location
def LandingHeight(InputTetris, column):
    locate = istop(InputTetris)
    reset = []
    for i in range(len(locate)):
        if locate[i][1] == topmost(InputTetris):
            reset.append(locate[i])
    where = reset[0][0]
    #print(where)
    i = 0
    while i < len(column[where]):
        if column[where][i] == '1':
            count = 20 - i
            break
        else:
            i += 1
    return count - 0.5 * len(isleft(InputTetris))
def ErodedPieceCellsMetric(InputTetris, Allblocksign):
    find = Simulate_FindCompleteRow(1, Allblocksign)
    check = InputTetris.position()
    count = 0
    for i in range(len(check)):
        if check[i][1] in find[1] :
            count += 1
    return len(find[1]) * count
def RowTransitions(Allblocks):
    count = 0
    for i in range(len(Allblocks)):
        for j in range(len(Allblocks[i])-1):
            if Allblocks[i][j] != Allblocks[i][j+1]:
                count += 1
    return count
def ColumnTransitions(column):
    count = 0
    for i in range(len(column)):
        for j in range(len(column[i])-1):
            if column[i][j] != column[i][j+1]:
                count += 1
    return count
def BoardBuriedHoles(column):
    counter = 0
    for j in range(len(column)):
        i = 0
        while i < len(column[j]):
            if column[j][i] == '1':
                break
            else:
                i += 1       
        for k in range(i, len(column[j])):
            if column[j][k] == '0':
                counter += 1
    return counter
def BoardWells(column):
    count = 0
    for j in range(len(column)):
        if j == 0:
            empty = []
            for i in range(len(column[j])):
                if column[j][i] == '0' and column[j+1][i] == '1':
                    empty.append(i)
            count += BoardWellsCount(empty)
        if j == len(column) - 1:
            empty = []
            for i in range(len(column[j])):
                if column[j][i] == '0' and column[j-1][i] == '1':
                    empty.append(i)
            count += BoardWellsCount(empty)
        else:
            empty = []
            for i in range(len(column[j])):
                if column[j][i] == '0' and column[j-1][i] == '1' and column[j+1][i] == '1':
                    empty.append(i)
            count += BoardWellsCount(empty)
    return count
def BoardWellsCount(lists):
    total = 0
    record = []
    for i in range(len(lists)):
        if lists[i] in record:
            continue
        total += 1
        count = 1
        while lists[i] + 1 in lists:
            count += 1
            total += count
            record.append(lists[i] + 1)
            if i != len(lists) - 1:
                i += 1          
            else:
                break
    return total
def evaluate(Allblocksign, ColumnSign, InputTetris):
    #print(ColumnSign)
    #print('L', LandingHeight(InputTetris, ColumnSign))
    #print('E', ErodedPieceCellsMetric(InputTetris, Allblocksign))
    #print('R', RowTransitions(Allblocksign))
    #print('C', ColumnTransitions(ColumnSign) )
    #print('BB', BoardBuriedHoles(ColumnSign))
    #print('BW', BoardWells(ColumnSign))
    return LandingHeight(InputTetris, ColumnSign) * -45 + ErodedPieceCellsMetric(InputTetris, Allblocksign) * 34 - RowTransitions(Allblocksign) * 32 - ColumnTransitions(ColumnSign) * 93 - 79 * BoardBuriedHoles(ColumnSign) - 34 * BoardWells(ColumnSign)
#LandingHeight(InputTetris, ColumnSign) * -45 + ErodedPieceCellsMetric(InputTetris, Allblocksign) * 34 - RowTransitions(Allblocksign) * 32 - ColumnTransitions(ColumnSign) * 93 - 79 * BoardBuriedHoles(ColumnSign) - 34 * BoardWells(ColumnSign)
def Game_Over_Animation(Allblocks):
    for row in Allblocks:
        for block in row:
            t = list(block.color)
            for i in range(len(t)):
                if t[i] > 10:
                    t[i] -= 10
            block.color = tuple(t)
#timeup means if it is ended by time is 0
def WinnerAnimation(winner, timeup):
    winnertext={1:'You Win!', 2:'You Lose!', 0:'Tie!'}
    if winner == 1:
        loser = 2
    elif winner == 2:
        loser = 1
    else:
        loser = 0
    if timeup:
        TEXT_Animation(RECT_BOARD1.centerx, RECT_BOARD1.centery, RECT_BOARD2.centerx, RECT_BOARD2.centery, "Time's up", DISPLAY_TIME=2000)
        TEXT_Animation(RECT_BOARD1.centerx, RECT_BOARD1.centery, RECT_BOARD1.centerx, RECT_BOARD1.centery, winnertext[winner])
        TEXT_Animation(RECT_BOARD2.centerx, RECT_BOARD2.centery, RECT_BOARD2.centerx, RECT_BOARD2.centery, winnertext[loser]) 
    else:
        TEXT_Animation(RECT_BOARD1.centerx, RECT_BOARD1.centery, RECT_BOARD2.centerx, RECT_BOARD2.centery, 'GAME OVER', DISPLAY_TIME=2000)
        TEXT_Animation(RECT_BOARD1.centerx, RECT_BOARD1.centery, RECT_BOARD1.centerx, RECT_BOARD1.centery, winnertext[winner])
        TEXT_Animation(RECT_BOARD2.centerx, RECT_BOARD2.centery, RECT_BOARD2.centerx, RECT_BOARD2.centery, winnertext[loser])                    
def WinnerAnimationFunish(winner):
    winnertext={1:'You Win!', 2:'You Lose!', 0:'Tie!'}
    if winner == 1:
        loser = 2
    elif winner == 2:
        loser = 1
    else:
        loser = 0
    TEXT_Animation(RECT_BOARD1.centerx, RECT_BOARD1.centery, RECT_BOARD1.centerx, RECT_BOARD1.centery, winnertext[winner])
    TEXT_Animation(RECT_BOARD2.centerx, RECT_BOARD2.centery, RECT_BOARD2.centerx, RECT_BOARD2.centery, winnertext[loser]) 
    

if __name__=='__main__':
    main()

