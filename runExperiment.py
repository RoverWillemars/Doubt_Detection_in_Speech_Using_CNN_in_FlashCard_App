# This file should be used to run the application.
import pygame
import os

from Application.gameHandler import *

os.chdir("./user-modelling-project-neural-navigators/")

# Setting basic variables
screenOn = True
bg_colour = (252,247,240) # Sandy white colour

# function to open the menu window; located in gameHandler.py. Returns the "screen" object, which can be manipulated here.
screen, clock = init_pygame(1024, 576)
screen.fill(bg_colour) # Change colour
pygame.display.update() # Need to update the display after changing colour for it to take effect.

tryOutPicture = pygame.image.load("./Images/Country_Outlines/afghanistan.jpg").convert_alpha()

while(screenOn == True):
    # Every loop, events from the OS (e.g. keypress, mouse movement, etc.) are collected by pygame
    pygame.event.get()

    # Checks for key press each loop
    keys = pygame.key.get_pressed()
    # If the keypress is escape, use the function quitApp (inside gameHandler.py) to escape the while loop
    if keys[pygame.K_ESCAPE]:
        screenOn = quitApp()



pygame.quit()
