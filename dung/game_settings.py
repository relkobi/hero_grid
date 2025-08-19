
class GameSettings:
    def __init__(self):
        self.sound = True
        self.volume = 0.1
        self.resolution = [1024, 768]
        # self.resolution = [1280, 720]
        # self.resolution = [1920, 1080]
        # self.resolution = [2560, 1440]
        self.fullscreen = False
        self.font_name = "upheavtt.ttf"


    def set_volume(self, volume):
        self.volume = max(0, min(volume, 1))            


game_settings = GameSettings()