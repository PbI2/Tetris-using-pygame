import pygame, sys, random, time
from pygame.locals import *


FPS=30
WINDOWWIDTH = 750
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
##Allblocksign = [[Allblocks[j][i].state for i in range(10)] for j in range(20 + AboveLine)]
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
            self.rotationtype = 1
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



def istop(InputTetris): # a subfunction of the 'topmost' function
    check = InputTetris.position()
    i = 0
    while i < len(check): 
        if [check[i][0],check[i][1]-1] in check:
            check.remove([check[i][0],check[i][1]])
        else:
            i+=1

    return check
def topmost(InputTetris): # It is used to ensure that the dropping block would not appear on the screen until its y position > 0
    result = istop(InputTetris)
    empty = []
    for i in range(len(result)):
        empty.append(result[i][1])
    return min(empty)
def canRotate(InputTetris): # to simulate whether it is possible for the block to rotate
    if InputTetris.shape == 'O': # since the 'O' shape don't need to rotate
        return True
    else:
        InputTetris.rotationstate = (InputTetris.rotationstate + 1) % InputTetris.rotationtype() #let's change to the simulate state
        check = InputTetris.position()

        for i in range(len(check)):   
            if check[i][1] >= 20: # touch the bottom boundary 
                InputTetris.center[1] -= bottom(InputTetris) - 19 # to denote how many times the block should be lifted up
                check2 = InputTetris.position() # after lifting up the block, we need to detect whether the block position is suitable
                for i in range(len(check2)):
                    if Allblocks[check2[i][1]+AboveLine][check2[i][0]].state == '1' : # if the block collides with other blocks, which is forbidden
                        InputTetris.center[1] +=1 # back to the original state, and the rotation command is invalid
                        return False
            elif check[i][0] >= 10: # touch the right boundary
                InputTetris.center[0] -= rightmost(InputTetris) - 9 # to denote how many times the block should be moved left
                check2 = InputTetris.position()
                for i in range(len(check2)) :
                    if Allblocks[check2[i][1]+AboveLine][check2[i][0]].state == '1' : #touch other blocks
                        if InputTetris.shape == 'I': # the block 'I' case should be unique. Just consider this exclusive case for 'I' block:
                            InputTetris.center[0] -=1 # the rightmost block of the 'I' block overlaps with other blocks. As a result, we need to move left once again to fulfill this case. 
                            check3 = InputTetris.position() # all the cases are considered. Let's test whether the block position is suitable:
                            for i in range(len(check3)) : # we don't need to consider the case that the leftmost part of the 'I' block cross the left boundary, which is impossible.
                                if Allblocks[check3[i][1]+AboveLine][check3[i][0]].state == '1' : # if the block still touches other blocks 
                                    InputTetris.center[0] +=2 # back to the original state, and the rotation command is invalid 
                                    return False
                            return True
                        else: # for other blocks, which are not as complicated as the 'I' block is, 
                            InputTetris.center[0] +=1 #just back to the original state, invalidating the rotation command
                            return False
                return True
            elif check[i][0] < 0: # touch the left boundary. The rules are similar to the previous one. 
                InputTetris.center[0] += -leftmost(InputTetris) 
                check2 = InputTetris.position()
                for i in range(len(check2)):
                    if Allblocks[check2[i][1]+AboveLine][check2[i][0]].state == '1' :
                        if InputTetris.shape == 'I': 
                            InputTetris.center[0] +=1 
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
                if check[i] in isleft(InputTetris): # if other blocks collide with the 'left part' of the block:
                    InputTetris.center[0] +=1  # move right once
                    check2 = InputTetris.position() # check whether this modification is accepted:
                    for i in range(len(check2)) :
                        if check2[i][0] >= 10: #touch the right boundary
                            InputTetris.center[0] -=1
                            return False
                        elif Allblocks[check2[i][1]+AboveLine][check2[i][0]].state == '1' :
                            if InputTetris.shape == 'I': #consider the exclusive 'I' case: When the 'I' block is moved left once, it is still possible
                                InputTetris.center[0] +=1 # that the 'left part ' of the block still collides with other blocks. As a result, we need to
                                check3 = InputTetris.position() # move right again to include this case.
                                for i in range(len(check3)) :
                                    if check3[i][0] >= 10: # cross the right boundary, which is not allowed
                                        InputTetris.center[0] -=2
                                        return False
                                    elif Allblocks[check3[i][1]+AboveLine][check3[i][0]].state == '1' : # still collides with other blocks
                                        InputTetris.center[0] -=2
                                        return False
                            else: # for other blocks, just end the simulation and invalidate the rotation command
                                InputTetris.center[0] -=1
                                return False
                    return True
                elif check[i] in isright(InputTetris): # similar thoughts of the previous one
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
                else: # only 'I' block could possibly reach here, for other blocks collide with the inner part of the 'I' block
                    if check[i][0] < InputTetris.center[0]: #The position of the collision is on the left side of the center part of the 'I' block.
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

def isbottom(InputTetris): # the 'bottom part' of the block: the possible part of the block that could touch other blocks below it.
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
def bottom(InputTetris): # the bottom y location of the block
    result = isbottom(InputTetris)
    empty = []
    for i in range(len(result)):
        empty.append(result[i][1])
    return max(empty)
def canDrop(InputTetris):
        check = InputTetris.position()
        for i in range(len(check)):
            if check[i][1] >= 19: # if the block doesn't cross the bottom boundary
                return False
            elif check[i] in isbottom(InputTetris): # and doesn't touch any other block, 
                if Allblocks[check[i][1]+AboveLine+1][check[i][0]].state == '1':
                    return False
        return True    #then the block can drop
def MoveDownSide(InputTetris):
    check = InputTetris.position()

    if canDrop(InputTetris):
        InputTetris.center[1] +=1 
def Drop(InputTetris):

    if canDrop(InputTetris):
        InputTetris.center[1] +=1
# In fact, these two functions above are the same, just named differently for their intentions
def isleft(InputTetris):# the 'left part' of the block: the possible part of the block that could touch other blocks on the left side 
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
def leftmost(InputTetris): # the leftmost x location of the block
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
def MoveDownDirectly(InputTetris):

    while canDrop(InputTetris) == True:
        InputTetris.center[1] +=1

#'I','J','L','O', 'S', 'T', 'Z'
def main():
    global DISPLAYSURF, Allblocks, score, image
    pygame.init()
    score = 0
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Tetris')

    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYSURF.fill(BACK_GROUND_COLOR)
    image = {}
    for shape in ['I','J','L','O', 'S', 'T', 'Z']:
        image[shape] = pygame.image.load(f'image\Tetris{shape}.png')
        image[shape].convert()
    #Openingscreen()
    #DrawBoard()
    # if 'single' is pressed:
    StartGameAnimation()
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
    gameover = False
    moveleft = False
    moveright = False
    movedown = False
    space = False
    rightshift = False
    sound = True
    rotate = False
    level = 1
    lastMoveSidewaysTime = time.time()
    lastRotateTime = time.time()
    lastMoveDownTime = time.time()

    fallingspeed = 0.5
    if pause == False:
        DrawBoard(thesecondone, hold, score, level)
    return_to_page = False
    perform = False
    while topmost(droppingblock) < 0:
        droppingblock.center[1] +=1
    while True:

        for event in pygame.event.get():
            # When QUIT or press the esc key, quit the game
            if event.type == KEYUP:
                if event.key ==K_p:
                    if pause == False:

                        pause = True

                        Allblockscolor =[]
                        for row in Allblocks:

                            rowcolor=[]
                            for block in row:
                                rowcolor.append(block.color)   
                            Allblockscolor.append(rowcolor)

                        for row in Allblocks:
                            for block in row:
                                block.color = BACK_GROUND_COLOR

                        DrawBoard(thesecondone, hold, score, level)
                        TEXT_Animation(RECT_BOARD.centerx, RECT_BOARD.centery, 'PAUSE', DISPLAY_TIME=0)


                        '''
                        pygame.mixer.music.stop()
                         '''
                        #pause
                    else:
                        pause = False
                        TEXT_Animation(RECT_BOARD.centerx, RECT_BOARD.centery, 'PAUSE',FRONTCOLOR = BACK_GROUND_COLOR, DISPLAY_TIME=0)
                        for row in Allblocks:
                            for block in row:
                                block.color = Allblockscolor[block.y][block.x]

                        DrawBoard(thesecondone, hold, score, level)


                        '''
                        pygame.mixer.music.play(-1, 0.0)
                        '''
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
                    #sys.exit()
                    return_to_page = True
                    break
                elif event.key == K_RSHIFT:
                    rightshift = False
                    '''
                elif event.key == K_m:
                    if sound == True:
                        pygame.mixer.music.stop()
                        sound = False
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                        sound = True
                        '''
            elif pause == True:


                break

            elif event.type == QUIT :
                #pygame.mixer.music.stop()
                pygame.quit()
                #sys.exit()
                return_to_page = True
                break
            elif event.type == KEYDOWN:
                if event.key == K_LEFT :
                    MoveLeftSide(droppingblock)
                    moveleft = True
                    moveright = False
                    lastMoveSidewaysTime = time.time() 
                elif event.key == K_RIGHT:
                    MoveRightSide(droppingblock)
                    lastMoveSidewaysTime = time.time()
                    moveright = True
                    moveleft = False
                elif event.key == K_UP:
                    #rotation
                    rotate = True
                    if not canRotate(droppingblock):
                        if droppingblock.rotationstate == 0:
                            droppingblock.rotationstate = droppingblock.rotationtype() - 1
                        else:
                            droppingblock.rotationstate -= 1
                    lastRotateTime = time.time()       
                elif event.key == K_DOWN:
                    MoveDownSide(droppingblock)
                    movedown = True
                    lastMoveDownTime = time.time()
                    #accelerate the speed
                elif event.key == K_SPACE:
                    space = True
                    MoveDownDirectly(droppingblock)

                    for location in range(len(droppingblock.position())):
                        rowlocation = droppingblock.position()[location][1]
                        columnlocation = droppingblock.position()[location][0]
                        Allblocks[rowlocation+AboveLine][columnlocation].state = '1'        
                        Allblocks[rowlocation+AboveLine][columnlocation].color = droppingblock.color

                    DrawBoard(thesecondone, hold, score, level)

                    CompleteRow = FindCompleteRow()
                    completerow = CompleteRow[:]
                    if len(completerow) > 0:
                        last_score = score

                    score += len(completerow)

                    EliminateRowBlocks(CompleteRow)
                    thechoice = random.choice(['I','J','L','O', 'S', 'T', 'Z'])
                    thefirsttwochoice = thefirsttwochoice[1:]+[thechoice]
                    thefirstone = thefirsttwochoice[0]
                    thesecondone = thefirsttwochoice[1]
                    droppingblock = Tetris(thefirstone)
                    while topmost(droppingblock) < 0:
                        droppingblock.center[1] +=1
                    if len(completerow) > 0:
                        DrawBoard(thesecondone, hold, last_score, level, SCORECOLOR = BACK_GROUND_COLOR)

                    DrawBoard(thesecondone, hold, score, level)
                    if option_check(droppingblock, Allblocks) == False:
                        gameover = True
                        break
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
                elif event.key == K_RSHIFT:
                    if record == False:
                        rightshift = True
        fallingspeedlist = [0.5 ,0.5, 0.44, 0.38, 0.32, 0.26, 0.21, 0.17, 0.13, 0.10, 0.08, 0.06, 0.04, 0.03, 0.02, 0.02] 
        
        if score > level * 10:
            level += 1
            if level <= 15:
                fallingspeed =  fallingspeedlist[level]
            else:fallingspeed =  fallingspeedlist[15]
            DrawBoard(thesecondone, hold, score, level - 1, LEVELCOLOR = BACK_GROUND_COLOR)
            DrawBoard(thesecondone, hold, score, level)
        if return_to_page :
            break
        if pause:

            continue
        if gameover:
            if not perform :
                for i in range(10):
                    Game_Over_Animation(Allblocks)
                    DrawBoard(thesecondone, hold, score, level)
                    pygame.time.delay(100)
                perform = True
            else:
                TEXT_Animation(RECT_BOARD.centerx, RECT_BOARD.centery, 'GAME OVER', DISPLAY_TIME=2000)

            continue
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

        if (moveleft or moveright) and time.time() - lastMoveSidewaysTime > movesidewayfrequency:
            if moveleft:
                MoveLeftSide(droppingblock)
            elif moveright:
                MoveRightSide(droppingblock)
            lastMoveSidewaysTime = time.time()

        if movedown and time.time() - lastMoveDownTime > movedownfrequency :
            MoveDownSide(droppingblock)
            lastMoveDownTime = time.time()
            '''
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

        DrawBoard(thesecondone, hold, score, level)
        #check if the dropping block is descended to the bottom
        if canDrop(droppingblock) == False:

            if time.time() - lastdrop > fallingspeed :
                CompleteRow = FindCompleteRow()
                completerow = CompleteRow[:]
                if len(completerow) > 0:
                    last_score = score

                score += len(completerow)

                EliminateRowBlocks(CompleteRow)
                thechoice = random.choice(['I','J','L','O', 'S', 'T', 'Z'])
                thefirsttwochoice = thefirsttwochoice[1:]+[thechoice]
                thefirstone = thefirsttwochoice[0]
                thesecondone = thefirsttwochoice[1]
                droppingblock = Tetris(thefirstone)
                while topmost(droppingblock) < 0:
                    droppingblock.center[1] +=1

                if len(completerow) > 0:
                    DrawBoard(thesecondone, hold, last_score, level, SCORECOLOR = BACK_GROUND_COLOR)

                DrawBoard(thesecondone, hold, score, level)

                if option_check(droppingblock, Allblocks) == False:
                    gameover = True
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
                Drop(droppingblock)
                lastdrop = time.time()
            else:
                if time.time() - lastdrop > fallingspeed:
                    Drop(droppingblock)
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
def DrawBoard(thesecondone, hold, score, level, SCORECOLOR = WHITE, LEVELCOLOR = WHITE, BACKCOLOR = BACK_GROUND_COLOR, TEXT_FONT = 35):
    global BOARDWIDTH, BOARD_LEFT, BOARD_UP, RECT_BOARD, BLOCK_SIZE
    Coord_centerx = BOARD_LEFT + BOARDWIDTH + 30 
    Coord_centery = BOARD_UP + 40
    for raw_index in range(AboveLine,len(Allblocks)):
        for block in Allblocks[raw_index]:
            pygame.draw.rect(DISPLAYSURF, block.color, block.rect)
    if hold:
        pygame.draw.rect(DISPLAYSURF, BACK_GROUND_COLOR, (BOARD_LEFT-4*BLOCK_SIZE-6, BOARD_UP, 4*BLOCK_SIZE, 4*BLOCK_SIZE))
        DISPLAYSURF.blit(image[hold.shape], (BOARD_LEFT-4*BLOCK_SIZE-6, BOARD_UP))


    #next block
    pygame.draw.rect(DISPLAYSURF, BACK_GROUND_COLOR, (BOARD_LEFT+BOARDWIDTH+6, BOARD_UP, 4*BLOCK_SIZE, 4*BLOCK_SIZE))
    DISPLAYSURF.blit(image[thesecondone], (BOARD_LEFT+BOARDWIDTH+6, BOARD_UP))

    fontObj = pygame.font.Font('freesansbold.ttf', TEXT_FONT)

    textSurfaceObj3 = fontObj.render(f'score:', True, WHITE,BACKCOLOR)
    textRectObj3 = textSurfaceObj3.get_rect()
    textRectObj3.center = (Coord_centerx + 30,Coord_centery + 160)
    DISPLAYSURF.blit(textSurfaceObj3, textRectObj3)

    textSurfaceObj3_1 = fontObj.render(f'{score}', True, SCORECOLOR,BACKCOLOR)
    textRectObj3_1 = textSurfaceObj3_1.get_rect()
    textRectObj3_1.topleft = textRectObj3.topright
    DISPLAYSURF.blit(textSurfaceObj3_1, textRectObj3_1)

    textSurfaceObj4 = fontObj.render(f'level:', True, WHITE,BACKCOLOR)
    textRectObj4 = textSurfaceObj4.get_rect()
    textRectObj4.center = (Coord_centerx + 30,Coord_centery + 200)
    DISPLAYSURF.blit(textSurfaceObj4, textRectObj4)

    textSurfaceObj4_1 = fontObj.render(f'{level}', True, LEVELCOLOR,BACKCOLOR)
    textRectObj4_1 = textSurfaceObj4_1.get_rect()
    textRectObj4_1.topleft = textRectObj4.topright
    DISPLAYSURF.blit(textSurfaceObj4_1, textRectObj4_1)

    textSurfaceObj5 = fontObj.render(f'HOLD', True, WHITE,BACKCOLOR)
    textRectObj5 = textSurfaceObj5.get_rect()
    textRectObj5.center = (BOARD_LEFT - 2*BLOCK_SIZE - 3, Coord_centery + 120)
    DISPLAYSURF.blit(textSurfaceObj5, textRectObj5)

    textSurfaceObj6 = fontObj.render(f'NEXT', True, WHITE,BACKCOLOR)
    textRectObj6 = textSurfaceObj6.get_rect()
    textRectObj6.center = (BOARD_LEFT +  BOARDWIDTH + 2*BLOCK_SIZE + 6, Coord_centery + 120)
    DISPLAYSURF.blit(textSurfaceObj6, textRectObj6)
    pygame.display.update()
#DISPLAY_TIME == 0 means it won't be removed 
def StartGameAnimation():
    pygame.draw.rect(DISPLAYSURF, RED, (BOARD_LEFT-3, BOARD_UP-3, BOARDWIDTH+6, BOARDHEIGHT+6),3)

    #next
    pygame.draw.rect(DISPLAYSURF, RED, (BOARD_LEFT+BOARDWIDTH+3, BOARD_UP-3, 4*BLOCK_SIZE+6, 4*BLOCK_SIZE+6),3)

    #hold
    pygame.draw.rect(DISPLAYSURF, RED, (BOARD_LEFT-4*BLOCK_SIZE-9, BOARD_UP-3, 4*BLOCK_SIZE+6, 4*BLOCK_SIZE+6),3)

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
def FindCompleteRow():

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
def option_check(InputTetris, Allblocks):
    check = InputTetris.position()
    for i in range(len(check)):
        if Allblocks[check[i][1]][check[i][0]].state == '1':
            return False
    return True
def Game_Over_Animation(Allblocks):
    for row in Allblocks:
        for block in row:
            t = list(block.color)
            for i in range(len(t)):
                if t[i] > 10:
                    t[i] -= 10
            block.color = tuple(t)

if __name__=='__main__':
    main()
