import pygame
from dung.game_settings import game_settings
from dung.size_settings import SIZES

def create_screen(fullscreen):
    flags = (pygame.FULLSCREEN | pygame.SCALED) if fullscreen else 0
    size = (SIZES.SCREEN_WIDTH, SIZES.SCREEN_HEIGHT)

    if fullscreen:
        # Close the current display and Reinitialize it cleanly so the renderer will work with scale if it first initiate without it
        pygame.display.quit()     
        pygame.display.init()      

    return pygame.display.set_mode(size, flags)

create_screen(game_settings.fullscreen)