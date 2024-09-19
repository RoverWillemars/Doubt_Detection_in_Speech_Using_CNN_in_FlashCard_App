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

# function to open the menu window; located in gameHandler.py. Returns the "screen" object, which can be manipulated here.
screen, clock = init_pygame(screen_width, screen_height)
screen.fill(bg_colour) # Change colour
pygame.display.update() # Need to update the display to make sure background colour changes.

# Load in assets
image_play = pygame.image.load("./Images/UI_features/Play.png").convert_alpha()
image_exit = pygame.image.load("./Images/UI_features/Exit.png").convert_alpha()
#menu_image = pygame.image.load("./Images/...").convert_alpha()

# Create button instances
button_play = Button((screen_width/2)-200, (screen_height/2)-(screen_height)/5, image_play)
button_exit = Button((screen_width/2)-200, (screen_height/2)+(screen_height)/6, image_exit)

while(screenOn == True):
    if button_play.draw(screen) == True:
        screenOn = quitApp()
        experimentOn = runExperiment()
    if button_exit.draw(screen) == True:
        screenOn = quitApp()

    # Every loop, events from the OS (e.g. keypress, mouse movement, etc.) are collected by pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # This gets called when you press the "x" button on the top right of the window.
            screenOn = quitApp()
        keys = pygame.key.get_pressed() # Checks for key press each loop. "keys" will keep track of each key press
        if keys[pygame.K_ESCAPE]: # If the keypress is escape, use the function quitApp (inside gameHandler.py) to escape the while loop
            screenOn = quitApp() # quitApp() is a function in gameHandler.py

    pygame.display.update()

screen.fill(1,0,0) # Change colour

while(experimentOn == True):

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # This gets called when you press the "x" button on the top right of the window.
            screenOn = quitApp()
        keys = pygame.key.get_pressed() # Checks for key press each loop. "keys" will keep track of each key press
        if keys[pygame.K_ESCAPE]: # If the keypress is escape, use the function quitApp (inside gameHandler.py) to escape the while loop
            screenOn = quitApp() # quitApp() is a function in gameHandler.py
    pygame.display.update()

pygame.quit()
