from pyfirmata import Arduino, SERVO
from time import sleep
import numpy as np
import pygame
import sys

from pygame.locals import*
pygame.init()
pygame.display.set_caption('Arm Controller')
screen = pygame.display.set_mode((500,500),0,32)
clock = pygame.time.Clock()

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    print(joystick.get_name())

font = pygame.font.SysFont(None,30)
text = font.render("hello world", True,(100,0,0) )

def write(text,color, position):
    screen.blit(font.render(text,True,color), position)
    
port='COM3'
#board = Arduino(port)
servoPins = np.array([3,5,6,9,10,11])
servoAngles = np.array([20,140,90,130,30,180])
motion = np.array([0,0,0,0,0,0])
#def rotateServo(pin,angle):
#    board.digital[pin].write(angle)

def main():
    while True:
        screen.fill((0,0,0))
   
        
        for i in range (0, len(servoPins)):
            #print("i=" + str(i))
            #print("pin="+str(servoPins[i]))
            if abs(motion[i]) < .1:
                motion[i] = 0
            servoAngles[i] += motion[i]
            if servoAngles[i] < 0:
                servoAngles[i] = 0
            if servoAngles[i] > 180:
                servoAngles[i] = 180
            print("angle"+str(i)+"="+str(servoAngles[i]))
            write("angle"+str(i)+"="+str(servoAngles[i]),(0,255,0),(250,250+20*i))
            #rotateServo(servoPins[i],servoAngles[i])
        for event in pygame.event.get():
            if  event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == JOYAXISMOTION:
                #print((event.axis))
                if event.axis < 4 and abs(event.value) > 0.1:
                    print(event.value)
                    motion[event.axis] = event.value
            if event.type == JOYBUTTONDOWN:
                print(event)
                if event.button == 11:
                    motion[4] = 1
                if event.button == 12:
                    motion[4] = -1
                if event.button == 14:
                    motion[5] = 1
                if event.button == 13:
                    motion[5] = -1
            if event.type == JOYBUTTONUP:
                if event.button == 12 or event.button == 11:
                    motion[4] = 0
                if event.button == 14 or event.button == 13:
                    motion[5] = 0
        pygame.display.update()
        clock.tick(60)
main()