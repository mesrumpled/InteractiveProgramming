""" labelDemo.py
    creating a basic label sprite"""
    
import pygame
pygame.init()

# screen = pygame.display.set_mode((640, 480))    
    
class Label(pygame.sprite.Sprite):
    """ Label Class  
        Attributes:
            font: any pygame Font or SysFont objects
            text: text to display
            center: desired position of label center (x, y)
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("None", 30)
        self.text = ""
        self.center = (320, 240)
                
    def update(self):
        self.image = self.font.render(self.text, 1, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.center
        
# def main():
#     pygame.display.set_caption("Label demo")
    
#     background = pygame.Surface(screen.get_size())
#     background.fill((255, 255, 255))
#     screen.blit(background, (0, 0))
    
#     label1 = Label()
#     label2 = Label()
#     labelEvent = Label()
#     allSprites = pygame.sprite.Group(label1, label2, labelEvent)
    
#     label1.text = "Hi. I'm a label."
#     label1.center = (100, 100)
    
#     label2.text = "I'm another label."
#     label2.center = (400, 400)
    
#     clock = pygame.time.Clock()
#     keepGoing = True
#     while keepGoing:
#         clock.tick(30)
        
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 keepGoing = False
#             elif event.type == pygame.MOUSEMOTION:
#                 (mouseX, mouseY) = pygame.mouse.get_pos()
#                 labelEvent.text = "mouse: (%d, %d)" % (mouseX, mouseY)
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 labelEvent.text = "button press"
#             elif event.type == pygame.KEYDOWN:
#                 labelEvent.text = "key down"
        
#         allSprites.clear(screen, background)
#         allSprites.update()
#         allSprites.draw(screen)
        
#         pygame.display.flip()





import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEMOTION
import time
import csv
import random

pygame.init()


def generate_rates(f):
    """Generates a dictionary containing the rates for each element in the data set"""
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
    """Generates a color for each element in the data set"""
    colors = {}
    for s in d:
        colors[s] = (random.randint (2,255), random.randint (2,255), random.randint (2,255))
    return colors


STATE_RATES = generate_rates('CleanedUpData_noyear.csv')

SIZE = (1700, 1040)

STATE_COLORS = generate_colors(STATE_RATES)

print STATE_RATES.keys()[0]
print STATE_COLORS.keys()[0]



class View(object):
    """visualizes the data and labels"""
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen

    def draw(self):
        self.screen.fill(pygame.Color('white'))
        for state in self.model.states_rect:
            pygame.draw.rect(self.screen, pygame.Color(*STATE_COLORS[state]), self.model.states_rect[state])
        self.screen.blit(model.title, (SIZE[0]/2.0,SIZE[1]/9.0))
        self.screen.blit(model.astate, (200, 200))
        pygame.display.update()



class Model(object):
    def __init__(self):
        self.states_rect = {}
        for i, state in enumerate(STATE_RATES):
            if i < 1:
                print state
            self.states_rect[state] = pygame.Rect(i*(SIZE[0]/50.0) + 10, 600, (SIZE[0]/50.0-20), 0)

        freetypeT = pygame.font.SysFont("serif", 72)
        self.title = freetypeT.render("Hi", True, (0, 128, 0))

        freetype = pygame.font.SysFont("serif", 24)
        self.astate = freetype.render(STATE_RATES.keys()[0], True, STATE_COLORS.values()[0])
        self.astate = pygame.transform.rotate(self.astate, 90)
        
    def update(self, position):
        # Update all model attributes based on the position of the mouse
        for state in STATE_RATES:
                scaled_value = (float(position[0])/SIZE[0])*len(STATE_RATES[state])
                chosen_index = int(scaled_value)
                self.states_rect[state].height = (-5*float(STATE_RATES[state][chosen_index]))
        

        
class MouseController(object):
    def __init__(self, model):
        self.model = model

    def handle_event(self, event):
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
    


