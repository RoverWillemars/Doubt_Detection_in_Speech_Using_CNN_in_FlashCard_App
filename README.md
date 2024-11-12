# Main idea
Adaptive fact learning system that incorporates speech analysis to track confidence/uncertainty of facts. By using already existing speech recognition/transcription software, the system evaluates whether the answer is correct or not. This is nothing new of course, therefore, our system additionally investigates the Mel spectograms using a CNN to recognize doubt in the answer. We then want to implement this as an additional parameter in the decay of activation " $$d_i(t)=c∗e^{A(t−1)}+α$$ ", that interacts with _α_. By doing so, we hope to optimize the timing of repeated presentation of an item even better. 

# Algorithm
**Prosodic Analysis**

Prosodic features include elements like pitch (fundamental frequency), speech rate, intonation, loudness, and pause patterns. Changes in these features can indicate a speaker's emotional state, including confidence.

**Key Features:**

* Pitch: Confident speakers tend to have more controlled and stable pitch. Nervous or uncertain speakers may exhibit pitch variability.
* Speech Rate: Confident speakers often maintain a steady speech rate, while hesitant or uncertain individuals may have slower or more erratic speech patterns.
* Loudness: Confident speakers are generally louder and more assertive, while less confident individuals may speak more quietly.

**Algorithms:**

* Support Vector Machines (SVMs): Applied to prosodic features for classification of confident vs. non-confident speech.
* Mel-frequency cepstral coefficients (MFCCs) and spectral properties can be used to train machine learning models for detecting confidence.
* Convolutional Neural Network (CNN): CNNs are often used for tasks like audio classification, where they can learn to recognize patterns in spectrograms (visual representations of sound) or directly from raw audio data.

MFCC is used as first step in any automatic speech recognition. Short term power spectrum of any sound represented by the Mel frequency cepstral (MFC) and combination of MFCC makes the MFC. It can be derived from a type of inverse Fourier transform(cepstral) representation. MFC allows a better representation of sound because in MFC the frequency bands are equally distributed on the Mel scale which approximates the human auditory system’s response more closely.


To get starting data we recorded users using the app and label the responses. This allowed us to get data containing sincere doubt without faking it. We use Speech Recognition python library to transcribe speech and extract features. We tried to use SVM to classify these features of speech into confident or doubtful. However, SVM performance was poor and because of that we decided to use Convolutional Neural Network (CNN) instead. We implemented a CNN to predict whether an audio sample is confident or doubtful based on the audio features. Here's how it works:
1. Feature Extraction: We extract Mel spectrograms from the audio files as input to the CNN. Mel spectrograms are a visual representation of the frequency spectrum of audio over time, and they work well for audio classification tasks with CNNs.
2. CNN Model: The CNN architecture is designed to process the spectrograms and make predictions. The CNN consists of multiple convolutional layers  followed by pooling layers to progressively reduce the dimensionality of the input.
3. Training: The CNN will be trained on the extracted features from confident and doubtful audio files.
4. Fine tuning: We will fine tune our model on the subject after the first block of trials where the participant has to indicate confidence of their answers. Fine-tuning it on a particular subject dataset by continuing training on new data with a reduced learning rate and fewer epochs allows us to avoid overfitting and avoid overwriting previously learned features.
5. Prediction: Once trained, the model will predict the confidence level of new audio files (either confident or doubtful). 

This CNN-based approach provided us with better accuracy than the SVM, we believe the reason is that CNNs are adept at learning from spectrograms, which capture both time and frequency characteristics of the audio data.

## Incorporating a user model
The adaptive fact learning system itself is based on SlimStampen/MemoryLab ([original paper](https://research.rug.nl/en/publications/predicting-university-students-exam-performance-using-a-model-bas)), which incorporates a user model through the form of a computational cognitive model based on the ACT-R framework ([book](https://academic.oup.com/book/4367)). Each fact that is learned when using the learning system is represented by a *chunk* $i$ that has a level of *activation* $A_i(t)$:

$$A_i(t) = \ln\left( \sum^n_{j=1} t_j^{-d_i(t)} \right)$$

The level of activation $A_i$ at time $t$ is determined by both the sum of $n$ previous encounters ($t_1, ..., t_n$ seconds ago) and the *decay* of activation $d(t)$, which is expressed through the formula:

$$d_i(t)=c∗e^{A(t−1)}+α$$

The model adapts the estimated decay of a chunk for a given user by estimating the value for the rate of forgetting $\alpha$ for a chunk. Then, by using a scheduling algorithm that determines which chunks are the mostly likely to be forgotten the soonest, facts (or chunks) will be presented in such a way that facts will be remembered optimally over time.

Given that a person's regular speech patterns are likely to be unique for any given person, the system needs to be able to track the baseline for the prosodic features of a person's speech. This creates a user model within the system that can be used to determine when a person's speech patterns diverge from their baseline. A possible way to do this is by estimating and continuously updating a distribution for each prosodic feature of a given person's speech patterns during learning. Then, by setting a threshold for each distribution, e.g. when a given value is $i\sigma$ apart from the mean in a normal distribution, diverging values of specific prosodic features can be detected when they cross the threshold. Depending on how far a value diverges from the mean, a confidence level can be determined for each prosodic feature.

Things to be taken into account:
- How can the confidence levels of the speech patterns be incorporated into the adaptive fact learning system? Can the confidence levels influence the change in the rate of forgetting $\alpha$? Or is an additional parameter needed for the decay formula (or elsewhere in the system)?
- How do the confidence levels of the speech patterns influence the user model, when a wrong answer is given during learning? E.g. if the confidence level is high while the answer is wrong, should this be represented in the cognitive model as more likely to be forgotten than when the confidence level is low?

For the final model, we decided to add a doubt-detection parameter (δ) in the form of a multiplier for the RoF (_α_):

$$d_i(t)=c∗e^{A(t−1)}+α∗δ(l)$$

The values the doubt detection parameter can take, given the answer and doubt-classification, are shown below:

![image](https://github.com/user-attachments/assets/ca270451-5456-47d3-94f6-10c0a3bba27a)

# User interface

### General UI Decisions:
For the User Interface design, we decided to keep the layout minimalistic to reduce the amount of visual distractions on the page. Additionally, the colours used will be in a muted tone to help with this effect. However, if the app tries to communicate something important to the user (e.g. Correct/Incorrect response), this information will be provided in a more pronounced colour to try and point attention towards that message. 

### Task UI:

The main focus of the task UI is to present the stimuli with little distraction. This is done by only including the stimuli in addition to a response box that actively records the microphone input and shows what is being picked up in text. (e.g. in the picture below, the user has said "Indonesia" out loud.)

![presentationofcountry](https://github.com/user-attachments/assets/7c5d4051-5df1-45ef-a631-87974c4f1626)


#### Stimuli:

For this experiment, we have chosen outlines of countries to be the stimuli. The user will have to vocally respond with the name of the country to get the trial correct.

#### Feedback to the User:

The task provides feedback to the user to signal if their response was correct/incorrect.

![correct](https://github.com/user-attachments/assets/09137f1d-757d-43fe-9810-4c43e83f18e7)
![answer took too long](https://github.com/user-attachments/assets/302c6547-2ebd-4887-8294-845b766c0e0f)


If the user gets the answer wrong, the correct response is shown in the response box and played into the headphones once again.

#### Indicate Doubt prompt

During the first block, after each trial of non-new stimuli, the user is prompted to indicate whether they were doubtful/confident: 

![udoubtful](https://github.com/user-attachments/assets/8508fbc6-b41b-44a6-b885-b22537efb943)


# Experiment design

Before the trials of the experiment start, the participant will be given 5 question they have to type in (for the purpose of gathering information about the participant demographics):
- "What is your age?"
- "What gender do you identify as?"
- "What nationality are you?"
- "How familiar are you with geography?"

After the answers to these questions have been typed in, the participant will be presented with a screen that gives an explanation about the upcoming trial. During the experiment, the mastery of facts will be measured by determining whether the activation of a fact is still above the forget threshold after 10 minutes (the length of a block). The time it takes for a participant to reach mastery will be used as the metric to compare the systems/check the manipulation.

## Blocks
Using a within-subject design, the experiment will consist of 3 blocks of trials. The first block is a training and fine-tuning block, whereas the second and third blocks use the standard and doubt-detection system, of which the order is chosen randomly. Three different sets of stimuli have been prepared, with the first block having twenty stimuli and the second and third both consisting of fifteen different stimuli, and no two sets sharing identical stimuli. The first block will always have the same stimuli set for each participant (_training set_). The order of the stimuli set for the second and third blocks is chosen randomly. 

- **Block 1**: _Familiarization and fine-tuning the doubt detection model_  
In this block, participants get accustomed to the experimental setup and the task at hand. Stimuli will keep being presented until 15 minutes after the start of the block. After a previously presented stimulus is shown, the participant will be prompted to decide whether they felt 'confident' or 'doubtful' about their answer. After this block has ended, the audio recordings of this block's trials and their respective prompted confidence answer will be used to fine-tune the doubt detection model to the participant's voice. The reaction time and rate of forgetting for each trial that is measured within this block will be assumed to be purely preparatory and not included in the final results.  
Two types of trials can occur:
    1. (_A stimulus has NOT been presented before_)  
        - The name of the shown country is given at the start.  
        - Text-to-speech is used to show how to pronounce the name of the shown country.
        - Whenever the 'Space' key is pressed --> the trial ends
    2. (_A stimulus has been presented before_)  
        - The name of the shown country is hidden.  
        - The start time of the trial is measured.  
        - Whenever the 'Space' key is pressed  
--> the reaction time of the trial is calculated (time of pressing 'Space' - start time trial) and the participant should use the microphone to give the name of the shown country.  
        - When the participant is finished speaking the name into the microphone  
--> both the correct answer and the participant's answer are shown, with the correctness of the participant's answer (red: incorrect answer, green: correct answer)
        - When the participant is finished speaking  
--> a prompt will be shown in which the participant has to state whether they were feeling 'confident' (by pressing 'A') or 'doubtful' (by pressing 'L') about their answer, after which the trial ends
        - Notes:
            - The participant has to start speaking WITHIN 3 seconds (this is to prevent cheating by staying silent until the participant remembers the answer from a previous encounter of the current stimulus)  
--> otherwise, an error and the correct answer will be given, while the participant's answer will be assumed as incorrect 
            - When the participant start speaking, they have 4 seconds to finish their phrase (this is to prevent cheating by speaking slowly until the participant remembers the answer from a previous encounter of the current stimulus)  
--> otherwise, an error and the correct answer will be given, while the participant's answer will be assumed as incorrect  
- **Block 2/3**: _Adaptive fact learning (WITH doubt detection)_  
In this block, participants do the same types of trials as in the first block, but with 3 major differences:
    1. Reaction times and rates of forgetting from facts in this block will be measured and used in the final results.
    2. No prompt will be shown that asks the participant for whether they felt 'confident' and 'doubtful' about their answers
    3. The fine-tuned doubt detection model will determine whether the participant felt 'confident' or 'doubtful' about their answer using the respective audio recording. Based on the output of the model ('confident' or 'doubtful') and the correctness of the participant's answer ('correct' or 'wrong'), the rate of forgetting ($\alpha$) for the current presented stimulus will be adjusted by multiplying with the relevant doubt modifier.
- **Block 2/3**: _Adaptive fact learning (WITHOUT doubt detection)_  
This block will be the same as block the doubt-detection block, but without adjusting the rate of forgetting for stimuli through the fine-tuned doubt detection model.


### Trial Overview

The figure below depicts the trial overview. 

![image](https://github.com/user-attachments/assets/637372a2-63ad-4a1b-9c59-b25db6201754)

