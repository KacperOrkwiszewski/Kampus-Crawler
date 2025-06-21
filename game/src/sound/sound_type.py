from enum import Enum
import pygame.mixer

pygame.mixer.init() # forcing to initialize faster

class MusicType(Enum):
  Menu = 0,
  Intro = 1

MUSIC_FILES = {
  MusicType.Menu: "sounds/main_menu_music.mp3",
  MusicType.Intro: "sounds/intro_music.mp3",
}

class SoundEffectType(Enum):
  Hover = 0,
  Click = 1

SOUND_EFFECTS = {
  SoundEffectType.Hover: pygame.mixer.Sound("sounds/hover_effect.mp3"),
  SoundEffectType.Click: pygame.mixer.Sound("sounds/click_effect.mp3")
}