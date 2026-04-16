import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        pygame.mixer.init()
        self.tracks = [os.path.join(music_folder, f) for f in os.listdir(music_folder)]
        self.current = 0
        self.playing = False

    def play(self):
        pygame.mixer.music.load(self.tracks[self.current])
        pygame.mixer.music.play()
        self.playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False

    def next(self):
        self.current = (self.current + 1) % len(self.tracks)
        self.play()

    def previous(self):
        self.current = (self.current - 1) % len(self.tracks)
        self.play()
