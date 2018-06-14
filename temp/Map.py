#Ant World
#Created By: Frank L Brasington

#This is the Map of the world that the Ants will live in.

#this world was created in pygame
import pygame
import numpy as np
import math

#Imports the Deep Q network form AI in Ai.py
from Ai import Dqn

#This generates our AI
#The constructor for DQN looks like does below
#def __init__(self, input_size, nb_action, gamma):
in_size = 2
actions = 3
gamma = 0.9
ai = Dqn(in_size,actions,gamma)
#temporary
action2rotation = [0, 20, 20]



#Colors
black = (0,0,0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
dark_green = (0, 166, 0)
blue = (0, 0, 255)

#for the clock and time
clock = pygame.time.Clock()

# create a surface on the screen with size
world_width = 800
world_length = 800
screen = pygame.display.set_mode((world_width, world_length))


#this is a simple function that calculates the distance between two objects
def dist_calc(x, y, goal_x, goal_y):
    return np.sqrt((x - goal_x)**2 + (y - goal_y)**2)


class Ant():

    def __init__(self, start_x, start_y, color, type):
        self.o_type = type
        #for the starting x and y
        self.loc_x = start_x
        self.loc_y = start_y
        #sets the color
        self.color = color
        #sets the size x by y
        self.x = 10
        self.y = 10
        #sets the radiis of the body
        self.radius = 10
        #sets the distance of the sensors
        self.sensor_x = self.loc_x
        self.s_distance = 15
        #x and y of the sensor
        self.s_x = self.loc_x + self.s_distance
        self.s_y = self.loc_y
        #sets the starting angle
        self.angle = 0
        body = pygame.draw.circle(screen, self.color, (self.loc_x, self.loc_y), self.radius, 0)
        #these are the left and right senseors
        sensor = pygame.draw.circle(screen, blue, (self.s_x, self.s_y), 3, 0)

        #this area is for all the variables such as if the ant is carrying food
        self.has_food = False
        #this stores if the ant is carrying food
        self.food = None

        #this sets the goals for the ant moving from the upper left to the lower right
        self.goal_x = 700
        self.goal_y = 700
        #this is the current distance from the ant to the goal
        self.distance = dist_calc(start_x, start_y, self.goal_x, self.goal_y)
        self.last_reward = 0
        self.scores = []


    def update(self):
        #draws the image
        body = pygame.draw.circle(screen, self.color, (self.loc_x, self.loc_y), 10, 0)
        sensor = pygame.draw.circle(screen, blue, (self.s_x, self.s_y), 3, 0)

        #if the ant is carring food then the food needs to be upated
        if self.food != None:
            self.food.move(self.loc_x, self.loc_y)

        #this keeps the ant on the map
        if self.loc_y+self.radius > world_length:
            self.loc_y = world_length - self.radius
        if self.loc_y - self.radius < 0:
            self.loc_y = 0 + self.radius
        if self.loc_x + self.radius > world_width:
            self.loc_x = world_width - self.radius
        if self.loc_x - self.radius < 0:
            self.loc_x = 0 + self.radius

    def move(self, movement=0, turn=0):
        self.angle += turn
        #changes to radians as needed
        rad = np.pi/180 * self.angle
        #the change to the x and y direction
        self.loc_x += movement * math.cos(rad)
        self.loc_y += movement * math.sin(rad)
        #sets the sensors to the correct locations
        self.s_x = self.loc_x + self.s_distance*math.cos(rad)
        self.s_y = self.loc_y + self.s_distance*math.sin(rad)
        #converts the locations to integers
        self.loc_y = int(self.loc_y)
        self.loc_x = int(self.loc_x)
        self.s_x = int(self.s_x)
        self.s_y = int(self.s_y)

    #this is the sensor, dectects what the object that is there
    def sense(self, o):
        #detects if the object is in the sensor's area
        if self.s_x - o.loc_x < 10 and self.s_x - o.loc_x > -10:
            if self.s_y - o.loc_y < 10 and self.s_y - o.loc_y > -10:
                #print(o.o_type)
                if o.o_type == "Food" and self.food == None:
                    self.food = o
                    self.has_food = True
                #testing the giving of food
                if o.o_type == "Queen" and self.food != None:
                    self.give_food(o)

    #this transfer the food object to the other ant
    def give_food(self, ant_object):
        if self.food != None:
            if ant_object.has_food == False:
                #give the food object
                ant_object.food = self.food
                #removes the food object
                self.food = None
                #changes the status for the two ants
                self.has_food = False
                ant_object.has_food = True

    #this gives out all the rewards
    #currently this is a simple task of the ant moving from the upper left to the lower right
    #then return back to the upper left and repeat
    def rewards(self):
        #checks to see if there is a reward for being closer to the desired location
        cur_distance = dist_calc(self.loc_x, self.loc_y, self.goal_x, self.goal_y)
        if cur_distance < self.distance:
            self.last_reward = 0.1

        #sets the goal to the upper right or lower left
        if cur_distance < 50:
            if self.goal_x == 700:
                self.goal_x = self.goal_y = 200
            else:
                self.goal_x = self.goal_y = 700
        

#this is for the food that the ants will be collecting and eating
class Food():
    o_type = "Food"

    def __init__(self, start_x, start_y):
        self.color = dark_green
        self.loc_x = start_x
        self.loc_y = start_y
        body = pygame.draw.circle(screen, self.color,(self.loc_x, self.loc_y), 5, 0)

    def update(self):
        body = pygame.draw.circle(screen, self.color, (self.loc_x, self.loc_y), 5, 0)

    #this allows the food to be moved
    #x & y are the new location for the food that is being moved
    def move(self, x, y):
        self.loc_y = y
        self.loc_x = x

#this is the main function
def main():

    #initializes the pygame module
    pygame.init()
    pygame.display.set_caption("Ant World")

    #defines a variable to control the main loop
    running = True

    #makes 1 ant
    a = Ant(300, 500, red, "ant")

    #creates a Queen ant for testing
    #q = Ant(300, 400, black, "Queen")

    #makes 1 food pellet
    p = Food(500,500)

    #This list stores all the objects in the Ant WOrld
    ants = []
    food = []

    #adds the ant and the food pellet
    ants.append(a)
    #ants.append(q)
    food.append(p)

    #this is all the objects in the ant world
    w_objects = ants + food

    #the main loop function
    while running:
        #gets all the events
        for event in pygame.event.get():
            #quits the ant world
            if event.type == pygame.QUIT:
                running = False

        #updates the background
        screen.fill(white)
        #print("line 225")
        #does all the move actions for the ants
        #for a in ants:
        #THis is the last signal that was recieved
        last_signal = [(a.loc_x, a.loc_y), (a.s_x, a.s_y)]
        #print("line230")
        #print("last_reward: ", a.last_reward, " last_signal: ", last_signal)
        action = ai.update(a.last_reward, last_signal)
        #print("line232")
        a.scores.append(ai.score())
        rotation = action2rotation[action]
        #print("line 233")
        a.move(1, rotation)

        #draws all the stuff in our world
        for n in ants:
            n.update()
        for f in food:
            f.update()

        #checks to see if the food is in the sensor
        #for x in w_objects:
        #a.sense(q)
        a.sense(f)

        #this sets the game to 60 FPS
        pygame.display.update()
        clock.tick(60)

#runs this if this file is the main script
if __name__ == "__main__":
    main()