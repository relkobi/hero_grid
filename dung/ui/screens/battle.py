import math
import pygame
from dung.entities.heroes.hero import Hero
from dung.size_settings import SIZES
from dung.monster_settings import HEROES_SETTINGS, WEAPON_SETTINGS
from dung.settings import *
from dung.ui.components.tooltip import Tooltip
from dung.utils import *
from dung.font_settings import FONTS


def _draw_square_pie(screen, rect, percent, color):
    if percent <= 0:
        return
    if percent >= 100:
        pygame.draw.rect(screen, color, rect)
        return

    center = (rect.width / 2, rect.height / 2)
    w, h = rect.width, rect.height

    # Perimeter of the square path we use (start at top center, go clockwise):
    # The path is 4 edges: top-center -> top-right -> bottom-right -> bottom-left -> top-left -> top-center
    # We define these 5 points (the path is closed)
    path_points = [
        (w/2, 0),        # top center
        (w, 0),          # top-right corner
        (w, h),          # bottom-right corner
        (0, h),          # bottom-left corner
        (0, 0),          # top-left corner
        (w/2, 0)         # back to top center to close loop
    ]

    # Compute total perimeter length of the path (sum of segments)
    def dist(p1, p2):
        return math.hypot(p2[0]-p1[0], p2[1]-p1[1])
    perimeter = 0
    for i in range(len(path_points)-1):
        perimeter += dist(path_points[i], path_points[i+1])

    target_length = (percent / 100) * perimeter

    points = [center]  # start polygon from center
    length_accum = 0

    # Walk along path_points edges accumulating length until target_length reached
    for i in range(len(path_points) - 1):
        start = path_points[i]
        end = path_points[i + 1]
        edge_len = dist(start, end)

        if length_accum + edge_len >= target_length:
            remain = target_length - length_accum
            ratio = remain / edge_len
            interp_x = start[0] + (end[0] - start[0]) * ratio
            interp_y = start[1] + (end[1] - start[1]) * ratio
            points.append(start)
            points.append((interp_x, interp_y))
            break
        else:
            points.append(start)
            length_accum += edge_len

    # Draw polygon on transparent surface and blit it
    pie_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.polygon(pie_surface, color, points)
    screen.blit(pie_surface, rect.topleft)


def draw_battle_screen(screen, event_list, monster, hero: Hero, battle_log, fight_over=False):
    x_offset, y_offset = 20, SIZES.HEADER_SECTION_SIZE + 10
    fight_label = FONTS.TITLE_FONT.render(f"Fight level {monster.level} {monster.name}", True, (0, 0, 0))
    screen.blit(fight_label, (x_offset, y_offset))
    y_offset += FONTS.TITLE_FONT.get_height() + 10

    monster_size = SIZES.TILE_SIZE * 2
    monster_image = pygame.image.load(resource_path(f"dung/assets/{monster.name.lower()}.png"))
    monster_image = pygame.transform.scale(monster_image, (monster_size, monster_size))
    monster_rect = pygame.Rect(x_offset + (300 - monster_size) // 2, y_offset, monster_size, monster_size)
    screen.blit(monster_image, monster_rect)
    y_offset += monster_rect.height + 10

    #HEALTH BAR HERE
    health_ratio = max(monster.health / monster.max_health, 0)

    health_outer_rect = pygame.Rect(x_offset, y_offset, 300, 30)
    health_inner_rect = pygame.Rect(x_offset, y_offset, 300 * health_ratio, 30)

    pygame.draw.rect(screen, WHITE, health_outer_rect, border_radius=10)
    pygame.draw.rect(screen, RED_COLOR, health_inner_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, health_outer_rect, border_radius=10, width=1)

    health_text = f"{max(monster.health, 0)} / {monster.max_health}"
    health_label = FONTS.TEXT_FONT.render(health_text, True, BLACK)
    health_text_width, health_text_height = FONTS.TEXT_FONT.size(health_text)
    screen.blit(health_label, (health_outer_rect.x + ((300 - health_text_width) / 2), health_outer_rect.y + ((30 - health_text_height) / 2)))
    y_offset += health_outer_rect.height + 20

    weapon_damage = WEAPON_SETTINGS[monster.weapon]["damage"]
    stats = [
        f"Strength: {monster.strength}",
        f"Speed: {monster.speed}",
        f"Weapon: {monster.weapon} ({weapon_damage[0]}-{weapon_damage[1]})",
        f"Attacks: {monster.attacks}",
        f"Damage: {monster.get_damage_string()}",
        f"Shield: {monster.shield}",
        f"Block Chance: {monster.block}%",
        f"Critical Chance: {monster.critical_hit}%",
    ]
    
    stat_label_height = FONTS.TEXT_FONT.get_height() + 5
    for text in stats:
        label = FONTS.TEXT_FONT.render(text, True, BLACK)
        screen.blit(label, (x_offset, y_offset))
        y_offset += stat_label_height  # Space between stats

    battle_log.draw(screen)

    if (fight_over is not True):
        

        hero_modified_strength = hero.strength + hero.get_buff_combine_value("strength", 0)
        # skill_details = [
        #     "Perform a basic attack.",
        #     "Increases defense value for the next 3 turns.",
        #     "A swift attack that deals increased damage with a higher chance to critically hit. There is a chance you may be hit by the enemy's weapon during the attack.",
        #     f"Use your shield to strike the enemy for {hero_modified_strength} damage and stun them for 1 turn.",
        #     "Increase your strength and defense by 2, and your block chance by 10% for 4 turns."
        # ]

        keys = ["SPACE", "Q", "W", "E", "R"]
        pygame_keys = [pygame.K_SPACE, pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r]
        skill_names = []
        skill_details = []
        skill_cooldowns = []
        for skill_key in pygame_keys:
            skill_item = hero.get_hero_skills_item(skill_key)
            skill_names.append(skill_item["name"])
            skill_details.append(skill_item["details"])
            skill_cooldowns.append(skill_item["data"].get("cooldown", None))


        skill_size = SIZES.TILE_SIZE 
        y_skill = SIZES.HEADER_SECTION_SIZE + SIZES.HEIGHT - battle_log.height - skill_size - 20
        mouse_pos = pygame.mouse.get_pos()
        for i, skill_name in enumerate(skill_names):
            skill_rect = pygame.Rect(x_offset + i * (skill_size + 5) ,y_skill, skill_size, skill_size)
            
            is_skill_on_cooldown = not hero.is_skill_active(pygame_keys[i])
            if skill_rect.collidepoint(mouse_pos):
                color = YELLOW
                if is_skill_on_cooldown:
                    color = WHITE
                
                footer = None if skill_cooldowns[i] is None else f"Cooldown: {skill_cooldowns[i]}"
                Tooltip().draw(
                    surface=screen,
                    header_font=FONTS.TITLE_FONT,
                    header=skill_name,
                    font=FONTS.TEXT_FONT,
                    text=skill_details[i],
                    position=(skill_rect.x, skill_rect.y + skill_size),
                    direction="topleft",  # or "bottomleft", etc.
                    max_width=skill_size * 7,
                    max_height=skill_size * 3,
                    space_before_footer=footer is not None,
                    footer=footer
                )

                for event in event_list:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pygame.event.post(pygame.event.Event(HERO_SKILL_USED, {"key": pygame_keys[i]}))
            else:
                color = WHITE

            pygame.draw.rect(screen, color, skill_rect, border_radius=2)
            pygame.draw.rect(screen, BLACK, skill_rect, border_radius=2, width=1)

            if is_skill_on_cooldown:
                skill_cooldown = hero.get_cooldown(pygame_keys[i])
                percentage = round(skill_cooldown["turns_left"] / skill_cooldown["total_turns"] * 100)
                _draw_square_pie(screen, skill_rect, percentage, GRAY)

                cooldown_label = FONTS.TEXT_FONT.render(str(skill_cooldown["turns_left"]), True, BLACK)
                cooldown_label_rect = cooldown_label.get_rect()
                cooldown_label_rect.topright = (skill_rect.x + skill_rect.width - 4, skill_rect.y + 1)
                screen.blit(cooldown_label, cooldown_label_rect)

            skill_label = FONTS.TEXT_FONT.render(keys[i], True, BLACK)
            skill_label_rect = skill_label.get_rect()
            skill_label_rect.bottomleft = (skill_rect.x + 4, skill_rect.y + skill_size - 1)
            screen.blit(skill_label, skill_label_rect)

    screen.set_clip(None)  # Reset clip
