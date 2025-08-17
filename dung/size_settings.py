from dung.settings import TILE_COUNT, ROWS_COUNT, COLUMNS_COUNT
from dung.game_settings import game_settings

HEADER_SECTION_RATIO = 0.15
SIDEBAR_SECTION_RATIO = 0.3

class SizeSettings:
    _instance = None

    def __new__(cls, screen_width=None, screen_height=None):
        if cls._instance is None:
            if screen_width is None or screen_height is None:
                raise ValueError("screen_width and screen_height must be provided on first creation")
            cls._instance = super(SizeSettings, cls).__new__(cls)
            cls._instance._calculate_screen_values(screen_width, screen_height)
        return cls._instance

    def _calculate_screen_values(self, screen_width: int, screen_height: int):
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.HEADER_SECTION_SIZE = round(self.SCREEN_HEIGHT * HEADER_SECTION_RATIO)
        self.SIDEBAR_SECTION_SIZE = round(self.SCREEN_WIDTH * SIDEBAR_SECTION_RATIO)
        min_space = min(self.SCREEN_WIDTH - self.SIDEBAR_SECTION_SIZE, self.SCREEN_HEIGHT - self.HEADER_SECTION_SIZE)
        self.ROOM_SIZE = min_space // TILE_COUNT
        self.WIDTH = TILE_COUNT * self.ROOM_SIZE
        self.HEIGHT = TILE_COUNT * self.ROOM_SIZE

        self.HEADER_SECTION_SIZE = self.SCREEN_HEIGHT - self.HEIGHT # all the left over pixel will be added
        self.SIDEBAR_SECTION_SIZE = self.SCREEN_WIDTH - self.WIDTH

        self.TILE_SIZE = self.WIDTH // COLUMNS_COUNT
        print(f"min_space={min_space}, self.ROOM_SIZE={self.ROOM_SIZE}, self.TILE_SIZE={self.TILE_SIZE}")


    def update_resolution(self, screen_width: int, screen_height: int):
        self._calculate_screen_values(screen_width, screen_height)

SIZES = SizeSettings(game_settings.resolution[0], game_settings.resolution[1])
