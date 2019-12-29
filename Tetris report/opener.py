# the animation used in the game
import pygame, random, time, sys, os
from pygame.locals import *


FPS=30
WINDOWWIDTH = 1366
WINDOWHEIGHT = 768

BLACK   = (  0,  0,  0)
WHITE   = (255,255,255)
RED     = (255,  0,  0) 
GREEN   = (  0,255,  0)
BLUE    = (  0,  0,255)
YELLOW  = (255,255,  0)
AQUA    = (  0,255,255)
PURPLE  = (153, 50,204)
ORANGE  = (255,165,  0)

BACK_GROUND_COLOR = BLACK



def Opening_Screening():
    
    global DISPLAYSURF, FPSCLOCK
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption("Plat Tetris!")
    FPSCLOCK = pygame.time.Clock()
    
    
    DISPLAYSURF.fill(BACK_GROUND_COLOR)
    
    TextAnimation(WINDOWWIDTH/2, WINDOWHEIGHT/4, 'Tetris', 100, GREEN)
    
    TitleRect = TEXT_Rect(WINDOWWIDTH/2, WINDOWHEIGHT/4, 'Tetris' , 100)
    TextAnimation(WINDOWWIDTH/2, WINDOWHEIGHT/2,  'Single Player', 50, BLACK, WHITE)
    SinglePlayerRect = TEXT_Rect(WINDOWWIDTH/2, WINDOWHEIGHT/2, 'Single Player' , 50)
    print(SinglePlayerRect)
    
    TextAnimation(WINDOWWIDTH/2, WINDOWHEIGHT/2 +100,'Player VS Computer', 50, BLACK, WHITE)
    PlayervsComputerRect = TEXT_Rect(WINDOWWIDTH/2, WINDOWHEIGHT/2+100, 'Player VS Computer' , 50)
    
    
    
    TextAnimation(WINDOWWIDTH/2, WINDOWHEIGHT/2 +200, 'Player VS Player', 50, BLACK, WHITE)
    PlayervsPlayerRect = TEXT_Rect(WINDOWWIDTH/2, WINDOWHEIGHT/2 +200, 'Player VS Player' , 50)
    
    TextAnimation(WINDOWWIDTH/2, WINDOWHEIGHT/2 +300, 'Computer VS Computer', 50, BLACK, WHITE)
    ComputervsComputerRect = TEXT_Rect(WINDOWWIDTH/2, WINDOWHEIGHT/2 +300, 'Computer VS Computer' , 50)
    
    
    mousex = 0
    mousey = 0
    
    LINEWIDTH = 3
    while True:
        mouseclicked = False
        for event in pygame.event.get():
            
        
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            
            
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                
                
            
            
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseclicked = True
                print(mousex, mousey)
        
        if mouseclicked == True:
            print ('Yes')
            if  IsInRect(mousex, mousey, SinglePlayerRect):
                print('1')
                pygame.quit()
                
                print('SinglePlayer')
                import reference
                reference.main()
        
                RestartProgram()    
                    #

            elif  IsInRect(mousex, mousey, PlayervsComputerRect):
                pygame.quit()
                print('PlayervsComputer')
                import reference4
                reference4.main()
                RestartProgram()   
                    #
            elif  IsInRect(mousex, mousey, PlayervsPlayerRect):

                pygame.quit()
                print('PlayervsPlayer')
                import reference2
                reference2.main()
                RestartProgram()
                #
                    
            elif  IsInRect(mousex, mousey, ComputervsComputerRect):

                pygame.quit()
                print('ComputervsComputer')
                import reference5
                reference5.main()
                RestartProgram()
                #
                    
        
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)    
        
def RestartProgram():    
    print('restart')
    path = sys.executable
    os.execl(path, path, sys.argv[0])
    



# other design:
# the setting of the special game in the double game
def TEXT_Rect(Coord_centerx, Coord_centery, TEXTmsg, TEXT_FONT = 32 , FONT_TYPE = 'freesansbold.ttf'):
    fontObj = pygame.font.Font(FONT_TYPE, TEXT_FONT)
    textSurfaceObj = fontObj.render(TEXTmsg, True, WHITE, BLACK)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (Coord_centerx,Coord_centery)
    return textRectObj
    


def TextAnimation(Coord_centerx, Coord_centery,TEXTmsg, TEXT_FONT = 32, FRONTCOLOR = RED, BACKCOLOR = BACK_GROUND_COLOR, DISPLAY_TIME = 0, FONT_TYPE = 'freesansbold.ttf'):
    
    fontObj = pygame.font.Font(FONT_TYPE, TEXT_FONT)
    textSurfaceObj = fontObj.render(TEXTmsg, True, FRONTCOLOR,BACKCOLOR)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (Coord_centerx,Coord_centery)

    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    pygame.display.update()
    
    if DISPLAY_TIME != 0:
        pygame.time.delay(DISPLAY_TIME)
        pygame.draw.rect(DISPLAYSURF, BACK_GROUND_COLOR, textRectObj)

        pygame.display.update()
        
def IsInRect(x,y,rect):
    if rect.left < x < rect.right and rect.top < y < rect.bottom:
        return True
    return False

if __name__ == '__main__':
    Opening_Screening()