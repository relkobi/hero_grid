import pygame
from dung.settings import BLACK

DEFAULT_STEP = 0.05
DEFAULT_VOLUME = 0.5
HANDLE_SIZE = 20
LINE_HEIGHT = 3

class VolumeSlider:
    def __init__(self, x, y, width, font, event_type, initial_volume=DEFAULT_VOLUME, step=DEFAULT_STEP):
        self.x = x
        self.y = y
        self.width = width
        self.volume = initial_volume
        self.step = step
        self.event_type = event_type
        self.dragging = False
        self.font = font
        self.dirty = False

        self.line_color = BLACK
        self.handle_color = BLACK
        self.text_color = BLACK

    def resize(self, x, y, width, font):
        self.x = x
        self.y = y
        self.width = width
        self.font = font

    def draw(self, screen):
        # Draw volume bar (centered)
        line_rect = pygame.Rect(0, 0, self.width, LINE_HEIGHT)
        line_rect.center = (self.x, self.y)
        pygame.draw.rect(screen, self.line_color, line_rect)
        line_rect.center = (self.x, self.y)
        pygame.draw.rect(screen, self.line_color, line_rect)

        # Draw handle (centered on line + offset)
        handle_x = self.x - self.width // 2 + self._get_handle_offset()
        handle_rect = pygame.Rect(0, 0, HANDLE_SIZE, HANDLE_SIZE)
        handle_rect.center = (handle_x, self.y)
        pygame.draw.rect(screen, self.handle_color, handle_rect)

        # Draw volume text above the slider
        label = self.font.render(f"Volume: {int(round(self.volume * 100))}%", True, self.text_color)
        text_rect = label.get_rect(center=(self.x, self.y - self.font.get_height()))
        screen.blit(label, text_rect)

    def handle_event(self, event):
        mousewheel_hitbox_rect = pygame.Rect(0, 0, self.width, HANDLE_SIZE + self.font.get_height())
        mousewheel_hitbox_rect.center = (self.x , self.y - self.font.get_height() // 2)

        line_hitbox_rect = pygame.Rect(0, 0, self.width, HANDLE_SIZE)
        line_hitbox_rect.center = (self.x , self.y)

        handle_x = self.x - self.width // 2 + self._get_handle_offset()
        handle_rect = pygame.Rect(0, 0, HANDLE_SIZE, HANDLE_SIZE)
        handle_rect.center = (handle_x, self.y)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if handle_rect.collidepoint(event.pos):
                self.dragging = True
            elif line_hitbox_rect.collidepoint(event.pos):
                volume_change_value = DEFAULT_STEP if (event.pos[0] - handle_rect.x) > 0 else -DEFAULT_STEP
                self.update_volume(self.volume + volume_change_value)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if handle_rect.collidepoint(event.pos):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                new_vol = self._get_volume_from_pos(event.pos[0])
                self.update_volume(new_vol)

        elif event.type == pygame.MOUSEWHEEL:
            if mousewheel_hitbox_rect.collidepoint(pygame.mouse.get_pos()):
                volume_change_value = max(-10, min(10, event.y)) * self.step
                new_vol = self.volume + volume_change_value
                self.update_volume(new_vol)

    def update_volume(self, new_vol, trigger_event=True):
        new_vol = max(0.0, min(1.0, round(new_vol / self.step) * self.step)) # normalize volume value to have only step multipication values 
        if new_vol != self.volume:
            self.volume = new_vol
            if trigger_event:
                pygame.event.post(pygame.event.Event(self.event_type, {"volume": self.volume}))

    def _get_handle_offset(self):
        return int(self.volume * self.width)

    def _get_volume_from_pos(self, pos_x):
        left = self.x - self.width // 2
        rel_x = max(left, min(pos_x, left + self.width)) - left
        raw_volume = rel_x / self.width
        return round(raw_volume / self.step) * self.step
