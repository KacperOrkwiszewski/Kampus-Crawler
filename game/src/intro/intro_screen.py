import pygame
from PIL import Image

from sound.SoundManager import SoundManager
from sound.sound_type import MusicType

class IntroScreen:

    def __init__(self, screen):
        self.screen = screen
        self.gif_path = "src/intro/navi_intro.gif"
        self.frames, self.durations = self.load_gif_frames()

    def load_gif_frames(self):
        image = Image.open(self.gif_path)
        frames = []
        durations = []

        try:
            while True:
                frame = image.convert('RGBA')
                mode = frame.mode
                size = frame.size
                data = frame.tobytes()

                py_image = pygame.image.fromstring(data, size, mode)
                frames.append(py_image)

                duration = image.info.get('duration', 100)
                durations.append(duration)

                image.seek(image.tell() + 1)
        except EOFError:
            pass

        return frames, durations

    def _play(self):
        SoundManager.play_music(MusicType.Intro, False)
        clock = pygame.time.Clock()
        frame_index = 0
        elapsed_time = 0
        playing = True

        screen_width, screen_height = self.screen.get_size()
        frame_width, frame_height = self.frames[0].get_size()
        x = (screen_width - frame_width) // 2
        y = (screen_height - frame_height) // 2

        while playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    playing = False

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.frames[frame_index], (x, y))
            pygame.display.flip()

            duration = self.durations[frame_index]
            elapsed_time += clock.tick(1000)

            if elapsed_time >= duration:
                frame_index += 1
                elapsed_time = 0
                if frame_index >= len(self.frames):
                    playing = False

    @classmethod
    def play(cls, screen):
        cls(screen)._play()