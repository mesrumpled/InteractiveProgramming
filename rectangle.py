import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEMOTION
import time

STATE_PREGGERS = {'Alabama':[100, 200, 300, 100, 200, 300], 'Utah':[200, 400, 300, 800, 200, 100]}
STATE_PREGGERS = {'Alabama':[100, 200, 300, 100, 200, 300], 'Utah':[200, 400, 300, 800, 200, 100]}
VALUES = [100, 200, 300, 500, 600, 900]
SIZE = (1040, 1040)

class Rectangle(object):
    """makes a Rectangle"""
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def height_adjust(self, height):
        self.height = height

class View(object):
    """visualizes the rectangle"""
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen

    def draw(self):
        self.screen.fill(pygame.Color('black'))
        r = pygame.Rect(self.model.rectangle.left,
                        self.model.rectangle.top,
                        self.model.rectangle.width,
                        self.model.rectangle.height)
        pygame.draw.rect(self.screen, pygame.Color('Medium Aquamarine'), r)
        r2 = pygame.Rect(self.model.rectangle2.left,
                        self.model.rectangle2.top,
                        self.model.rectangle2.width,
                        self.model.rectangle2.height)
        pygame.draw.rect(self.screen, pygame.Color('Green'), r2)
        pygame.display.update()

class Model(object):
    def __init__(self):
        self.rectangle = Rectangle(150, 900, 50, 50)
        self.rectangle2 = Rectangle(300, 900, 50, 50)
        self.rectangle2 = Rectangle(300, 900, 50, 50)

class MouseController(object):
    def __init__(self, model):
        self.model = model

    def handle_event(self, event):
        if event.type != MOUSEMOTION:
            return
        else:
            position = pygame.mouse.get_pos()
            scaled_value = (float(position[0])/SIZE[0])*len(STATE_PREGGERS['Alabama'])
            chosen_index = int(scaled_value)
            self.model.rectangle.height_adjust(-STATE_PREGGERS['Alabama'][chosen_index])
            self.model.rectangle2.height_adjust(-STATE_PREGGERS['Utah'][chosen_index])
            scaled_value = (float(position[0])/SIZE[0])*len(VALUES)
            self.model.rectangle.height_adjust(-100*int(scaled_value))


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