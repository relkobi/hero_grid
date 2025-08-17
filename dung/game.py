# game.py

import pygame
import random

from dung.entities.heroes.knight import Knight
from dung.entities.monsters.monster import Monster
from dung.game_settings import game_settings
from dung.size_settings import SIZES
from dung.font_settings import FONTS
from dung.images_loader import IMAGES
from dung.battle_log import BattleLog
from dung.music_controller import MusicController
from dung.monster_settings import MONSTERS_SETTINGS
from dung.settings import *
from dung.ui.screens.battle import draw_battle_screen

from dung.ui import *
from dung.ui.screens.settings_screen import draw_settings_screen

pygame.init()

pygame.display.set_caption("Grid Hero")


# Game variables
hero = None
hero_pos = None
monsters = []
potions = []
current_monster = None
battle_messages = []
battle_turn = 1
state = START_SCREEN
clock = pygame.time.Clock()
show_menu = False
options_state = None

line_height = FONTS.TEXT_FONT.get_height()
scroll_offset = 0
max_scroll = line_height * BATTEL_LOG_VISIBLE_LINES_COUNT

battle_log = BattleLog(
    x=10,
    y=SIZES.SCREEN_HEIGHT - (BATTEL_LOG_VISIBLE_LINES_COUNT * FONTS.TEXT_FONT.get_height()) - 10,
    width= SIZES.WIDTH - 10,
    visible_lines=BATTEL_LOG_VISIBLE_LINES_COUNT,
)

music_controller = MusicController(game_settings.sound, game_settings.volume)

def create_screen(fullscreen):
    flags = pygame.FULLSCREEN if fullscreen else 0
    size = (SIZES.SCREEN_WIDTH, SIZES.SCREEN_HEIGHT)
    
    return pygame.display.set_mode(size, flags)

screen = create_screen(game_settings.fullscreen)

def place_monsters():
    monsters_count = random.randint(round(TILE_COUNT) - 1, round(TILE_COUNT) + 1)
    monsters = []
    while len(monsters) < monsters_count:
        pos = [random.randint(1, COLUMNS_COUNT-1), random.randint(0, ROWS_COUNT-1)]
        if pos != hero_pos and not any(m['pos'] == pos for m in monsters):
            monster_type = "goblin" if random.randint(0, 1) == 0 else "skeleton"
            monsters.append({
                'pos': pos,
                'entity': Monster(monster_type)
            })

    return monsters

def place_potions(monsters):
    # 1 potion for each 2 monsters
    count = len(monsters) // 2
    pots = []
    while len(pots) < count:
        pos = [random.randint(1, COLUMNS_COUNT-1), random.randint(0, ROWS_COUNT-1)]
        if pos != hero_pos and not any(m['pos'] == pos for m in monsters) and not any(p['pos'] == pos for p in pots):
            pots.append({'pos': pos})
    return pots

def handle_hero_action(key):
    action_messages = hero.perform_hero_action(current_monster['entity'], key)
    for action_message in action_messages:
        battle_log.add_message(action_message)

def handle_monster_action():
    action_messages = current_monster['entity'].perform_monster_action(hero)
    for action_message in action_messages:
        battle_log.add_message(action_message)

def check_battle_results():
    if hero.health <= 0:
        battle_log.add_message(f"{current_monster['entity'].name} Won!")
        return BATTLE_END_SCREEN

    if current_monster['entity'].health <= 0:
        battle_log.add_message(f"{hero.name} Won!")
        monster_xp = MONSTERS_SETTINGS[current_monster['entity'].name.lower()]["xp"]
        hero.gain_xp(monster_xp)
        return BATTLE_END_SCREEN
    
    return BATTLE_SCREEN

def handle_settings_items_events():
    global screen, state, options_state

    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        if state == SETTINGS_SCREEN:
            state = START_SCREEN
        else:
            options_state = None
    elif event.type == SETTINGS_MENU_BACK:
        if state == SETTINGS_SCREEN:
            state = START_SCREEN
        else:
            options_state = None
    elif event.type == SETTINGS_MENU_FULLSCREEN:
        game_settings.fullscreen = event.fullscreen
        screen = create_screen(game_settings.fullscreen)
    elif event.type == SETTINGS_MENU_SET_RESOLUTION:
        game_settings.resolution = event.resolution
        SIZES.update_resolution(event.resolution[0], event.resolution[1])
        FONTS.resize_fonts(game_settings.font_name, event.resolution[1])
        IMAGES.update_by_resolution()
        screen = create_screen(game_settings.fullscreen)
    elif event.type == SETTINGS_MENU_TOGGLE_SOUND:
        game_settings.sound = event.sound
        music_controller.set_sound(game_settings.sound)
    elif event.type == SETTINGS_MENU_SET_SOUND_VOLUME:
        game_settings.volume = event.volume
        music_controller.set_volume(game_settings.volume)

# Main game loop
running = True
while running:
    screen.fill(WHITE)
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False
            break

        if state == START_SCREEN:
            if event.type == START_SCREEN_ITEM_CLICKED:
                if event.item == SS_START_GAME_ITEM:
                    state = HERO_SELECT_SCREEN
                elif event.item == SS_COMPENDIUM_ITEM:
                    state = START_SCREEN # TODO
                elif event.item == SS_SETTINGS_ITEM:
                    state = SETTINGS_SCREEN
                elif event.item == SS_CREDITS_ITEM:
                    state = START_SCREEN # TODO
                elif event.item == SS_EXIT_GAME_ITEM:
                    running = False
                break
        
        elif state == SETTINGS_SCREEN:
            handle_settings_items_events()

        elif state == HERO_SELECT_SCREEN:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = START_SCREEN
            elif event.type == HERO_SELECTION_HERO_CLICKED:
                hero_type = event.hero
                # Initialize hero and entities
                hero_img = pygame.image.load(resource_path(f"dung/assets/{hero_type}.png"))
                hero_img = pygame.transform.scale(hero_img, (SIZES.TILE_SIZE, SIZES.TILE_SIZE))
                # hero_settings = HEROES_SETTINGS[hero_type]
                hero = Knight()
                hero_pos = [0, ROWS_COUNT // 2]
                monsters = place_monsters()
                potions = place_potions(monsters)
                state = GAME_RUNNING

        elif show_menu is True:
            if options_state is None:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    show_menu = False
                elif event.type == OPTIONS_MENU_ITEM_CLICKED:
                    item = event.item
                    if item == OM_NEW_RUN_ITEM:
                        state = HERO_SELECT_SCREEN
                        show_menu = False
                    elif item == OM_MAIN_MENU_ITEM:
                        state = START_SCREEN
                        show_menu = False
                    elif item == OM_SETTINGS_ITEM:
                      options_state = OM_SETTINGS_ITEM  
                    elif item == OM_EXIT_GAME_ITEM:
                        running = False
                        break
            elif options_state is OM_SETTINGS_ITEM:
                handle_settings_items_events()


        elif state == GAME_RUNNING:
            move = False
            dx, dy = 0, 0

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    dx = -1
                    move = True
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    dx = 1
                    move = True
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    dy = -1
                    move = True
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    dy = 1
                    move = True
                elif event.key == pygame.K_ESCAPE:
                    show_menu = True

            if event.type == GRID_TILE_CLICKED:
                if event.col == hero_pos[0] - 1 and event.row == hero_pos[1]:
                    dx = -1
                    move = True
                elif event.col == hero_pos[0] + 1 and event.row == hero_pos[1]:
                    dx = 1
                    move = True
                elif event.col == hero_pos[0] and event.row == hero_pos[1] - 1:
                    dy = -1
                    move = True
                elif event.col == hero_pos[0] and event.row == hero_pos[1] + 1:
                    dy = 1
                    move = True

            if move is True:
                new_x = hero_pos[0] + dx
                new_y = hero_pos[1] + dy

                if 0 <= new_x < COLUMNS_COUNT and 0 <= new_y < ROWS_COUNT:
                    hero_pos = [new_x, new_y]

                    # Check monster collision
                    for m in monsters:
                        if m['pos'] == hero_pos:
                            current_monster = m
                            battle_log.clear()
                            battle_turn = 1
                            state = BATTLE_SCREEN
                            break

                    # Check potion collision
                    for p in potions:
                        if p['pos'] == hero_pos:
                            hero.health = min(hero.max_health, hero.health + 5)
                            potions.remove(p)
                            break

        elif state == BATTLE_SCREEN:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_menu = True
                elif event.key in [pygame.K_SPACE, pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r]:
                    if hero.speed > current_monster['entity'].speed:
                        handle_hero_action(event.key)
                        state = check_battle_results()
                        if state == BATTLE_SCREEN:
                            handle_monster_action()
                            state = check_battle_results()
                    elif hero.speed == current_monster['entity'].speed:
                        handle_hero_action(event.key)
                        handle_monster_action()
                        state = check_battle_results()
                    else:
                        handle_monster_action()
                        state = check_battle_results()
                        if state == BATTLE_SCREEN:
                            handle_hero_action(event.key)
                            state = check_battle_results()

                    if state == BATTLE_END_SCREEN:
                        continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    battle_log.scroll_up()
                elif event.button == 5:  # Scroll down
                    battle_log.scroll_down()

        elif state == BATTLE_END_SCREEN:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                show_menu = True
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and event.button in [4, 5]:
                if event.button == 4:  # Scroll up
                    battle_log.scroll_up()
                elif event.button == 5:  # Scroll down
                    battle_log.scroll_down()
            
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if hero.health <= 0:
                    state = LOSE_SCREEN
                else:    
                    monsters.remove(current_monster)
                    current_monster = None

                    if not monsters:
                        state = WIN_SCREEN
                    else:
                        state = GAME_RUNNING
                    continue

        elif state == WIN_SCREEN:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                state = START_SCREEN

        elif state == LOSE_SCREEN:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                state = START_SCREEN

    # Rendering
    if state == START_SCREEN:
        music_controller.set_state_music(START_SCREEN)
        draw_start_screen(screen, event_list)

    elif state == SETTINGS_SCREEN:
        draw_settings_screen(screen, event_list)

    elif state == HERO_SELECT_SCREEN:
        music_controller.set_state_music(START_SCREEN)
        draw_hero_selection_screen(screen, event_list)

    elif state == GAME_RUNNING:
        music_controller.set_state_music(GAME_RUNNING)
        draw_header_section(screen)
        draw_grid(screen, event_list)
        draw_entities(screen, hero, hero_pos, monsters, potions)
        draw_hero_stats(screen, hero)

    elif state == BATTLE_SCREEN:
        music_controller.set_state_music(BATTLE_SCREEN)
        draw_header_section(screen)
        draw_hero_stats(screen, hero)
        draw_battle_screen(screen, event_list, current_monster['entity'], hero, battle_log)
    
    elif state == BATTLE_END_SCREEN:
        music_controller.set_state_music(BATTLE_END_SCREEN)
        draw_header_section(screen)
        draw_hero_stats(screen, hero)
        draw_battle_screen(screen, event_list, current_monster['entity'], hero, battle_log, True)
        show_text(screen, FONTS.LARGE_FONT, "Fight Over", y_offset=-100)
        show_text(screen, FONTS.TITLE_FONT, "press any key to continue...")

    elif state == WIN_SCREEN:
        music_controller.set_state_music(WIN_SCREEN)
        show_text(screen, FONTS.LARGE_FONT, "You WIN!", -200)
        show_text(screen, FONTS.TITLE_FONT, "Click button to play again", y_offset=100)

    elif state == LOSE_SCREEN:
        music_controller.set_state_music(LOSE_SCREEN)
        show_text(screen, FONTS.LARGE_FONT, "You LOST!", -200)
        show_text(screen, FONTS.TITLE_FONT, "Click button to try again", y_offset=100)

    if show_menu is True:
        if options_state is OM_SETTINGS_ITEM:
            draw_settings_menu(screen, event_list)
        else:
            draw_options_menu(screen, event_list)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
