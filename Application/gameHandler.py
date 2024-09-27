import pygame
import random
import speech_recognition as sr
import os
import time
from pathlib import Path

from slimstampen.spacingmodel import *

images_path = "Images/Country_Outlines"
country_files = [f for f in os.listdir(images_path)]
random.shuffle(country_files)

def getCurrentTime():
	return round(time.time()*1000)

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
    GoToMenu = True
    return GoToMenu

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
    
# Call this class to show a stimulus on the screen. Takes as input the stimulus' country first 3 letters. e.g. afghanistan = afg, belgium = bel    
class drawStimuli():
    def __init__(self, x, y, country_image, screen, scale):
        self.country_image = country_image
        self.rect = self.country_image.get_rect()
        self.rect.topleft = (x, y)
        self.country_image = pygame.transform.scale_by(self.country_image, factor = scale)
        screen.blit(self.country_image, (self.rect.x, self.rect.y)) # draw stimuli

# This class should be used to determine what the next stimuli would be. Make it based on the Slimstampen ROF variable. Currently just does it randomly.
class MemoryModel():
    def __init__(self):
        # Initiate spacing model
        self.model = SpacingModel()
        self.current_fact = None
        self.start_time = None
        self.new_fact = None
        
        # Initiate countries
        self.stim_countries = {}
        for file in country_files:
            self.stim_countries[Path(file).stem] = file
        
        # Initiate model facts
        for idx in range(len(self.stim_countries)):
            country = list(self.stim_countries.keys())[idx]
            self.model.add_fact(Fact(idx+1, country, country.lower()))
    
    # Determines the next country stimulus
    def next_country(self):
        self.start_time = getCurrentTime()
        self.current_fact, self.new_fact = self.model.get_next_fact(current_time = self.start_time)
        return self.current_fact.question

    # Returns image path for a given country
    def get_country_file_path(self, country):
        return os.path.join(images_path, self.stim_countries[country])
    
    # Returns response
    def give_answer(self, correct):
        rt = getCurrentTime() - self.start_time
        self.model.register_response(Response(self.current_fact, self.start_time, rt, correct))
    
def speech_to_text():
    try:
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "N/A"

#def determineUncertainty(): # Create a function that returns a number for the uncertainty of the answer depending on a fast fourier transform.

    
# This function uses the name of the file e.g. Afghanistan.png to check if the answer is correct. This saves us from having to save the right answers somewhere. That is why 
# The stimulus path is needed as a parameter of the function. Fortunately, in the game, the stim_path is also being used to load the image, making it easy to compare :D
def check_response(stim_path, user_response):
    split_path = stim_path.split("\\") # Splits the path e.g. \User\Documents\Picture.png into a list of 3 elements: "User", "Documents" and "Picture.png"
    last_element = split_path[-1] # Takes the last elements e.g. "Picture.png"
    split_png = last_element.split(".") # splits "Picture.png" into "Picture" and "png"
    correct_answer = split_png[0] # takes first element "Picture"

    # If the user_response is part of the file's country name (e.g. Afghanistan.png = Afghanistan), then return True. Otherwise False. 
    # This system should probably be made more fool proof. As certain countries (e.g. Chile) sounds like Chilli, which would be answered as incorrect. What can we do against this?
    if correct_answer in user_response:
        return True
    else:
        return False
