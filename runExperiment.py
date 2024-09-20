# This file should be used to run the application.
import pygame
import os

from Application.gameHandler import *

os.chdir("./user-modelling-project-neural-navigators/")

# Setting basic variables
screen_width = 1024
screen_height = 576
screenOn = True
bg_colour = (252,247,240) # Sandy white colour
experimentOn = False #starts false to get the user to the menu, when experiment starts, this is changed to true.
runApp = True

# function to open the menu window; located in gameHandler.py. Returns the "screen" object, which can be manipulated here.
screen, clock = init_pygame(screen_width, screen_height)

# Load in assets
image_play = pygame.image.load("./Images/UI_features/Play.png").convert_alpha()
image_exit = pygame.image.load("./Images/UI_features/Exit.png").convert_alpha()
#menu_image = pygame.image.load("./Images/...").convert_alpha()

# Create button instances
button_play = Button((screen_width/2)-200, (screen_height/2)-(screen_height)/5, image_play)
button_exit = Button((screen_width/2)-200, (screen_height/2)+(screen_height)/6, image_exit)

# Create stimuli instance
#stimuli((screen_width/2)-200, (screen_height/2)-(screen_height)/5, getStimuli())

while(runApp == True):
    while(screenOn == True):
        screen.fill(bg_colour) # Change colour
        if button_play.draw(screen) == True:
            screenOn = quitApp()
            experimentOn = runExperiment()
        if button_exit.draw(screen) == True:
            screenOn = quitApp()
            runApp = quitApp()


        # Every loop, events from the OS (e.g. keypress, mouse movement, etc.) are collected by pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # This gets called when you press the "x" button on the top right of the window.
                screenOn = quitApp()
                runApp = quitApp()
            keys = pygame.key.get_pressed() # Checks for key press each loop. "keys" will keep track of each key press
            if keys[pygame.K_ESCAPE]: # If the keypress is escape, use the function quitApp (inside gameHandler.py) to escape the while loop
                screenOn = quitApp() # quitApp() is a function in gameHandler.py
                runApp = quitApp()

        pygame.display.update()
    
    # Starting variables for the experiment:
    trial = 0 

    while(experimentOn == True):
        if trial == 0:
            screen.fill(bg_colour)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # This gets called when you press the "x" button on the top right of the window.
                screenOn = quitExperiment()
                experimentOn = False

            keys = pygame.key.get_pressed() # Checks for key press each loop. "keys" will keep track of each key press

            if keys[pygame.K_ESCAPE]:
                screenOn = quitExperiment()
                experimentOn = False

            if keys[pygame.K_RETURN]: # If you press enter, continue to next trial. This will need to be changed to a system that checks if user_answer == correct_answer
                stim_path = getStimuli().get_country_path()
                stim_image = pygame.image.load(f"{stim_path}").convert_alpha()

                pygame.time.wait(2000)

                drawStimuli(x = 337, y = 0, country_image = stim_image, screen = screen, scale = 0.5) # Draws stimulus. scale changes the size of the stimulus. However, if you change scale, also change x & y coord

                trial = trial + 1 # Currently uses this to keep track of trial, as there is no correct/incorrect of the trial yet.
                print(trial)
        pygame.display.update()

pygame.quit()
