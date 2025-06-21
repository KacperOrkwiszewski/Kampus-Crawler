from enum import Enum

class MusicType(Enum):
  Menu = 0

MUSIC_FILES = {
  MusicType.Menu: "sounds/main_menu_music.mp3"
}

class SoundType(Enum):
  Hover = 0,
  Click = 0