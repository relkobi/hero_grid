# ui.py

import pygame
from dung.entities.heroes.hero import Hero
from dung.size_settings import SIZES
from dung.monster_settings import LEVELS_SETTINGS, WEAPON_SETTINGS
from dung.settings import *
from dung.utils import *
from dung.font_settings import FONTS
from dung.images_loader import IMAGES


def draw_grid(screen, event_list):
    mouse_pos = pygame.mouse.get_pos()
    for x in range(0, COLUMNS_COUNT, 1):
        for y in range(0, ROWS_COUNT, 1):
            rect = pygame.Rect(x * SIZES.TILE_SIZE, SIZES.HEADER_SECTION_SIZE + y * SIZES.TILE_SIZE, SIZES.TILE_SIZE, SIZES.TILE_SIZE)
            if rect.collidepoint(mouse_pos):
                width = 3
                pygame.draw.rect(screen, darker_color(WHITE), rect)
                pygame.event.post(pygame.event.Event(GRID_TILE_HOVERED, {"col": x, "row": y}))


                for event in event_list:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pygame.event.post(pygame.event.Event(GRID_TILE_CLICKED, {"col": x, "row": y}))
            else:
                width = 1
            
            pygame.draw.rect(screen, BLACK, rect, width)

def show_text(screen, font, text, y_offset=0, center=True):
    label = font.render(text, True, BLACK)
    rect = label.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + y_offset)) if center else (10, 10 + y_offset)
    screen.blit(label, rect)

def grid_x_value(position):
    return position[0] * SIZES.TILE_SIZE

def grid_y_value(position):
    return SIZES.HEADER_SECTION_SIZE + position[1] * SIZES.TILE_SIZE

def draw_entities(screen, hero, hero_pos, monsters, potions, campfire_pos, chest_pos):
    # Draw campfire
    if campfire_pos is not None:
        campfire_rect = pygame.Rect(grid_x_value(campfire_pos), grid_y_value(campfire_pos), SIZES.TILE_SIZE, SIZES.TILE_SIZE)
        screen.blit(IMAGES.misc["campfire"], campfire_rect)

    # Draw chest
    if chest_pos is not None:
        campfire_rect = pygame.Rect(grid_x_value(chest_pos), grid_y_value(chest_pos), SIZES.TILE_SIZE, SIZES.TILE_SIZE)
        screen.blit(IMAGES.misc["chest"], campfire_rect)

    # Draw monsters (green)
    for monster in monsters:
        m_rect = pygame.Rect(grid_x_value(monster['pos']), grid_y_value(monster['pos']), SIZES.TILE_SIZE, SIZES.TILE_SIZE)
        monster_type = monster["entity"].name.lower()
        monster_image = IMAGES.monsters["goblin"] if monster_type == "goblin" else IMAGES.monsters["skeleton"]
        screen.blit(monster_image, m_rect)

    # Draw potions (red)
    for potion in potions:
        p_rect = pygame.Rect(grid_x_value(potion['pos']) + SIZES.TILE_SIZE // 4, grid_y_value(potion['pos']) + SIZES.TILE_SIZE // 4, SIZES.TILE_SIZE//2, SIZES.TILE_SIZE//2)
        screen.blit(IMAGES.misc["health_potion"], p_rect)

    # Draw hero
    hero_rect = pygame.Rect(grid_x_value(hero_pos), grid_y_value(hero_pos), SIZES.TILE_SIZE, SIZES.TILE_SIZE)
    screen.blit(IMAGES.heroes[hero.name.lower()], hero_rect)


def draw_hero_stats(screen, hero):
    x_offset, y_offset = SIZES.WIDTH + 20, SIZES.HEADER_SECTION_SIZE + 10  # Position to start drawing stats

    label = FONTS.TITLE_FONT.render(hero.name, True, BLACK)
    screen.blit(label, (x_offset, y_offset))
    y_offset += FONTS.TITLE_FONT.get_height()

    label = FONTS.TEXT_FONT.render( f"Level: {hero.level}", True, BLACK)
    screen.blit(label, (x_offset, y_offset))
    y_offset += FONTS.TEXT_FONT.get_height()

    #XP BAR HERE
    y_offset += 20
    next_level_xp = LEVELS_SETTINGS[hero.level]
    xp_ratio = max(hero.xp / next_level_xp, 0)

    xp_outer_rect = pygame.Rect(x_offset, y_offset, 300, 30)
    xp_inner_rect = pygame.Rect(x_offset, y_offset, 300 * xp_ratio, 30)
    y_offset += xp_outer_rect.height

    pygame.draw.rect(screen, WHITE, xp_outer_rect, border_radius=10)
    pygame.draw.rect(screen, YELLOW, xp_inner_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, xp_outer_rect, border_radius=10, width=1)

    xp_text = f"{hero.xp} / {next_level_xp}"
    xp_label = FONTS.TEXT_FONT.render(xp_text, True, BLACK)
    xp_text_width, xp_text_height = FONTS.TEXT_FONT.size(xp_text)
    screen.blit(xp_label, (xp_outer_rect.x + ((300 - xp_text_width) / 2), xp_outer_rect.y + ((30 - xp_text_height) / 2)))
    y_offset += xp_outer_rect.height


    # HERO IMAGE
    image_size = SIZES.TILE_SIZE * 2
    hero_image = pygame.image.load(resource_path(f"dung/assets/{hero.name.lower()}.png"))
    hero_image = pygame.transform.scale(hero_image, (image_size, image_size))
    image_rect = pygame.Rect(x_offset + (300 - image_size) // 2, y_offset, image_size, image_size)
    screen.blit(hero_image, image_rect)
    y_offset += image_size

    #HEALTH BAR HERE
    health_ratio = max(hero.health / hero.max_health, 0)
    health_outer_rect = pygame.Rect(x_offset, y_offset, 300, 30)
    health_inner_rect = pygame.Rect(x_offset, y_offset, 300 * health_ratio, 30)

    pygame.draw.rect(screen, WHITE, health_outer_rect, border_radius=10)
    pygame.draw.rect(screen, RED_COLOR, health_inner_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, health_outer_rect, border_radius=10, width=1)

    health_text = f"{max(hero.health, 0)} / {hero.max_health}"
    health_label = FONTS.TEXT_FONT.render(health_text, True, BLACK)
    health_text_width, health_text_height = FONTS.TEXT_FONT.size(health_text)
    screen.blit(health_label, (health_outer_rect.x + ((300 - health_text_width) / 2), health_outer_rect.y + ((30 - health_text_height) / 2)))
    y_offset += health_outer_rect.height

    # Hero Stats
    y_offset += 20 # stats margin
    weapon_damage = WEAPON_SETTINGS[hero.weapon]["damage"]

    stats = [
        _get_attribute_stat_line(hero, "Strength", "strength", hero.strength, 0),
        _get_attribute_stat_line(hero, "Speed", "speed", hero.speed, 0),
        f"Weapon: {hero.weapon} ({weapon_damage[0]}-{weapon_damage[1]})",
        _get_attribute_stat_line(hero, "Attacks", "attacks", hero.attacks, 0),
        f"Damage: {hero.get_damage_string()}",
        _get_attribute_stat_line(hero, "Shield", "shield", hero.shield, 0),
        _get_attribute_stat_line(hero, "Block Chance", "block", hero.block, 0),
        _get_attribute_stat_line(hero, "Critical Chance", "critical_hit", hero.critical_hit, 0),
    ]

    stat_label_height = FONTS.TEXT_FONT.get_height() + 5
    for text in stats:
        label = FONTS.TEXT_FONT.render(text, True, BLACK)
        screen.blit(label, (x_offset, y_offset))
        y_offset += stat_label_height  # Space between stats

    # for buff_item in hero.buffs:
    #     text = f"{buff_item["name"].capitalize()}: {buff_item["value"]}"
    #     label = FONTS.TEXT_FONT.render(text, True, GREEN_COLOR)
    #     screen.blit(label, (x_offset, y_offset))
    #     y_offset += stat_label_height  # Space between stats

    for debuff_item in hero.debuffs:
        text = f"{debuff_item["name"].capitalize()}: {debuff_item["value"]}"
        label = FONTS.TEXT_FONT.render(text, True, RED_COLOR)
        screen.blit(label, (x_offset, y_offset))
        y_offset += stat_label_height  # Space between stats

def _get_attribute_stat_line(hero: Hero, attribute_title: str, attribute_key: str, attribute_base_value: int, default_value: int):
    attribute_modifier = hero.get_buff_combine_value(attribute_key, default_value)
    modified = attribute_modifier != default_value
    attribute_calculated_value = attribute_base_value
    if modified:
        attribute_calculated_value += attribute_modifier
    modified_string = ""
    if modified:
        modified_string = f" ({attribute_modifier})"

    return f"{attribute_title}: {attribute_calculated_value}{modified_string}"


__all__ = ['draw_grid', 'show_text', 'draw_entities', 'draw_hero_stats']
