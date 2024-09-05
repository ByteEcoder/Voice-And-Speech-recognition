import speech_recognition as sr
import librosa
import numpy as np
import os

# Initialize recognizer
recognizer = sr.Recognizer()

# Paths to your reference voice sample files
reference_voice_paths = [
    "C:\\Users\\sumit\\CODING\\Sample_Wave file\\Sumit.wav",
    "C:\\Users\\sumit\\Downloads\\Voice Testing.wav",
   "C:\\Users\\sumit\\CODING\\Sample_Wave file\\1.wav",
   "C:\\Users\\sumit\\CODING\\Sample_Wave file\\2.wav",
   "C:\\Users\\sumit\\CODING\\Sample_Wave file\\3.wav",
   "C:\\Users\\sumit\\CODING\\Sample_Wave file\\4.wav",
   "C:\\Users\\sumit\\CODING\\Sample_Wave file\\5.wav",
   "C:\\Users\\sumit\\CODING\\Sample_Wave file\\6.wav",
   "C:\\Users\\sumit\\CODING\\Sample_Wave file\\7.wav",
   "C:\\Users\\sumit\\CODING\\Sample_Wave file\\8.wav",
   "C:\\Users\\sumit\\CODING\\Sample_Wave file\\9.wav",
   "C:\\Users\\sumit\\CODING\\Sample_Wave file\\10.wav"

]

# Function to load and extract MFCC features from a list of reference files
def load_reference_mfccs(paths):
    mfcc_means = []
    for path in paths:
        audio, sr_librosa = librosa.load(path, sr=None)
        mfcc = librosa.feature.mfcc(y=audio, sr=sr_librosa, n_mfcc=13)
        mfcc_mean = np.mean(mfcc, axis=1)
        mfcc_means.append(mfcc_mean)
    return np.mean(mfcc_means, axis=0)

# Load and process reference voice samples
reference_mfcc_mean = load_reference_mfccs(reference_voice_paths)

# Function to compare the reference voice with a new voice sample
def compare_voices(voice_audio, sr):
    voice_mfcc = librosa.feature.mfcc(y=voice_audio, sr=sr, n_mfcc=13)
    voice_mfcc_mean = np.mean(voice_mfcc, axis=1)
    
    # Calculate the Euclidean distance between the MFCCs of the two voices
    distance = np.linalg.norm(reference_mfcc_mean - voice_mfcc_mean)
    
    # Set a threshold for recognition (adjust for better sensitivity)
    threshold =60 # Lower threshold to increase sensitivity
    
    return distance < threshold

# Real-time voice recognition loop
while True:
    try:
        with sr.Microphone() as mic:
            # Adjust for ambient noise and listen to the input
            recognizer.adjust_for_ambient_noise(mic, duration=1)
            recognizer.pause_threshold = 1
            print("Listening...")
            audio = recognizer.listen(mic)
            
            # Recognize the speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            text = text.lower()
            if (text=="sos" or text=="help"):    # for getting location on voice recognition
                os.system('python geocode.py')
                
             # Output the recognized text to the terminal
            print(f"Recognized: {text}")
            
            # Convert audio data to floating point and normalize it
            audio_data = np.frombuffer(audio.get_wav_data(), np.int16).astype(np.float32)
            audio_data = audio_data / np.max(np.abs(audio_data))
            
            # Compare the live voice with the pre-recorded samples
            is_recognized = compare_voices(audio_data, sr=16000)  # Use the appropriate sample rate

            if is_recognized:
                print("Voice recognized.")
            else:
                print("Voice not recognized.")

    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        recognizer = sr.Recognizer()  # Reinitialize the recognizer
        continue
    
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        break
