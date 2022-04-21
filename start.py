#!/bin/python

import os
import subprocess
import time 

# import required libraries
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

# speech recoganition
import speech_recognition as sr

# lemmatization
import nltk
import os


sgnFiles = os.listdir('./SignFiles/')
sgnFiles = [ name[:-6] for name in sgnFiles ]

availTokens = set(sgnFiles)

nullfile = open('/dev/null', 'w')

def giveSign(input:str):
    if input in availTokens:
        os.system('timeout 1s nc localhost 8052 < SignFiles/' + input + '.sigml 2>&1 > /dev/null')
    else:
        for l in input:
            os.system('timeout 1s nc localhost 8052 < SignFiles/' + l.upper() + '.sigml 2>&1 > /dev/null')

def runApp():
    subprocess.Popen('./sigml-render', stdout=nullfile, stdin=nullfile)
    time.sleep(3)


def recordAudio(filename:str, dur:int): 
    print('now recording!')
    # Sampling frequency
    freq = 44100
    
    # Recording duration
    duration = dur
    
    # Start recorder with the given values 
    # of duration and sample frequency
    recording = sd.rec(int(duration * freq), 
                       samplerate=freq, channels=2)
    
    # Record audio for the given number of seconds
    sd.wait()
 
    # Convert the NumPy array to audio file
    wv.write(filename, recording, freq, sampwidth=2)

def recoganize(filename:str):
    # initialize the recognizer
    r = sr.Recognizer()

    text = 'what'
    try:
        with sr.AudioFile(filename) as source:
            # listen for the data (load audio to memory)
            audio_data = r.record(source)
            # recognize (convert from speech to text)
            text = r.recognize_google(audio_data)
            print(text)
    except:
        print('Can\'t hear!, try Again!')
    return text


exist = os.path.exists('./sigml-render')
if not exist:
    print('extracting client renderer!')
    os.system('rar e sigml-render.rar')

runApp()
while True:
    print('waiting for input')
    input()
    recordAudio('rec.wav', 5)
    text = recoganize('rec.wav')
    words = nltk.word_tokenize(text)

    for w in words:
        giveSign(w.lower())
