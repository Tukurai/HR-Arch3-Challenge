import glob
import os
import time
import pygame


def main():
    # For testing:
    pygame.init()
    clock = pygame.time.Clock()
    sound_manager = SoundManager()

    sound_manager.play_music("mainmenu.wav")
    sound_manager.play_sfx("augh.wav")



    while True:
        for event in pygame.event.get():
            speed = 0.0
            max_speed = 1.0

            car_sounds = ["car1_rev_up", "car1_driving", "car1_rev_down", "car1_idle"]

            # ??????????????????????????????????????????
            if event.type == pygame.KEYDOWN:
                print("A key has been pressed!")
                if event.key == pygame.K_UP:
                    if speed < max_speed:
                        speed += 0.01
                    print("UP")
                    sound_manager.play_car_sound(speed, max_speed, car_sounds)
                else:
                    if speed > 0:
                        speed -= 0.01

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


class SoundManager():
    def __init__(self, channels=10):
        '''
        Init the sound manager with the amount of mixer channels (10 default)
        '''
        # Setup assets folder path and init sound libraries
        current_path = os.path.dirname(os.path.dirname(__file__))

        # Init the sound libraries
        self.libraries = self.init_libraries(
            os.path.join(current_path, "Assets")
        )
        self.sfx_library = self.libraries[0]
        self.music_library = self.libraries[1]

        self.mixer = pygame.mixer.init()
        pygame.mixer.set_num_channels(channels)

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

    def play_sfx(self, sfx_file: str):
        '''
        Play a sound effect on an available channel
        '''
        self.sfx_library[sfx_file].play()

    def pause_sfx(self, sfx_file: str):
        '''
        Pause a sound effect
        '''
        self.sfx_library[sfx_file].pause()

    def stop_sfx(self, sfx_file: str):
        '''
        Stop a sound effect
        '''
        self.sfx_library[sfx_file].stop()

    def volume_sfx(self, sfx_file: str, amount=0):
        '''
        amount 0 will get the current volume\n
        higher or lower will also change the current volume
        '''
        current_vol = self.sfx_library[sfx_file].get_volume()

        if amount == 0:
            return current_vol
        else:
            self.sfx_library[sfx_file].set_volume(current_vol + amount)
            return self.sfx_library[sfx_file].get_volume()

    def play_music(self, sound_file: str, loops=-1, start=0.0, fade_ms=0):
        '''
        Loads and starts the music
        '''
        pygame.mixer.music.load(self.music_library[sound_file])
        pygame.mixer.music.play(loops, start, fade_ms)

    def pause_music(self):
        '''
        Pauses the music
        '''
        pygame.mixer.music.pause()

    def stop_music(self):
        '''
        Stops the music
        '''
        pygame.mixer.music.stop()

    def queue_music(self, sound_file: str):
        '''
        Queues music to be played after the current playing music has ended
        '''
        pygame.mixer.music.queue(sound_file)

    def volume_music(self, amount=0):
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

    def pause_all(self):
        '''
        Pauses all sound playback (mixer and music)
        '''
        pygame.mixer.pause()
        pygame.mixer.music.pause()

    def resume_all(self):
        '''
        Resumes all sound playback (mixer and music)
        '''
        pygame.mixer.unpause()
        pygame.mixer.music.unpause()



    # TODO: Add method for car sounds
    # Function assigns car sound sequence to any free mixer track
    # List of 3 sound files: rev_up, steady(repeatable) and rev_down.
    # Returns the assigned mixer track:

    def play_car_sound(self, speed, max_speed, sound_files: list):
        rev_up = self.sfx_library[sound_files[0]]
        driving = self.sfx_library[sound_files[1]]
        rev_down = self.sfx_library[sound_files[2]]
        idle = self.sfx_library[sound_files[3]]

        if speed == 0 and idle.get_num_channels() == 0:
            self.stop_car_sound(sound_files)
            idle.play(-1)
        elif 0 < speed < max_speed and rev_up.get_num_channels() == 0:
            self.stop_car_sound(sound_files)
            rev_up.play()
        elif speed == max_speed and driving.get_num_channels() == 0:
            self.stop_car_sound(sound_files)
            driving.play(-1)
        elif 0 < speed < max_speed and driving.get_num_channels() == 1:
            self.stop_car_sound(sound_files)
            rev_down.play()

    def stop_car_sound(self, sound_files: list):
        for file in sound_files:
            self.sfx_library[file].stop()

            



if __name__ == "__main__":
    main()
