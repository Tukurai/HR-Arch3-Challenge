from Settings import settings

class GameScene:
    def __init__(self, scene_manager, sprite_manager, scene_name, components):
        self.scene_manager = scene_manager
        self.sprite_manager = sprite_manager
        self.scene_name = scene_name
        self.components = components

    def handle_event(self, event):
        for component in self.components:
            component.handle_event(event)

    def update(self, timedelta, input_state):
        for component in self.components:
            component.update(timedelta, input_state)

    def draw(self, screen):
        for component in self.components:
            component.draw(screen)

    def scene_changed(self):
        sound_manager = self.scene_manager.sound_manager

        if settings.MUSIC_CHILD_MODE is True:
            menu_music = "mainmenu_child.wav"
            race_music = "race_child.wav"
        else:
            menu_music = "mainmenu_2.wav"
            race_music = "race.wav"

        if self.scene_name != "Race":
            sound_manager.stop_all_sfx()

            if sound_manager.current_playing_music != menu_music:
                sound_manager.play_music(menu_music)
        else:
            sound_manager.stop_music()
            sound_manager.play_music(race_music, volume=0.3)

