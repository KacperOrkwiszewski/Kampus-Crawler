from PIL import Image
import pygame

class PlayerImageInfo:
    def __init__(self, gif_path, movement_speed):
        # Load all frames from the GIF file
        self.frames = self.load_gif_frames(gif_path)
        self.frame_index = 0  # Index of the current frame
        # Lower value means faster animation
        self.animation_speed = 0.2 / movement_speed  # Animation speed depends on movement speed
        # Slower animation for idle.gif
        if gif_path.startswith('idle'):
            self.animation_speed = 0.5
        self.time_since_last_frame = 0.0  # Time since last frame update

        # Set final scaled width and height (from the first frame)
        self.scale_size_x = self.frames[0].get_width()
        self.scale_size_y = self.frames[0].get_height()

    def load_gif_frames(self, gif_path):
        # Open the GIF using PIL
        pil_image = Image.open(gif_path)
        frames = []

        scale_x = 80  # Target width
        scale_y = 80  # Target height

        try:
            while True:
                # Convert the current frame to RGBA format
                frame = pil_image.convert('RGBA')
                mode = frame.mode
                size = frame.size
                data = frame.tobytes()
                # Convert PIL image data to Pygame surface
                pygame_image = pygame.image.fromstring(data, size, mode)
                # Scale the frame to the desired size
                pygame_image = pygame.transform.scale(pygame_image, (scale_x, scale_y))
                # Add the scaled frame to the list
                frames.append(pygame_image)
                # Move to the next frame
                pil_image.seek(pil_image.tell() + 1)
        except EOFError:
            pass

        # Store scaled size (used for centering)
        self.scale_size_x = scale_x
        self.scale_size_y = scale_y

        return frames

    def get_current_frame(self, dt):
        # Increase time since last frame by the delta time
        self.time_since_last_frame += dt
        # If it's time to change the frame
        if self.time_since_last_frame >= self.animation_speed:
            # Move to the next frame (loop back to start if needed)
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.time_since_last_frame = 0
        # Return the current frame surface
        return self.frames[self.frame_index]
