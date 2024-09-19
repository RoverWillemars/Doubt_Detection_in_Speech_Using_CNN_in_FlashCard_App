import pygame

# Initialize the window
def init_pygame(width, height):
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("Auditory Fact Learning")
    clock = pygame.time.Clock()
    return screen, clock

# Use this to start up the app; will bring the user to the starting menu.
def runApp():
    width = 1920
    height = 1080
    init_pygame(width, height)

# Use this to run the experiment.
def runExperiment():
    startExperiment = True
    return startExperiment

# Bring user back the main menu, from in the experiment.
def quitExperiment():
    test = 2

# Close the window fully
def quitApp():
    screenOn = False
    return screenOn

# Define class for the buttons on the main menu screen
class Button():
    def __init__(self, x, y, button_image):
        self.button_image = button_image
        self.rect = self.button_image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, screen):
        action = False # This is the variable where you can decide what the button does in the game loop. In essence, the button changes the 'action' to 'True', which is returned
                        # and can be used as a trigger for something else to happen.

        # Gets the current mouse position 
        pos = pygame.mouse.get_pos()

        # check if the mouse position is on top of the button (& if there's a click):
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw the button:
        screen.blit(self.button_image, (self.rect.x, self.rect.y))

        return action