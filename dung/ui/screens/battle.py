import pygame
from dung.size_settings import SIZES
from dung.monster_settings import WEAPON_SETTINGS
from dung.settings import *
from dung.ui.components.tooltip import Tooltip
from dung.utils import *
from dung.font_settings import FONTS

print("battle.py loaded")


def draw_battle_screen(screen, event_list, monster, hero, battle_log, fight_over=False):
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
        
        skills = ["Attack", "Defense", "Reckless Attack", "Bash", "Concentrate"]
        skill_details = [
            "Perform a basic attack.",
            "Increases defense value for the next 3 turns.",
            "A swift attack that deals increased damage with a higher chance to critically hit. There is a chance you may be hit by the enemy's weapon during the attack.",
            "Use your shield to strike the enemy for [str] damage and stun them for 1 turn.",
            "Increase your strength and defense by 2, and your block chance by 10% for 4 turns."
        ]
        keys = ["SPACE", "Q", "W", "E", "R"]


        skill_size = SIZES.TILE_SIZE 
        y_skill = SIZES.HEADER_SECTION_SIZE + SIZES.HEIGHT - battle_log.height - skill_size - 20
        mouse_pos = pygame.mouse.get_pos()
        for i, skill in enumerate(skills):
            skill_rect = pygame.Rect(x_offset + i * (skill_size + 5) ,y_skill, skill_size, skill_size)
            
            if skill_rect.collidepoint(mouse_pos):
                color = YELLOW

                Tooltip().draw(
                    surface=screen,
                    header_font=FONTS.TITLE_FONT,
                    header=skill,
                    font=FONTS.TEXT_FONT,
                    text=skill_details[i],
                    position=(skill_rect.x, skill_rect.y + skill_size),
                    direction="topleft",  # or "bottomleft", etc.
                    max_width=skill_size * 5,
                    max_height=skill_size * 3
                )

                for event in event_list:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pygame.event.post(pygame.event.Event(OPTIONS_MENU_ITEM_CLICKED, {"skill": i}))
            else:
                color = WHITE

            pygame.draw.rect(screen, color, skill_rect, border_radius=2)
            pygame.draw.rect(screen, BLACK, skill_rect, border_radius=2, width=1)
            skill_label = FONTS.TEXT_FONT.render(keys[i], True, (0, 0, 0))
            skill_label_rect = skill_label.get_rect()
            skill_label_rect.bottomleft = (skill_rect.x + 4, skill_rect.y + skill_size - 1)
            screen.blit(skill_label, skill_label_rect)

    screen.set_clip(None)  # Reset clip
