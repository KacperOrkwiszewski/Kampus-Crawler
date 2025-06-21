import pygame.mixer
from .sound_type import *

class SoundManager:
  def play_music(type):
    pygame.mixer.music.load(MUSIC_FILES[type])
    pygame.mixer.music.play(-1) # loop back when finished

  def set_music_volume(vol):
    pygame.mixer.music.set_volume(vol)

  def stop():
    pygame.mixer.music.fadeout(1000) # smooth stop