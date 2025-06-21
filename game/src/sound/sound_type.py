from enum import Enum
import pygame.mixer

pygame.mixer.init() # forcing to initialize faster

class MusicType(Enum):
  Menu = 0

MUSIC_FILES = {
  MusicType.Menu: "sounds/main_menu_music.mp3"
}

class SoundEffectType(Enum):
  Hover = 0,
  Click = 0

SOUND_EFFECTS = {
  SoundEffectType.Click: pygame.mixer.Sound("sounds/click_effect.mp3")
}