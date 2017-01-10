'''
Created on Nov 12, 2014

@author: Zachary Kirby

Version 1.5.2 beta

@about: This game demonstrates the synthesis of Python and Arduino.
A trivia game that also moves a tangible/ real-time car every time the user answers
a question correctly. 

Purpose: built to be used at the club rush to attract attention for the robotics
club. Also an awesome challenge to see if I can figure out how 
to communicate and intermediate between two languages

Future: The Current GUI runs on pygame and was built when I was more comfortable
with that module. However, plans are set to change the program to GTK+3 and add
LAN support through a local mesh network in the school. Also the graphics need
to be upgraded as I am not an artist. 
'''

#--Imports--
import serial, time, random, sys
import pygame
from pygame.locals import *

#--Movable Car logic--  
class BlueCar(pygame.sprite.Sprite):
    def __init__(self, width, height):
        '''A basic Movable car that shows
        the progress of the player'''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Pics\Carb.png").convert()
        self.rect = self.image.get_rect()
    def update_movement(self):
        self.rect.x += 88

#--Serial Communications With Ariduno initiation--
def serail_connect(com='COM3'):
    '''Try to Connect to a serial port in order
    to interface with arduino and run commands'''
    try:
        ser = serial.Serial(com, 9600)
        time.sleep(2)
        print("Connected To: "+ser.portstr)
        return ser
    except Exception, e:
        print("Encountered Error connecting to Arduino: "+str(e))

#--Question Database--
def question_database():
    '''Holds the database of both the questions and the answers, 
    is a seperate function so it can be called in other files'''
    #The list of questions for the game
    custom_log = ["6 * 8","25 * 31","100 * 400", "5 * 5 * 7", "829348237282378327 * 0", "10/5","482/2","75/2","50/100", "(50/5)/5", "53 - 13","2468 - 1357", "58 - 76", "4000 - 300 - 20 - 1", "3278377364 - 3278377363","102 + 93", "3 + 3 + 3 + 3 + 3 + 3 + 3","7 + 493","2468 + 1357","999 + 111", "5^2", "2^4","1^100", "7823^0", "7^3","Free Space!(type '1')", 'Challenge:(4*3)^2 + 90 - 34', "Challenge:(2^2)^3)^3)","Free Space!(type '1')", "Challenge: 5^5"]
    #The dictoinary of answers to the questions
    custom_ans = {"6 * 8" : "48", "25 * 31": "775","100 * 400": "40000", "5 * 5 * 7": "175", "829348237282378327 * 0": "0", "10/5": "2","482/2": "241","75/2": "37.5","50/100": ".5", "(50/5)/5": "2", "53 - 13": "40","2468 - 1357": "1111", "58 - 76": "-18", "4000 - 300 - 20 - 1": "3679", "3278377364 - 3278377363": "1","102 + 93": "195", "3 + 3 + 3 + 3 + 3 + 3 + 3": "21","7 + 493": "500","2468 + 1357": "3825","999 + 111": "1110", "5^2": "25", "2^4": "16","1^100": "1", "7823^0": "1", "7^3": "343","Free Space!(type '1')": "1", 'Challenge:(4*3)^2 + 90 - 34': "200", "Challenge:(2^2)^3)^3)": "262144","Free Space!(type '1')": "1", "Challenge: 5^5": "3125"}
    
    return custom_log, custom_ans

def new_question(log_base, log_ans):
    '''Creates the next question
    so that the game continues'''
    global quePointer, queAsked, userComparison
    quePointer = random.randrange(30)
    queAsked = log_base[quePointer]
    userComparison = log_ans[log_base[quePointer]]

def new_text(text, posX, posY, bgcolor, color, font, space, blit_on, orientation=1):
    '''Creates a new Text and blits
    it to the screen'''
    try:
        textStat=font.render(str(text), True, color, bgcolor) 
        textposStat = textStat.get_rect(centerx=space.get_width()/2)
        textposStat.top = posY
        if orientation == 1:
            textposStat.right = posX
        elif orientation == 2:
            textposStat.left = posX
        blit_on.blit(textStat, textposStat)
    except Exception, e:
        print("Failed to Blit Text to Screen: "+str(e))

def main():
    '''Main Loop that runs/updates 
    pygame componets and graphics'''
    
    #--Background Logic--
    BGcolor = (0,255,255); black = (0,0,0); white = (255, 255, 255); red = (255, 0, 0); blue = (40, 40, 170); grey = (100, 100, 100)
    pygame.init()
    queLog, queAns = question_database()
    #conn = serial_connect()
    pygame.display.set_caption("~~Schooled~~")
    screen=pygame.display.set_mode((1100,700),0,32)
    background = pygame.image.load("Pics\BGblue.jpg").convert()
    clock=pygame.time.Clock()
    clock.tick(80)  
    
    #--Create Car--    
    cars = pygame.sprite.Group()
    car = BlueCar(50, 50)
    car.rect.x = -188
    car.rect.y = 93
    cars.add(car)
        
    #--Font Selections--
    headFont = pygame.font.Font("Fonts/Chunkfive Ex.ttf", 15)   
    smallStat = pygame.font.Font("Fonts/stat.ttf", 25)   
    bigStat = pygame.font.Font("Fonts/stat.ttf", 55)   
    otherFont = pygame.font.Font("Fonts/Acens.ttf", 85)   
    
    #--Empty starting ints, strings, and booleans--
    right = 0
    wrong = 0
    scorePercentage = 100
    queRemaining = 30
    corseCompleted = 0
    currentQue = 0
    correctAns = "None"
    pastAns = "None"
    currentCatagory = "Math"
    userAns = ""
    continuationQualifier = True
    
    #--The First Question--
    new_question(queLog, queAns)
    
    #--Start of Real-Time game logic--
    while True:
        screen.blit(background,(0,0))  
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
                #conn.close()
            if event.type == KEYDOWN and continuationQualifier == True:
                if event.unicode.isalpha():
                    userAns += event.unicode
                elif event.key == K_BACKSPACE:
                    userAns = userAns[:-1]
                elif event.key == K_RETURN:
                    #--If they get it right--
                    if userAns == userComparison:
                        right+=1
                        pastAns = userAns
                        correctAns = userComparison
                        queRemaining-=1
                        corseCompleted += 10
                        userAns = ""
                        new_question(queLog, queAns)
                        car.update_movement()
                        scorePercentage+=3.3
                        #ser.write('R')
                    #--If they get it wrong--
                    elif userAns != userComparison:                        
                        wrong+=1
                        pastAns = userAns
                        correctAns = userComparison
                        queRemaining-=1
                        userAns = ""
                        new_question(queLog, queAns)
                        scorePercentage-=3.3
                        #ser.write('W')   
                        
                    #--Added Number Input Section--        
                elif event.key == K_1:
                    userAns += "1"
                elif event.key == K_2:
                    userAns += "2"
                elif event.key == K_3:
                    userAns += "3"
                elif event.key == K_4:
                    userAns += "4"
                elif event.key == K_5:
                    userAns += "5"
                elif event.key == K_6:
                    userAns += "6"
                elif event.key == K_7:
                    userAns += "7"
                elif event.key == K_8:
                    userAns += "8"
                elif event.key == K_9:
                    userAns += "9"
                elif event.key == K_0:
                    userAns += "0"
                elif event.key == K_PERIOD:
                    userAns += "."
                elif event.key == K_MINUS:
                    userAns += "-"
                
                #--Easter Eggs :3--
                elif event.key == K_BACKSLASH:
                    userAns += "Zach rocks!"
                elif event.key == K_FORWARDSLASH:
                    userAns += "ROBOTICS!!!!"
                elif event.key == K_AT:
                    userAns += "Live Long and Prosper" 
        
        #--Int to String Convestions--
        right_str = str(right)      
        wrong_str = str(wrong)
        queR_str = str(queRemaining)
        scorePer_str = str(scorePercentage)  
        course_completed_str = str(corseCompleted)
            
        #--Stats screen text positioning--
        new_text("Stats", 970, 58, BGcolor, blue, smallStat, background, screen)
        new_text("Question:", 307, 57, BGcolor, (0,103,51), bigStat, background, screen)
        new_text("Your Answer:", 405, 290, BGcolor, (0, 103, 51), bigStat, background, screen)
        new_text("Questions Right:", 1020, 115, BGcolor, (9,249,17), headFont, background, screen)
        new_text(("Questions Wrong: "+wrong_str), 1026, 147, BGcolor, (205,0,0), headFont, background, screen)
        new_text(("Questions Left: "+queR_str), 1018, 178, BGcolor, (237,255,124), headFont, background, screen)
        new_text(("Category: "+currentCatagory), 994, 245, BGcolor, black, headFont, background, screen)
        new_text(("Answer: "+correctAns), 980, 280, BGcolor, (0,0,128), headFont, background, screen)
        new_text(("Completed: "+course_completed_str+"%"), 600, 592, BGcolor, grey, smallStat, background, screen)
        new_text(("Your Answer: "+pastAns), 1030, 315, BGcolor, (75,0,130), headFont, background, screen)
        new_text(("Score: "+scorePer_str+"%"), 985, 387, BGcolor, (255,215,0), headFont, background, screen)
        new_text("Join Robotics!", 990, 456, BGcolor, (0,128,0), headFont, background, screen)
        new_text("Version: 1.5.2", 984, 420, BGcolor, (178,34,34), headFont, background, screen)
        new_text(userAns, 233, 390, black, white, bigStat, background, screen, orientation=2)
        cars.draw(screen) 
        
        #--Blits the question to the Screen as long as the player has question left--
        if continuationQualifier == True:
            new_text(queAsked, 137, 160, white, black, bigStat, background, screen, orientation=2)
                        
        #--If they win by answering 10 questions right, end the Game--
        if right == 10:
            background = pygame.image.load("Pics\WinB.jpg").convert()  
            new_text("Winner!!!", 100, 190, (255,255,255), blue, otherFont, background, screen, orientation=2)
            continuationQualifier = False
            #conn.close()
        
        #--If the player runs out of questions, i.e. loses the game--
        if queRemaining == 0:
            new_text("You're Out Of Questions", 100, 190, (0,0,0), red, otherFont, background, screen, orientation=2)
            continuationQualifier = False #Prevents user from writing anything to the screen
            #conn.close() 
            
        pygame.display.flip()
        pygame.display.update()
    pygame.quit() 
    
if __name__ == '__main__':main()
       