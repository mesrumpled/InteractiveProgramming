""" Visualizes input data over the years 1990-2014 as an interactive bar graph.

@authors: March Saper, Emma Price

Software Design 2016 Olin College of Engineering"""
    
import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEMOTION
import time
import csv
import random
import collections
   

def generate_rates(f):
    """Takes a csv file with one column of states and the other of the rates for each
    state. It takes this file and then maps each state to a single key and the rates
    into a list that is the value for each state key"""
    with open(f, 'rb') as f:
        reader = csv.reader(f)
        rates = {}
        for row in reader:
            if row[0] in rates:
                rates[row[0]].append(row[1])
            else:
                rates[row[0]] = [row[1]]
        return rates


def generate_colors(d):
    """Generates a color for each element in the data set by iterating through the
    number of keys and mapping that value onto the rgb scale. The rgb functions were
    chosen through trial and error"""
    colors = {}
    for index, state in enumerate(d.iterkeys()):
    # for state,index in d.iteritems():
        #print index
        colors[state] = ((index*255)/51, (index*200)/51, 200)
        #print (index*100)/51
    return colors


STATE_RATES = collections.OrderedDict(sorted(generate_rates('CleanedUpData_noyear.csv').items()))

SIZE = (1700, 1040)

STATE_COLORS = collections.OrderedDict(sorted(generate_colors(STATE_RATES).items()))


class View(object):
    """visualizes the data on the screan and creates labels for each bar in the bar graph"""
    def __init__(self, model, screen):
        """initializes the model class and screen surface"""
        self.model = model
        self.screen = screen

    def draw(self):
        """draws rectangles and labels"""
        self.screen.fill(pygame.Color('white'))
        for state in self.model.states_rect:
            pygame.draw.rect(self.screen, pygame.Color(*STATE_COLORS[state]), self.model.states_rect[state])
    
        self.screen.blit(model.title, (SIZE[0]/1.8,SIZE[1]/17))
        self.screen.blit(model.year, (SIZE[0]/1.1,SIZE[1]/8))

        for i, state in enumerate(model.states_names):
            self.screen.blit(model.states_names[state], (i*(SIZE[0]/50.0), 650))

        for i, state in enumerate(model.states_num):
            self.screen.blit(model.states_num[state], ((i*(SIZE[0]/50.0) + 8, 615)))

        self.screen.blit(model.surprise, (0,0))
        pygame.display.update()


class Model(object):
    """stores the state of the visualization for each year and updates the year and
    resulting visualization as the mouse moves across the screen"""
    def __init__(self):
        self.states_rect = {}
        for i, state in enumerate(STATE_RATES):
            self.states_rect[state] = pygame.Rect(i*(SIZE[0]/50.0) + 8, 600, (SIZE[0]/50.0-16), 0)
        self.states_rect = collections.OrderedDict(sorted(self.states_rect.items()))

        # initialize the title
        freetypeT = pygame.font.SysFont("serif", 54)
        self.title = freetypeT.render("Teen Pregnancy Rates per capita", True, (0, 0, 0))

        # initialize the state names
        self.states_names = {}
        for i, state in enumerate(STATE_RATES):
            freetype = pygame.font.SysFont("serif", 24)
            self.states_names[state] = freetype.render(STATE_RATES.keys()[i], True, (0, 0, 0))
            self.states_names[state] = pygame.transform.rotate(self.states_names[state], 90)
        self.states_names = collections.OrderedDict(sorted(self.states_names.items()))

        # initialize the state values
        self.states_num = {}
        for i, state in enumerate(STATE_RATES):
            self.freetype = pygame.font.SysFont("serif", 18)
            self.states_num[state] = self.freetype.render("-", True, (0, 0, 0))
        self.states_num = collections.OrderedDict(sorted(self.states_num.items()))

        # initializes the year
        freetypeY = pygame.font.SysFont("serif", 38)
        p = ""
        self.year = freetypeY.render(p, True, (0, 0, 0))

        # initializes the surpirse text
        freetypeS = pygame.font.SysFont("comicsansms", 20)
        self.surprise = freetypeS.render("", True, (0, 0, 0))

        
    def update(self, position):
        """updates rectangle dimensions and labels based on the controller position"""
        for state in STATE_RATES:
                scaled_value = (float(position[0])/SIZE[0])*len(STATE_RATES[state])
                chosen_index = int(scaled_value)
                self.states_rect[state].height = (-5*float(STATE_RATES[state][chosen_index]))

        # Shows the current year 
        freetypeY = pygame.font.SysFont("serif", 38)
        p = str(1990 + chosen_index)
        self.year = freetypeY.render(p, True, (0, 0, 0))

        # Shows the current rate for each state
        for state in self.states_num: #freetype = pygame.font.SysFont("serif", 18)
            pos = STATE_RATES[state][chosen_index]
            val = int(float(pos))
            self.states_num[state] = self.freetype.render(str(val), True, (0, 0, 0))
        
        # Is a surprise!
        if position == (0, 0):
            freetypeS = pygame.font.SysFont("comicsansms", 30)
            self.surprise = freetypeS.render("yay birth control", True, (0, 255, 0))
            

        
class MouseController(object):
    def __init__(self, model):
        """initializes the controller"""
        self.model = model

    def handle_event(self, event):
        """tracks the position of the controller and updates the model accordingly"""
        if event.type != MOUSEMOTION:
            return
        else:
            position = pygame.mouse.get_pos()
            self.model.update(position)

              

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)

    model = Model()
    view = View(model, screen)
    controller = MouseController(model)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_event(event)
        view.draw()
        time.sleep(.001)
    
