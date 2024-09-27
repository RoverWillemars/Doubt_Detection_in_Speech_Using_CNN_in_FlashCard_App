# This file should be used to run the application.
import pygame
import os

from Application.gameHandler import *

#os.chdir("./user-modelling-project-neural-navigators/")

# Initiate model
model = MemoryModel()

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
    answer = None # No answer has been given yet.
    font = pygame.font.SysFont(None, 25)

    while(experimentOn == True):
        screen.fill(bg_colour)
        pygame.display.update()

        # add a system that introduces new facts.

        if trial > 0:
			# Determine the next country
            stimulus = model.next_country()
            print(stimulus)
			
			# Load the country image into PyGame
            stim_path = model.get_country_file_path(stimulus)
            stim_image = pygame.image.load(f"{stim_path}").convert_alpha()

			# Draw the country image
            drawStimuli(x = 337, y = 20, country_image = stim_image, screen = screen, scale = 0.5) # Draws stimulus. scale changes the size of the stimulus. However, if you change scale, also change x & y coord
            pygame.display.update()
            
            if answer == None:
				# Determine answer from speech
                answer = speech_to_text() # Uses the speech_to_text function in gameHandler to return the transcription of what has been spoken
                text = font.render(f"Answer: {answer}", True, (0,0,255)) # Sets the font, maybe place somewhere else? Or is it needed? idk
                screen.blit(text, (screen_width/2, 500)) # draw the spoken text (transcription) on screen. in the brackets are the x&y coordinates.
                pygame.display.update()

				# Check if answer is correct
                user_feedback = False
                if stimulus == answer:
                    user_feedback = True
                    
                # Update memory model
                model.give_answer(user_feedback)

                pygame.time.wait(100)

                if user_feedback == True:
                    pygame.draw.circle(screen, (0,128,0), (screen_width/2, screen_height/2), 10)
                else:
                    pygame.draw.circle(screen, (128,0,0), (screen_width/2, screen_height/2), 10)

                pygame.display.update()
                answer = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # This gets called when you press the "x" button on the top right of the window.
                screenOn = quitExperiment()
                experimentOn = False

            keys = pygame.key.get_pressed() # Checks for key press each loop. "keys" will keep track of each key press

            if keys[pygame.K_ESCAPE]:
                screenOn = quitExperiment()
                experimentOn = False
        
        trial = trial + 1

        pygame.time.wait(2000) # wait 2000ms, maybe redundant?

pygame.quit()
