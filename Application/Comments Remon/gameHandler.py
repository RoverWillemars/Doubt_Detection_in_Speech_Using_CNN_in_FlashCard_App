import pygame
import random
import speech_recognition as sr

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
# Edit Remon: needs to be integrated with the spacingmodel.get_next_fact() function
class getStimuli():
    def __init__(self):
        self.stim_countries = ["Afghanistan", "Argentina", "Belgium"] # saf = south africa. Would be nice to implement the json file here

    def get_country_path(self):
        # Edit Remon start: this is just a suggestion, I'm not sure whether this would work
        #selected_country = random.choice(self.stim_countries) <-- commented out
        time_start_trial = time_since_start_inMS # need a tracker of the time since start learning session, in Milli Seconds --> also shouldnt put this here ofcourse
        next_fact, new = m.get_next_fact(current_time = time_start_trial) 
        # this also returns a Boolean indiciating whether the returned fact is new (True), we can use this to create a different presentation of the fact
        
        # get fact_id from the next fact, then retrieve element from list and return the directory, need to implement the json file here.
        next_fact_id = next_fact.fact_id
        selected_country = self.stim_countries[next_fact_id] # make sure to start fact_id from zero
        # Edit Remon end
        return f".\Images\Country_Outlines\{selected_country}.jpg" # returns the directory of the country.
    
def speech_to_text():
    try:
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        
     # Edit Remon: As soon as the recording stops the time should be recorded in 'time_after_speech = time_since_start_inMS'   
            
        return f"Answer: {r.recognize_google(audio)}"
    except sr.UnknownValueError:
        return f"No words could be analysed from your speech"
    
# This function uses the name of the file e.g. Afghanistan.png to check if the answer is correct. This saves us from having to save the right answers somewhere. That is why 
# The stimulus path is needed as a parameter of the function. Fortunately, in the game, the stim_path is also being used to load the image, making it easy to compare :D
# Edit Remon: might want to integrate this with the spacingmodel.register_response() function and Response object
def check_response(stim_path, user_response):
    split_path = stim_path.split("\\") # Splits the path e.g. \User\Documents\Picture.png into a list of 3 elements: "User", "Documents" and "Picture.png"
    last_element = split_path[-1] # Takes the last elements e.g. "Picture.png"
    split_png = last_element.split(".") # splits "Picture.png" into "Picture" and "png"
    correct_answer = split_png[0] # takes first element "Picture"

    # If the user_response is part of the file's country name (e.g. Afghanistan.png = Afghanistan), then return True. Otherwise False. 
    # This system should probably be made more fool proof. As certain countries (e.g. Chile) sounds like Chilli, which would be answered as incorrect. What can we do against this?
    if correct_answer in user_response:
        # edit Remon: register response in model, the variables don't exist locally rn so they need to be added to the function or we need to do it another way
        resp = Response(fact = next_fact, start_time = time_start_trial, rt = time_after_speech - me_start_trial, correct = True) # could also make a seperate variable of rt
        m.register_response(resp)
        
        return True
    else:
        # edit Remon: register response in model
        resp = Response(fact = next_fact, start_time = time_start_trial, rt = time_after_speech - me_start_trial, correct = False)
        m.register_response(resp)
        
        return False
