from os import getcwd, path
import pygame


def main():
    pygame.init()
    clock = pygame.time.Clock()
    sound_manager = SoundManager()

    print("augh")

    while True:
        sound_manager.play_sound(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


class SoundManager(object):

    # Creates object if it does not exist. Else returns instance.
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SoundManager, cls).__new__(cls)
            cls.mixer = pygame.mixer.init()
            cls.sound_library = cls.init_library(cls)

        return cls.instance

    def init_library(cls):

        # List of sound file names (hardcoded atm)
        sound_files = [
            "augh.wav"
        ]

        # Dict for sound library: key = int, value = sound obj
        sound_lib = {}

        for index in range(len(sound_files)):
            # Create path for sound file directory
            file_path = getcwd() + "\Sounds\\" + sound_files[index]

            # Add sound files to dict as sound object
            if path.exists(file_path):
                sound_lib[index] = pygame.mixer.Sound(getcwd() + "\Sounds\\" + sound_files[index])
            else:
                print(f"Sound file not found: {file_path}")
        
        return sound_lib

    def play_sound(cls, id: int):
        pygame.mixer.Sound.play(cls.sound_library[id])
        pygame.mixer.music.stop()


if __name__ == "__main__":
    main()