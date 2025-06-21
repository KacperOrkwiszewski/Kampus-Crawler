import pygame.mixer
from .sound_type import *

class SoundManager:

  def init():
    SoundManager.set_music_volume(0.5)
    SoundManager.set_effect_volume(0.5)

  def play_music(type):
    pygame.mixer.music.load(MUSIC_FILES[type])
    pygame.mixer.music.play(-1) # loop back when finished

  def set_music_volume(vol):
    pygame.mixer.music.set_volume(vol)

  def stop_music():
    pygame.mixer.music.fadeout(1000) # smooth stop

  def play_effect(type):
    SOUND_EFFECTS[type].play()

  def set_effect_volume(vol):
    for sfx in SOUND_EFFECTS.values():
      sfx.set_volume(vol)