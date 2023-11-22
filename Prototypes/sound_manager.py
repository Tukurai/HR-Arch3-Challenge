import glob
import os
import pygame


def main():
    pygame.init()
    clock = pygame.time.Clock()
    sound_manager = SoundManager()

    sound_manager.play_music(0)
    sound_manager.play_sfx(0)
    sound_manager.volume(-0.9)

    print(f"Current volume: {sound_manager.volume()}")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


class SoundManager(object):
    assets_dir = os.path.abspath(os.path.join(
        os.getcwd(), os.pardir)) + "\Assets"

    # Creates object if it does not exist. Else returns instance.
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SoundManager, cls).__new__(cls)

            cls.mixer = pygame.mixer.init()

            libraries = cls.init_libraries(cls)
            cls.sfx_library = libraries[0]
            cls.music_library = libraries[1]

        return cls.instance

    def init_libraries(cls):
        '''
        Init the sound libraries\n
        Uses the \Assets\Music and \Assets\SFX folders!
        '''
        # Dict for library: key = str, value = dict
        sfx_library = {}
        music_library = {}

        # Paths for the folders
        paths = {
            "sfx": cls.assets_dir + "\SFX\\",
            "music": cls.assets_dir + "\Music\\"
        }

        for key, value in paths.items():
            if os.path.exists(value):
                # Change dir to path
                os.chdir(value)

                # Add all wav files in sfx folder to dict
                index = 0
                for file in glob.glob("*.wav"):
                    if key == "sfx":
                        sfx_library[index] = pygame.mixer.Sound(file)
                    else:
                        music_library[index] = file

                    index += 1

        return sfx_library, music_library

    def play_sfx(cls, id: int):
        '''
        Play a sound effect
        '''
        pygame.mixer.Sound.play(cls.sfx_library[id])

    def play_music(cls, id: int, loops=-1, start=0.0, fade_ms=0, action="start"):
        '''
        start, pause or stop the music\n
        loops=-1 infinitly loops the music, other amounts will loop the given amount
        '''
        if action == "start":
            pygame.mixer.music.load(cls.music_library[id])
            pygame.mixer.music.play(loops, start, fade_ms)
        elif action == "pause":
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.stop()

    def volume(cls, amount=0):
        '''
        amount 0 will get the current volume\n
        higher or lower will also change the current volume
        '''
        current_vol = pygame.mixer.music.get_volume()

        if amount == 0:
            return current_vol
        else:
            pygame.mixer.music.set_volume(current_vol + amount)
            return pygame.mixer.music.get_volume


if __name__ == "__main__":
    main()
