import pygame
from pygame.locals import *
from random import randint, choice

class CEvent:
    def on_key_down(self, event):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]: return 'keKiri'
        elif keys[K_RIGHT]: return 'keKanan'
        elif keys[K_UP]: return 'keAtas'
        elif keys[K_DOWN]: return 'keBawah'
        elif keys[K_q]: return 'keluar'

class App:
    def __init__(self):
        pygame.init()
        self.size = self.weight, self.height = 1024, 768
        self._display_surf = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Pac-Man x Ghost")

        self.event = CEvent()
        self.clock = pygame.time.Clock()

        # Images
        self.pacmanR = pygame.image.load("asset/resized_pacman.png")
        self.pacmanL = pygame.image.load("asset/resized_pacmanL.png")
        self.pacmanUp = pygame.image.load("asset/resized_pacmanUp.png")
        self.pacmanDw = pygame.image.load("asset/resized_pacmanDw.png")
        self.apple = pygame.image.load("asset/resized_apple.png")
        self.enemy = pygame.image.load("asset/resized_enemy.png")

        # Initial Positions
        self.pm_back_rect = pygame.Rect(512, 350, 50, 50)
        self.ap_back_rect = pygame.Rect(randint(100, 950), randint(200, 600), 50, 50)
        self.enemy_rect = pygame.Rect(100, 100, 50, 50)
        self.enemy_dir = choice(['up', 'down', 'left', 'right'])

        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.score = 0
        self.apple_enable = True

        # Direction flags
        self.dir = 'right'

        # Maze walls
        self.walls = [
            pygame.Rect(200, 150, 600, 20),
            pygame.Rect(200, 150, 20, 400),
            pygame.Rect(200, 530, 600, 20),
            pygame.Rect(780, 150, 20, 400),
            pygame.Rect(400, 300, 200, 20)
        ]

        self._running = True

    def move_pacman(self):
        keys = pygame.key.get_pressed()
        step = 3
        dx, dy = 0, 0

        if keys[K_LEFT]: dx, self.dir = -step, 'left'
        elif keys[K_RIGHT]: dx, self.dir = step, 'right'
        elif keys[K_UP]: dy, self.dir = -step, 'up'
        elif keys[K_DOWN]: dy, self.dir = step, 'down'

        next_pos = self.pm_back_rect.move(dx, dy)
        if not any(next_pos.colliderect(w) for w in self.walls):
            self.pm_back_rect = next_pos

    def move_enemy(self):
        speed = 2
        dx, dy = 0, 0
        if self.enemy_dir == 'up': dy = -speed
        elif self.enemy_dir == 'down': dy = speed
        elif self.enemy_dir == 'left': dx = -speed
        elif self.enemy_dir == 'right': dx = speed

        next_rect = self.enemy_rect.move(dx, dy)
        if any(next_rect.colliderect(w) for w in self.walls):
            self.enemy_dir = choice(['up', 'down', 'left', 'right'])
        else:
            self.enemy_rect = next_rect

    def on_event(self, event):
        if event.type == QUIT or (event.type == KEYDOWN and self.event.on_key_down(event) == 'keluar'):
            self._running = False

    def on_loop(self):
        self.move_pacman()
        self.move_enemy()

        if self.pm_back_rect.colliderect(self.ap_back_rect) and self.apple_enable:
            self.apple_enable = False
            self.score += 10
            self.ap_back_rect.x = randint(100, 950)
            self.ap_back_rect.y = randint(200, 600)
            self.apple_enable = True

        if self.pm_back_rect.colliderect(self.enemy_rect):
            print("💀 Pac-Man dimakan musuh! Game over.")
            self._running = False

    def on_render(self):
        self._display_surf.fill((0, 0, 0))

        # Draw apple
        if self.apple_enable:
            self._display_surf.blit(self.apple, self.ap_back_rect)

        # Draw pacman
        if self.dir == 'right':
            self._display_surf.blit(self.pacmanR, self.pm_back_rect)
        elif self.dir == 'left':
            self._display_surf.blit(self.pacmanL, self.pm_back_rect)
        elif self.dir == 'up':
            self._display_surf.blit(self.pacmanUp, self.pm_back_rect)
        elif self.dir == 'down':
            self._display_surf.blit(self.pacmanDw, self.pm_back_rect)

        # Draw enemy
        self._display_surf.blit(self.enemy, self.enemy_rect)

        # Draw walls
        for wall in self.walls:
            pygame.draw.rect(self._display_surf, (0, 0, 255), wall)

        # Draw score
        text = self.my_font.render(f'Skor: {self.score}', True, (255, 255, 255))
        self._display_surf.blit(text, (10, 10))

        pygame.display.flip()

    def on_execute(self):
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    App().on_execute()
