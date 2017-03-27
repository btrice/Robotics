#! /usr/bin/env python
import pygame
import sys
import random

class Robot(object):

    def __init__ (self):
	    self.pygame = pygame.init()
	    self.screen = pygame.display.set_mode((640,480))
	    self.x = random.randint(0,9) # robot x position
	    self.y = random.randint(0,9) # robot y position
	    self.z     = 0.0
	    self.zred  = 0.0
	    self.zblue = 0.0

    def robot_up(self):
	    """ We call this methode when robot move up """	
	    self.y = self.y - 1
	    if self.y < 0:
		    self.y = 0

    def robot_down(self):
	    """ We call this methode when robot move down """	
	    self.y = self.y + 1
	    if self.y > 9:
		    self.y = 9

    def robot_left(self):
	    """ We call this methode when robot move left """
	    self.x = self.x - 1
	    if self.x < 0:
		    self.x = 0

    def robot_right(self):
	    """ We call this methode when robot move right """
	    self.x = self.x + 1
	    if self.x > 9:
		    self.x = 9
			
    def robot_random_move(self):
	    """ Robot random move """
	    r = random.randint(1,4)
	    if r == 1 and self.x < 9:
		    self.robot_right()
		    return 1
	    elif r == 2 and self.x > 0:
		    self.robot_left()
		    return 2
	    elif r == 3 and self.y > 0:
		    self.robot_up()
		    return 3
	    elif r == 4 and self.y < 9:
		    self.robot_down()
		    return 4
	    else:
		    return 5

    def display_robot(self):
	    """ Display robot on screen """
	    self.screen.fill((0,0,0))
	    blue = (0,0,255)
	    red = (255,0,0)
	    pygame.draw.rect(self.screen,blue,(0,0,640,48))
	    pygame.draw.rect(self.screen,blue,(0,0,64,480))
	    pygame.draw.rect(self.screen,red,(640-64,0,64,480))
	    pygame.draw.rect(self.screen,red,(0,480-48,640,48))
	    pygame.draw.circle(self.screen,(255,255,255),(self.x*64+32,self.y*48+24),24)
	    pygame.display.update()
	    pygame.time.wait(50)

    def perception(self):
	    """ Perception whenb robot hit the wall or encounter an obstacle """
	    self.z     = 0.0
	    self.zred  = 0.0
	    self.zblue = 0.0

	    if (self.x == 0 or self.y == 0) and  random.random() < 0.3:
		    self.zblue = 1.0
	    if (self.x == 9 or self.y == 9) and  random.random() < 0.3:
		    self.zred = 1.0

	    if (self.x == 0 or self.y == 0 or self.x == 9 or self.y == 9) and  random.random() < 0.3:
		    self.z = 1.0

    def display_probability_map(self,p):
	    """ Display robot probability map for localisation """
	    self.screen.fill((0,0,0))
	    for j in range(0,10):
		    for i in range(0,10):
			    pygame.draw.rect(self.screen,(50+205*p[i][j],0,50+205*p[i][j]),(i*64,j*48,64,48))
	    pygame.draw.circle(self.screen,(255,255,255),(self.y*64+32,self.x*48+24),24)
	    pygame.display.update()
	    pygame.time.wait(50)
		
    def init_probability_map(self):
	    """ Initialisation of probability map by 0.10 for each cell of the table"""
	    #0.10 should be 0.1 . Each line probalility should be equal to 1 (0.1 * 10 = 1)
	    #with 0.10 we can see the color difference between the screen and probabily map in display_probability_ma 
	    i = 10
	    j = 10	
	    return [[0.10 for x in range(j)] for y in range(j)]
		
	##################   LOCALISATION ####################
    def move_right(self, p):
	    """ When robot move rigth, the probability that it is on left is zero (0)
	    we move probability of each cell like p[9][9]= p[9][8],  p[8][9]= p[8][8] and put zero on the left column of probability table """
	    i = 9
	    j = 9	
	    while i > 0:
		    while j > -1:
			    p[j][i] = p[j][i-1]	
			    j = j - 1
		    j = 9			
		    i = i - 1	
		
	    for i in range(10):
		    p[i][0] = 0 # Put zero on the left column of probability table

    def move_left(self, p):
	    """ When robot move left, the probability that it is on right is zero (0)
	    we move probability of each cell like p[0][0]= p[0][1],  p[1][0]= p[1][1] and put zero on the right column of probability table """
	    i = 0
	    j = 0	
	    while i < 9:
		    while j < 10:
			    p[j][i] = p[j][i+1]	
			    j = j + 1
		    j = 0			
		    i = i + 1	
		
	    for i in range(10):
		    p[i][9] = 0 #  Put zero on the left column of probability table

    def move_up(self, p):
	    """ When robot move up, the probability that it is on down is zero (0)
	    we move probability of each cell like p[0][0]= p[1][0],  p[0][1]= p[1][1] and put zero on the down column of probability table """	
	    i = 0
	    j = 0	
	    while i < 9:
		    while j < 10:
			    p[i][j] = p[i+1][j]	
			    j = j + 1
		    j = 0			
		    i = i + 1
		
	    for i in range(10):
		    p[9][i] = 0 # Put zero on the down column of probability table
		
    def move_down(self, p):
	    """ When robot move down, the probability that it is on up is zero (0)
	    we move probability of each cell like p[9][9]= p[8][9],  p[9][8]= p[8][9] and put zero on the up column of probability table """
	    i = 9
	    j = 9	
	    while i > 0:
		    while j > -1:
			    p[i][j] = p[i-1][j]	
			    j = j - 1
		    j = 9			
		    i = i - 1
		
	    for i in range(10):
		    p[0][i] = 0 # Put zero on the up column of probability table 
		
    def localisation(self,m, p):
	    """ Localisation  """
	    if m == 1 :
		    self.move_right(p)
	    elif m == 2 :
		    self.move_left(p)
	    elif m == 3 :
		    self.move_up(p)
	    elif m == 4:
		    self.move_down(p)

    def display_prob(self, p):
	    """ Display probability map  """
	    for i in range(10):
		    for j in range(10):
			    print(p[i][j], end='  ')
		    print('\n')	
		
def main ():
    """Main function"""
    rt = Robot()
    p = rt.init_probability_map()

    while True:
        #rt.display_robot()
        rt.display_probability_map(p)
        m = rt.robot_random_move()
        rt.perception()
        rt.localisation(m,p)
        #print("x : " +str(rt.x))
        #print("y : " +str(rt.y))
        #rt.display_prob(p)
        #print(m)
        #print("Perception: I receive: "+str(rt.z))

if __name__ == "__main__":
    main()
