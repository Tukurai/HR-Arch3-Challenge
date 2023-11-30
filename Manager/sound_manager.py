import glob
import os
import time
import pygame
from Engine.car import DRIVE_CAR_EVENT

from Settings import settings


def main():
    # For testing:
    pygame.init()

    sound_manager = SoundManager()
    sound_manager.play_music("mainmenu_2.wav")
    sound_manager.volume_music(-0.8)
    # sound_manager.play_sfx("augh.wav")

    flag = False
    DONE = False
    screen = pygame.display.set_mode((500, 500))  # 1180, 216
    count = 0

    speed = 0
    previous_speed = 0
    max_speed = 10
    car_sounds = [
        "car1_rev_up.wav",
        "car1_driving.wav",
        "car1_rev_down.wav",
        "car1_idle.wav",
    ]

    while not DONE:
        pygame.event.pump()  # process event queue
        # It gets the states of all keyboard keys.
        keys = pygame.key.get_pressed()
        # print("%d"%count,keys)
        count += 1
        if keys[ord("w")]:  # And if the key is K_DOWN:
            if speed < max_speed:
                speed += 1
        else:
            if speed > 0:
                speed -= 1

        # print(speed)
        sound_manager.play_car_sound(
            speed, previous_speed, max_speed, car_sounds)
        previous_speed = speed
        time.sleep(0.1)


class SoundManager:
    def __init__(self, channels=10):
        """
        Init the sound manager with the amount of mixer channels (10 default)
        """
        self.mixer = pygame.mixer.init()
        pygame.mixer.set_num_channels(channels)

        # Setup assets folder path and init sound libraries
        current_path = os.path.dirname(os.path.dirname(__file__))
        self.libraries = self.init_libraries(
            os.path.join(current_path, "Assets"))
        self.sfx_library = self.libraries[0]
        self.music_library = self.libraries[1]

        self.current_playing_music = ""

    def init_libraries(self, assets_dir):
        """
        Init the sound libraries\n
        Uses the \Assets\Music and \Assets\SFX folders!
        """
        # Dict for library: key = str, value = dict
        sfx_library = {}
        music_library = {}

        # Paths for sound folders
        paths = {
            "sfx": os.path.join(assets_dir, "SFX"),
            "music": os.path.join(assets_dir, "Music"),
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

                for file in glob.glob("*.ogg"):
                    if key == "sfx":
                        sfx_library[file] = pygame.mixer.Sound(file)
                    else:
                        music_library[file] = file

        return sfx_library, music_library

    def play_sfx(self, sfx_file: str, volume=1.0):
        """
        Play a sound effect on an available channel
        """
        self.sfx_library[sfx_file].play()
        self.volume_sfx(self.sfx_library[sfx_file], volume)

    def pause_sfx(self, sfx_file: str):
        """
        Pause a sound effect
        """
        self.sfx_library[sfx_file].pause()

    def stop_sfx(self, sfx_file: str):
        """
        Stop a sound effect
        """
        self.sfx_library[sfx_file].stop()

    def volume_sfx(self, sfx_file: str, amount=0):
        """
        amount 0 will get the current volume\n
        higher or lower will also change the current volume
        """
        current_vol = self.sfx_library[sfx_file].get_volume()

        if amount == 0:
            return current_vol
        else:
            self.sfx_library[sfx_file].set_volume(
                (current_vol + amount) * settings.GLOBAL_VOLUME
            )
            return self.sfx_library[sfx_file].get_volume()

    def play_music(self, sound_file: str, loops=-1, start=0.0, fade_ms=0, volume=1.0):
        """
        Loads and starts the music
        """
        pygame.mixer.music.load(self.music_library[sound_file])
        pygame.mixer.music.play(loops, start, fade_ms)
        pygame.mixer.music.set_volume(volume * settings.GLOBAL_VOLUME)
        self.current_playing_music = sound_file

    def pause_music(self):
        """
        Pauses the music
        """
        pygame.mixer.music.pause()

    def stop_music(self):
        """
        Stops the music
        """
        pygame.mixer.music.stop()
        self.current_playing_music = ""

    def volume_music(self, amount=0):
        """
        amount 0 will get the current volume\n
        higher or lower will also change the current volume
        """
        current_vol = pygame.mixer.music.get_volume()

        if amount == 0:
            return current_vol
        else:
            pygame.mixer.music.set_volume(current_vol + amount)
            return pygame.mixer.music.get_volume()

    def pause_all(self):
        """
        Pauses all sound playback (mixer and music)
        """
        pygame.mixer.pause()
        pygame.mixer.music.pause()

    def resume_all(self):
        """
        Resumes all sound playback (mixer and music)
        """
        pygame.mixer.unpause()
        pygame.mixer.music.unpause()

    def handle_event(self, event):
        """
        Handles the sound manager events
        """
        if event.type == DRIVE_CAR_EVENT:
            self.play_car_sound(
                event.car.current_speed,
                event.car.prev_speed,
                event.car.max_speed,
                [
                    "car1_revup.wav",
                    "car1_driving.wav",
                    "car1_revdown.wav",
                    "car1_idle.wav",
                ],
            )

    # TODO: Add method for car sounds
    # Function assigns car sound sequence to any free mixer track
    # List of 3 sound files: rev_up, steady(repeatable) and rev_down.
    # Returns the assigned mixer track:

    def play_car_sound(self, speed, previous_speed, max_speed, sound_files: list):
        if speed < 0:
            speed = speed * -1
            max_speed = max_speed / 2

        if previous_speed < 0:
            previous_speed = previous_speed * -1

        for sound_file in sound_files:
            self.volume_sfx(sound_file, 2 * settings.GLOBAL_VOLUME)

        rev_up = self.sfx_library[sound_files[0]]
        driving = self.sfx_library[sound_files[1]]
        rev_down = self.sfx_library[sound_files[2]]
        idle = self.sfx_library[sound_files[3]]

        if speed == 0 and idle.get_num_channels() == 0:
            print("play idle")
            self.stop_car_sound(sound_files)
            idle.play(-1)

        elif speed > 0 and previous_speed < speed and rev_up.get_num_channels() == 0:
            print("play rev_up")
            self.stop_car_sound(sound_files)
            rev_up.play()

        elif speed > 0 and previous_speed > speed and rev_down.get_num_channels() == 0:
            print("play rev_down")
            self.stop_car_sound(sound_files)
            rev_down.play()

        elif (
            speed == max_speed
            and previous_speed == speed
            and driving.get_num_channels() == 0
        ):
            print("play driving")
            self.stop_car_sound(sound_files)
            driving.play(-1)

    def stop_car_sound(self, sound_files: list):
        for file in sound_files:
            self.sfx_library[file].stop()


if __name__ == "__main__":
    main()
