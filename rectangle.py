import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEMOTION
import time
import csv
import random

""" This imports and create a dictionary. Each key for each state has a list with rates for each year."""
with open('CleanedUpData_noyear.csv', 'rb') as f:
    reader = csv.reader(f)

    STATE_RATES = {}
    for row in reader:
        if row[0] in STATE_RATES:
            STATE_RATES[row[0]].append(row[1])
        else:
            STATE_RATES[row[0]] = [row[1]]


SIZE = (1040, 1040)

STATE_COLORS = {}
for state in STATE_RATES:
    STATE_COLORS[state] = (0, random.randint (0,100), random.randint (50,255))


class View(object):
    """visualizes the rectangles"""
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen

    def draw(self):
        self.screen.fill(pygame.Color('black'))
        for state in self.model.states_rect:
            pygame.draw.rect(self.screen, pygame.Color(*STATE_COLORS[state]), self.model.states_rect[state])
        pygame.display.update()

class Model(object):
    def __init__(self):
        self.states_rect = {}
        for location, state in enumerate(STATE_RATES):
            self.states_rect[state] = pygame.Rect(location*(SIZE[0]/50.0) + 5, 600, (SIZE[0]/50.0-10), 0)

        
class MouseController(object):
    def __init__(self, model):
        self.model = model

    def handle_event(self, event):
        if event.type != MOUSEMOTION:
            return
        else:
            position = pygame.mouse.get_pos()
            for state in STATE_RATES:
                scaled_value = (float(position[0])/SIZE[0])*len(STATE_RATES[state])
                chosen_index = int(scaled_value)
                self.model.states_rect[state].height = (-5*float(STATE_RATES[state][chosen_index]))  # Question about this!!


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