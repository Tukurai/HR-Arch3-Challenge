import glob
import os
import pygame


def main():
    # For testing:
    pygame.init()
    clock = pygame.time.Clock()
    sound_manager = SoundManager()

    sound_manager.play_music("mainmenu.wav")
    sound_manager.play_sfx("augh.wav")
    sound_manager.volume(-0.9)

    print(f"Current volume: {sound_manager.volume()}")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


class SoundManager(object):
    def __init__(self):
        # Setup assets folder path and init sound libraries
        current_path = os.path.dirname(os.path.dirname(__file__))

        # Init the sound libraries
        self.libraries = self.init_libraries(
            os.path.join(current_path, "Assets")
        )
        self.sfx_library = self.libraries[0]
        self.music_library = self.libraries[1]

        self.mixer = pygame.mixer.init()

    def init_libraries(self, assets_dir):
        '''
        Init the sound libraries\n
        Uses the \Assets\Music and \Assets\SFX folders!
        '''
        # Dict for library: key = str, value = dict
        sfx_library = {}
        music_library = {}

        # Paths for sound folders
        paths = {
            "sfx": os.path.join(assets_dir, "SFX"),
            "music": os.path.join(assets_dir, "Music")
        }

        for key, value in paths.items():
            if os.path.exists(value):
                # Change dir to path
                os.chdir(value)

                # Add all wav files in sfx folder to dict
                for file in glob.glob("*.wav"):
                    if key == "sfx":
                        sfx_library[file] = pygame.mixer.Sound(file)
                    else:
                        music_library[file] = file

        return sfx_library, music_library


    # TODO: Implement the sound channels n stuff :)

    def play_sfx(self, id: int):
        '''
        Play a sound effect
        '''
        pygame.mixer.Sound.play(self.sfx_library[id])

    def pause_sfx(self):
        '''
        Pause a sound effect
        '''

    def play_music(self, id: int, loops=-1, start=0.0, fade_ms=0):
        '''
        Loads and starts the music\n
        '''
        pygame.mixer.music.load(self.music_library[id])
        pygame.mixer.music.play(loops, start, fade_ms)

    def pause_all(self):
        pygame.mixer.pause()

    def volume(self, amount=0):
        '''
        amount 0 will get the current volume\n
        higher or lower will also change the current volume
        '''
        current_vol = pygame.mixer.music.get_volume()

        if amount == 0:
            return current_vol
        else:
            pygame.mixer.music.set_volume(current_vol + amount)
            return pygame.mixer.music.get_volume()

    # TODO: Add method for car sounds
    # Function assigns car sound sequence to any free mixer track
    # List of 3 sound files: rev_up, steady(repeatable) and rev_down.
    # Returns the assigned mixer track:

    def play_car_sound(self, sound_files: list):
        ...


if __name__ == "__main__":
    main()
