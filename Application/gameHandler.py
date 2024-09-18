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
    test = 1

# Bring user back the main menu, from in the experiment.
def quitExperiment():
    test = 2

# Close the window fully
def quitApp():
    screenOn = False
    return screenOn