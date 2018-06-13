#Ant World
#Created By: Frank L Brasington

#This is the Map of the world that the Ants will live in.

#this world was created in pygame
import pygame
import numpy
import math


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

class Ant():
    o_type = "ant"

    def __init__(self, start_x, start_y, color):
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
        self.s_x = self.loc_x
        self.s_y = self.loc_y
        #sets the starting angle
        self.angle = 0
        body = pygame.draw.circle(screen, self.color, (self.loc_x, self.loc_y), self.radius, 0)
        #these are the left and right senseors
        sensor = pygame.draw.circle(screen, blue , (self.loc_x+self.s_distance, self.loc_y), 3, 0)

        #this area is for all the variables such as if the ant is carrying food
        self.has_food = False
        #this stores if the ant is carrying food
        self.food = None


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
            self.loc_x = world_width + self.radius

    def move(self, movement=0, turn=0):
        self.angle += turn
        #changes to radians as needed
        rad = numpy.pi/180 * self.angle
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
                print(o.o_type)
                if o.o_type == "Food" and self.food == None:
                    self.food = o
                    self.has_food = True


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
    a = Ant(300, 500, red)

    #makes 1 food pellet
    p = Food(500,500)

    #This list stores all the objects in the Ant WOrld
    ants = []
    food = []

    #adds the ant and the food pellet
    ants.append(a)
    food.append(p)

    #the main loop function
    while running:
        #gets all the events
        for event in pygame.event.get():
            #quits the ant world
            if event.type == pygame.QUIT:
                running = False

        #updates the background
        screen.fill(white)

        #does all the move actions for the ants
        for a in ants:
            a.move()

        #draws all the stuff in our world
        for a in ants:
            a.update()
        for f in food:
            f.update()

        #checks to see if the food is in the sensor
        a.sense(p)
        a.move(1)

        #this sets the game to 60 FPS
        pygame.display.update()
        clock.tick(60)

#runs this if this file is the main script
if __name__ == "__main__":
    main()