import pygame, sys, random, time
from pygame.locals import *
FPS=10
WINDOWWIDTH = 600
WINDOWHEIGHT = 800
BLOCK_SPACE = 1

BOARDWIDTH = 300 + 9 * BLOCK_SPACE
BOARDHEIGHT = 600 +19 * BLOCK_SPACE
BOARD_LEFT = (WINDOWWIDTH - BOARDWIDTH)/2
BOARD_UP = (WINDOWHEIGHT - BOARDHEIGHT)/2
RECT_BOARD = pygame.Rect(BOARD_LEFT, BOARD_UP, BOARDWIDTH, BOARDHEIGHT)


BLOCK_SIZE =(BOARDWIDTH - 9 * BLOCK_SPACE) / 10

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
rotatefrequency = 0.15
class BLOCK:
    def __init__(self, x, y, color = BACK_GROUND_COLOR ):
        self.x = x 
        self.y = y
        self.state = '0'
        self.color = BACK_GROUND_COLOR
        self.left = BOARD_LEFT + self.x * (BLOCK_SIZE + BLOCK_SPACE)
        self.up = BOARD_UP + self.y * (BLOCK_SIZE + BLOCK_SPACE)
        self.rect = (self.left, self.up, BLOCK_SIZE, BLOCK_SIZE)
    def clear(self):
        self.state = '0'
        self.color = BACK_GROUND_COLOR
    def __str__(self):
        return f'[{self.x}, {self.y}]'
AboveLine = 0       
        
Allblocks=[[BLOCK(i,j) for i in range(10)] for j in range(-AboveLine,20)]
Allblocksign = [[Allblocks[j][i].state for i in range(10)] for j in range(20 + AboveLine)]
#[[[0, 0], [1, 0],..., [9, 0]][[0, 1],...[9, 1]]...]
def AllColumnSign(Allblocksign): # transfer the row to the column
    empty2 = []
    for j in range(len(Allblocksign[0])):
        empty = []
        for i in range(len(Allblocksign)):
            empty.append(Allblocksign[i][j])
        empty2.append(empty)
    return empty2
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
            search = {0:
        [[self.centerx(),self.centery()],
        [self.centerx()+1,self.centery()],
        [self.centerx(),self.centery()+1],
        [self.centerx()+1,self.centery()+1]]
            }
            return search[self.rotationstate]
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
def canRotate(InputTetris):
    if InputTetris.shape == 'O':
        return True
    else:
        InputTetris.rotationstate = (InputTetris.rotationstate + 1) % InputTetris.rotationtype()
        check = InputTetris.position()

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
                            InputTetris.center[0] -=1 #try again
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
def canDrop(InputTetris, Allblocks): #diff: Since we need to create a simulated board, the board used in the function should be specifed.
        check = InputTetris.position()
        for i in range(len(check)):
            if check[i][1] >= 19:
                return False
            elif check[i] in isbottom(InputTetris):
                if Allblocks[check[i][1]+AboveLine+1][check[i][0]].state == '1':
                    return False
        return True    
def MoveDownSide(InputTetris, Allblocks):#diff: Since we need to create a simulated board, the board used in the function should be specifed.
    check = InputTetris.position()
    
    if canDrop(InputTetris, Allblocks):
        InputTetris.center[1] +=1 
def Drop(InputTetris, Allblocks):#diff: Since we need to create a simulated board, the board used in the function should be specifed.

    if canDrop(InputTetris, Allblocks):
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
def canMoveLeftside(InputTetris):
    check = InputTetris.position()
    
    for i in range(len(check)):
        if check[i][0] <= 0:
            return False
        elif check[i] in isleft(InputTetris):
            if Allblocks[check[i][1]+AboveLine][check[i][0]-1].state == '1':
                return False        
    return True
def MoveLeftSide(InputTetris):
    
    if canMoveLeftside(InputTetris):
        InputTetris.center[0] -= 1
def isright(InputTetris):
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
def canMoveRightside(InputTetris):
    check = InputTetris.position()
    
    for i in range(len(check)):
        if check[i][0] >= 9:
            return False
        elif check[i] in isright(InputTetris):
            if Allblocks[check[i][1]+AboveLine][check[i][0]+1].state == '1':
                return False 
    return True
def MoveRightSide(InputTetris):
    
    if canMoveRightside(InputTetris):
        InputTetris.center[0]+= 1
def MoveDownDirectly(InputTetris, Allblocks): #diff: Since we need to create a simulated board, the board used in the function should be specifed.
    
    while canDrop(InputTetris, Allblocks) == True:
        InputTetris.center[1] +=1
        
#'I','J','L','O', 'S', 'T', 'Z'
def main():
    global DISPLAYSURF, Allblocks, score
    pygame.init()
    score = 0
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Tetris')
    
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYSURF.fill(BACK_GROUND_COLOR)
    #Openingscreen()
    #DrawBoard()
    # if 'single' is pressed:
    StartGameAnimation()
    DrawBoard()
    '''
    if random.randint(0, 1) == 0:
        pygame.mixer.music.load('tetrisb.mid')
    else:
        pygame.mixer.music.load('tetrisc.mid')
    pygame.mixer.music.play(-1, 0.0)
     '''
    thefirsttwochoice = [random.choice(['I','J','L','O', 'S', 'T', 'Z']), random.choice(['I','J','L','O', 'S', 'T', 'Z'])]
    thefirstone = thefirsttwochoice[0] 
    thesecondone = thefirsttwochoice[1]
    droppingblock = Tetris(thefirstone)
    print('next =', thesecondone)
    hold = None
    print('hold =', hold)
    print('score =', score)
    record = False
    lastdrop = None
    pause = False
    moveleft = False
    moveright = False
    movedown = False
    space = False
    rightshift = False
    sound = True
    rotate = False
    lastMoveSidewaysTime = time.time()
    lastRotateTime = time.time()
    lastMoveDownTime = time.time()
    trial = computer(droppingblock, Allblocks)    
    print('trial:', trial)
    while topmost(droppingblock) < 0:
        droppingblock.center[1] +=1
    while True:
        i = 0
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        while len(trial) > 0:
            # When QUIT or press the esc key, quit the game
            '''
            if event == KEYUP:
                if event.key ==K_p:
                    if pause == False:
                        pause = True
                        
                        pygame.mixer.music.stop()
                         
                        #pause
                    else:
                        pause = False
                        
                        pygame.mixer.music.play(-1, 0.0)
                        
                elif event.key == K_SPACE:
                    space = False
                elif event.key == K_LEFT:
                    moveleft = False
                elif event.key == K_RIGHT:
                    moveright = False
                elif event.key == K_UP:
                    rotate = False
                elif event.key == K_DOWN:
                    movedown = False
                elif event.key == K_ESCAPE:
                   # pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                elif event.key == K_RSHIFT:
                    rightshift = False
                    
                elif event.key == K_m:
                    if sound == True:
                        pygame.mixer.music.stop()
                        sound = False
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                        sound = True
                        
            elif pause == True:
                break
                '''
            if trial[i] == 'Q' :
                #pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            elif trial[i] == 'L' :
                MoveLeftSide(droppingblock)
                moveleft = True
                moveright = False
                lastMoveSidewaysTime = time.time() 
                trial = trial[1:]
                break
            elif trial[i] == 'R':
                MoveRightSide(droppingblock)
                lastMoveSidewaysTime = time.time()
                moveright = True
                moveleft = False
                trial = trial[1:]
                break
            elif trial[i] == 'U':
                #rotation
                rotate = True
                if not canRotate(droppingblock):
                    if droppingblock.rotationstate == 0:
                        droppingblock.rotationstate = droppingblock.rotationtype() - 1
                    else:
                        droppingblock.rotationstate -= 1
                lastRotateTime = time.time()
                trial = trial[1:]
                break
            elif trial[i] == 'D':
                MoveDownSide(droppingblock, Allblocks)
                movedown = True
                lastMoveDownTime = time.time()
                trial = trial[1:]
                break
                #accelerate the speed
            elif trial[i] == 'S':
                space = True
                MoveDownDirectly(droppingblock, Allblocks)

                for location in range(len(droppingblock.position())):
                    rowlocation = droppingblock.position()[location][1]
                    columnlocation = droppingblock.position()[location][0]
                    Allblocks[rowlocation+AboveLine][columnlocation].state = '1'        
                    Allblocks[rowlocation+AboveLine][columnlocation].color = droppingblock.color
                
                DrawBoard()
                Completeblocks = FindCompleteRow(Allblocks)
                completeblocks = Completeblocks[:]
                score += len(Completeblocks)
                EliminateRowBlocks(completeblocks)
                thechoice = random.choice(['I','J','L','O', 'S', 'T', 'Z'])
                thefirsttwochoice = thefirsttwochoice[1:]+[thechoice]
                thefirstone = thefirsttwochoice[0]
                thesecondone = thefirsttwochoice[1]
                droppingblock = Tetris(thefirstone)
                trial = computer(droppingblock, Allblocks)
                print('trial:',trial)
                while topmost(droppingblock) < 0:
                    droppingblock.center[1] +=1
                print('next =', thesecondone)
                if hold == None:
                    print('hold =', hold)
                else:
                    print('hold =', hold.shape)
                record = False
                print('score =', score)
                '''
                check = droppingblock.position()
                for i in range(len(check)):
                    if Allblocks[check[i][1]+AboveLine][check[i][0]].state == '1' :
                        gameoveranimation()
                        pygame.mixer.music.stop()
                        pygame.quit()
                        sys.exit()
                        '''
                #just move to the bottom without animation
                #trial = trial[1:]
                break
            elif trial[i] == 'START':
                trial = trial[1:]
                break
                '''
            elif event.key == K_RSHIFT:
                if record == False:
                    rightshift = True
                    
        if pause == True:
            continue
            '''
        #draw on the AllBlock
        if rightshift == True:
            if hold == None:
                test = Tetris(thefirsttwochoice[1])
                test.center = droppingblock.center
                if holdtest(test, droppingblock) == True:
                    print('hold')
                    hold = droppingblock
                    fixedpoint = hold.center
                    thechoice = random.choice(['I','J','L','O', 'S', 'T', 'Z'])
                    thefirsttwochoice = thefirsttwochoice[1:]+[thechoice]
                    thefirstone = thefirsttwochoice[0]
                    thesecondone = thefirsttwochoice[1]
                    droppingblock = Tetris(thefirstone)
                    droppingblock.center = fixedpoint
                    print('next =', thesecondone)
                    print('hold =', hold.shape)
                    print('score =', score)
                    rightshift = False
                    record = True
            else:
                print('hold')
                if holdtest(hold, droppingblock) == True:
                    fixedpoint = droppingblock.center
                    hold, droppingblock = droppingblock, hold
                    droppingblock.center = fixedpoint
                    rightshift = False
                    record = True
                else:
                    print('hold error')
                print('next =', thesecondone)
                print('hold =', hold.shape)
                print('score =', score)
            '''
        if (moveleft or moveright) and time.time() - lastMoveSidewaysTime > movesidewayfrequency:
            if moveleft:
                MoveLeftSide(droppingblock)
            elif moveright:
                MoveRightSide(droppingblock)
            lastMoveSidewaysTime = time.time()
            
        if movedown and time.time() - lastMoveDownTime > movedownfrequency :
            MoveDownSide(droppingblock, Allblocks)
            lastMoveDownTime = time.time()

        if rotate and time.time() - lastRotateTime > rotatefrequency :
            if not canRotate(droppingblock):
                if droppingblock.rotationstate == 0:
                    droppingblock.rotationstate = droppingblock.rotationtype() - 1
                else:
                    droppingblock.rotationstate -= 1
            lastRotateTime = time.time()
            '''
        for location in range(len(droppingblock.position())):
            rowlocation = droppingblock.position()[location][1]
            columnlocation = droppingblock.position()[location][0]
            Allblocks[rowlocation+AboveLine][columnlocation].state = '1'        
            Allblocks[rowlocation+AboveLine][columnlocation].color = droppingblock.color
        
        DrawBoard()
        #check if the dropping block is descended to the bottom
        if canDrop(droppingblock, Allblocks) == False:
            
            if time.time() - lastdrop > 0.5 :
                Completeblocks = FindCompleteRow(Allblocks)
                completeblocks = Completeblocks[:]
                score += len(Completeblocks)
                EliminateRowBlocks(completeblocks)
                
                thechoice = random.choice(['I','J','L','O', 'S', 'T', 'Z'])
                thefirsttwochoice = thefirsttwochoice[1:]+[thechoice]
                thefirstone = thefirsttwochoice[0]
                thesecondone = thefirsttwochoice[1]
                droppingblock = Tetris(thefirstone)
                trial = computer(droppingblock, Allblocks)
                while topmost(droppingblock) < 0:
                    droppingblock.center[1] +=1
                print('next =', thesecondone)
                if hold == None:
                    print('hold =', hold)
                else:
                    print('hold =', hold.shape)
                record = False
                print('score =', score)
            # change to the new one
            else:
                for location in range(len(droppingblock.position())):
                    rowlocation = droppingblock.position()[location][1]
                    columnlocation = droppingblock.position()[location][0]
                    Allblocks[rowlocation+AboveLine][columnlocation].state = '0'        
                    Allblocks[rowlocation+AboveLine][columnlocation].color = BACK_GROUND_COLOR 
        else:
            
            for location in range(len(droppingblock.position())):
                rowlocation = droppingblock.position()[location][1]
                columnlocation = droppingblock.position()[location][0]
                Allblocks[rowlocation+AboveLine][columnlocation].state = '0'        
                Allblocks[rowlocation+AboveLine][columnlocation].color = BACK_GROUND_COLOR
            if lastdrop == None:
                Drop(droppingblock, Allblocks)
                lastdrop = time.time()
            else:
                if time.time() - lastdrop > 0.5:
                    Drop(droppingblock, Allblocks)
                    lastdrop = time.time()
        pygame.display.update()
       
        FPSCLOCK.tick(FPS)
    #elif 'double' is pressed:    
def holdtest(hold, droppingblock):  
    check = hold
    check.center = droppingblock.center
    checkposition = check.position()
    for i in range(len(checkposition)):
        if checkposition[i][0] > 9 or checkposition[i][0] < 0:
            return False
        elif checkposition[i][1] > 19:
            return False
        elif Allblocks[checkposition[i][1]+AboveLine][checkposition[i][0]].state == '1':
            return False
    return True
#Redraw the game board
'''DIDN'T DRAW y<0'''       
def DrawBoard():
    for raw_index in range(AboveLine,len(Allblocks)):
        for block in Allblocks[raw_index]:
            pygame.draw.rect(DISPLAYSURF, block.color, block.rect)
            pygame.display.update()
#DISPLAY_TIME == 0 means it won't be removed 
def StartGameAnimation():
    pygame.draw.rect(DISPLAYSURF, RED, (BOARD_LEFT-3, BOARD_UP-3, BOARDWIDTH+6, BOARDHEIGHT+6),3)
    TEXT_Animation(RECT_BOARD.centerx, RECT_BOARD.centery, 'READY', DISPLAY_TIME=2000)
    TEXT_Animation(RECT_BOARD.centerx, RECT_BOARD.centery, '3', DISPLAY_TIME=1000)
    TEXT_Animation(RECT_BOARD.centerx, RECT_BOARD.centery, '2', DISPLAY_TIME=1000)
    TEXT_Animation(RECT_BOARD.centerx, RECT_BOARD.centery, '1', DISPLAY_TIME=1000)

def TEXT_Animation(Coord_centerx, Coord_centery, TEXTmsg, TEXT_FONT = 32, FRONTCOLOR = RED, BACKCOLOR = BACK_GROUND_COLOR, DISPLAY_TIME = 0):
    
    fontObj = pygame.font.Font('freesansbold.ttf', TEXT_FONT)
    textSurfaceObj = fontObj.render(TEXTmsg, True, FRONTCOLOR,BACKCOLOR)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (Coord_centerx,Coord_centery)
    
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    pygame.display.update()
    
    if DISPLAY_TIME != 0:
        pygame.time.delay(DISPLAY_TIME)
        pygame.draw.rect(DISPLAYSURF, BACK_GROUND_COLOR, textRectObj)
        pygame.display.update()
        
#return a list with complete row(index by its coordinate.y)
#empty list means there isn't any complete row 
def FindCompleteRow(Allblocks):#diff: Since we need to create a simulated board, the board used in the function should be specifed.
    
    CompleteRow = []
    for row_index in range(len(Allblocks)):
        state_one_count = 0
        for block in Allblocks[row_index]:
            if block.state == '1':
                state_one_count += 1
        if state_one_count == len(Allblocks[row_index]):
            CompleteRow.append(row_index)      
    return CompleteRow
#eliminate complete row blocks and drop the upper blocks

def EliminateRowBlocks(CompleteRow):
    count = 0
    def BlocksDropInRow(finish_row):
        #let every block in row 's color and state copy the upper one
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
        BlocksDropInRow(max(CompleteRow)+count)
        CompleteRow.remove(max(CompleteRow))
        count += 1
    
    pygame.display.update()
def computer(InputTetris, Allblocks):
    a_1 = time.time()
    SimulateTetris = InputTetris
    SimulateAllblocks = Allblocks
    SimulateAllblocksign = [[Allblocks[j][i].state for i in range(10)] for j in range(20 + AboveLine)]
    keep_y = SimulateTetris.center[1]
    keep_x = SimulateTetris.center[0]
    #print('warn,', SimulateTetris.rotationstate)
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
            move = j - keep_x
            spare.append(move) # to test the number of steps 
            while canDrop(SimulateTetris, SimulateAllblocks) == True:
                SimulateTetris.center[1] += 1
            check = SimulateTetris.position()
            for location in range(len(check)):
                rowlocation = check[location][1]
                columnlocation = check[location][0]
                SimulateAllblocks[rowlocation+AboveLine][columnlocation].state = '1'
                SimulateAllblocksign[rowlocation+AboveLine][columnlocation] = '1'
            
            SimulateColumnSign = AllColumnSign(SimulateAllblocksign) 
            #print(check)
            value = evaluate(SimulateAllblocks, SimulateAllblocksign, SimulateColumnSign, SimulateTetris)
            print(value)
            _trials.append(value)
            for location in range(len(check)):
                rowlocation = check[location][1]
                columnlocation = check[location][0]
                SimulateAllblocks[rowlocation+AboveLine][columnlocation].state = '0'
                SimulateAllblocksign[rowlocation+AboveLine][columnlocation] = '0'
            SimulateTetris.center[1] = keep_y
            SimulateTetris.center[0] = keep_x
        #print(_trials)
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
    a_2 = time.time()
    print('a_2 - a_1', a_2 - a_1)
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
        return the_work
    else:
        the_work = competitionlist[finallocation[0]] + ['S']
        InputTetris.rotationstate = 0
        return the_work
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
def ErodedPieceCellsMetric(InputTetris, Allblocks):
    find = FindCompleteRow(Allblocks)
    check = InputTetris.position()
    count = 0
    for i in range(len(check)):
        if check[i][1] in find :
            count += 1
    return len(find) * count
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
def evaluate(Allblocks, Allblocksign, ColumnSign, InputTetris):
    #print(ColumnSign)
    print('L', LandingHeight(InputTetris, ColumnSign))
    print('E', ErodedPieceCellsMetric(InputTetris, Allblocks))
    print('R', RowTransitions(Allblocksign))
    print('C', ColumnTransitions(ColumnSign) )
    print('BB', BoardBuriedHoles(ColumnSign))
    print('BW', BoardWells(ColumnSign))
    return LandingHeight(InputTetris, ColumnSign) * -45 + ErodedPieceCellsMetric(InputTetris, Allblocks) * 34 - RowTransitions(Allblocksign) * 32 - ColumnTransitions(ColumnSign) * 93 - 79 * BoardBuriedHoles(ColumnSign) - 34 * BoardWells(ColumnSign)
#value = -45 × landingHeight + 34 × erodedPieceCellsMetric - 32 × boardRowTransitions - 93 × boardColTransitions - (79 × boardBuriedHoles) - 34 × boardWells    
if __name__=='__main__':
    main()
