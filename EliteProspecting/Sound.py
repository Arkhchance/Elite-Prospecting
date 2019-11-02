#!/usr/bin/python
import os
import threading
try:
    from playsound import playsound
    audio = True
except ImportError:
    audio = False


class Sound():
    def __init__(self):
        self.audio_available = audio
        self.sound_file = os.path.dirname(os.path.realpath(__file__))
        self.sound_file += "/sound/ding.wav"

    def play(self):
        if self.audio_available:
            threading.Thread(target=self.play_sound).start()

    def play_sound(self):
        playsound(self.sound_file)
