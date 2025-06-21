from enum import Enum
import pygame.mixer

pygame.mixer.init() # forcing to initialize faster

class MusicType(Enum):
  Menu = 0,
  Intro = 1,
  Game = 2

MUSIC_FILES = {
  MusicType.Menu: "sounds/main_menu_music.mp3",
  MusicType.Intro: "sounds/intro_music.mp3",
  MusicType.Game: "sounds/game_music.mp3"
}

class SoundEffectType(Enum):
  Hover = 0,
  Click = 1,
  DoorOpen = 2,
  EctsLoss = 3,
  GameOver = 4,
  HeartLoss = 5,
  NewMessage = 6,
  TimesTicking = 7,
  WrongDoor = 8,
  Walking = 9

SOUND_EFFECTS = {
  SoundEffectType.Hover: pygame.mixer.Sound("sounds/hover_effect.mp3"),
  SoundEffectType.Click: pygame.mixer.Sound("sounds/click_effect.mp3"),
  SoundEffectType.DoorOpen: pygame.mixer.Sound("sounds/door_open_effect.mp3"),
  SoundEffectType.EctsLoss: pygame.mixer.Sound("sounds/ects_loss_effect.mp3"),
  SoundEffectType.GameOver: pygame.mixer.Sound("sounds/game_over_effect.mp3"),
  SoundEffectType.HeartLoss: pygame.mixer.Sound("sounds/heart_loss_effect.mp3"),
  SoundEffectType.NewMessage: pygame.mixer.Sound("sounds/new_message_effect.mp3"),
  SoundEffectType.TimesTicking: pygame.mixer.Sound("sounds/times_ticking_effect.mp3"),
  SoundEffectType.WrongDoor: pygame.mixer.Sound("sounds/wrong_door_effect.mp3"),
  SoundEffectType.Walking: pygame.mixer.Sound("sounds/walking_effect.mp3"),
}