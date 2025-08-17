import pygame

from dung.utils import resource_path
from dung.settings import *

pygame.mixer.init()

class MUSIC_THEME:
    BOSS = "boss"
    EXPLORATION = "exploration"
    BATTLE = "battle"
    MENU = "menu"

STATE_TO_MUSIC_MAPPING = {
    START_SCREEN: MUSIC_THEME.MENU,
    HERO_SELECT_SCREEN: MUSIC_THEME.MENU,
    GAME_RUNNING: MUSIC_THEME.EXPLORATION,
    BATTLE_SCREEN: MUSIC_THEME.BATTLE,
    BATTLE_END_SCREEN: MUSIC_THEME.BATTLE,
    WIN_SCREEN: MUSIC_THEME.MENU,
    LOSE_SCREEN: MUSIC_THEME.MENU,
}

class MusicController:
    def __init__(self, sound, volume):
        self.state = START_SCREEN
        self.music_theme = MUSIC_THEME.MENU
        self.volume = volume
        self.sound = sound
        
        self.set_volume(self.volume)
        self.set_sound(self.sound)

    def _get_state_music_theme(self, state):
        return STATE_TO_MUSIC_MAPPING[state] if STATE_TO_MUSIC_MAPPING.get(state, None) is not None else self.music_theme

    def _load_music(self, music_theme: MUSIC_THEME):
        if self.sound:
            pygame.mixer.music.load(resource_path(f"dung/assets/music/{music_theme}.mp3"))  # Use a relative path to your music file
            pygame.mixer.music.play(-1)  # -1 means loop forever

    def set_state_music(self, state):
        new_music_theme = self._get_state_music_theme(state)
        if self.music_theme != new_music_theme:
            self.music_theme = new_music_theme
            self._load_music(self.music_theme)

    def set_sound(self, on):
        self.sound = on
        if not self.sound:
            pygame.mixer.music.stop()
        self._load_music(self.music_theme)

    def set_volume(self, volume):
        self.volume = max(0, min(volume, 1))            
        pygame.mixer.music.set_volume(self.volume)

