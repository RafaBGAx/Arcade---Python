import pygame
import time
import config
import os

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(config.ENEMY_COLOR)
        image_path = os.path.join("images", "enemy.png")  # Assuming "player_ship.png" is your PNG file
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.timestamp = time.time()

    def update(self, screen):

        # Se o inimigo existir por muito tempo, eliminar do ecrã para evitar aglomeração de objetos.
        if time.time() - self.timestamp > config.VANISH_TIME:
            self.kill()

        # Mover para baixo.
        self.rect.y += config.ENEMY_SPEED

        screen.blit(self.image, self.rect)

    def check_collision(self, bullets):
        collisions = pygame.sprite.spritecollide(self, bullets, True)
        return collisions

    def reverse_direction(self, horizontal=True):
        # Função para reverter a direção.
        if horizontal:
            self.rect.x += config.ENEMY_SPEED
        else:
            self.rect.y += config.ENEMY_SPEED

class RicochetEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        image_path = os.path.join("images", "ricochetship.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.left = False

    def update(self, screen):
        super().update(screen)

        # Se o inimigo existir por muito tempo, eliminar do ecrã para evitar aglomeração de objetos.
        if time.time() - self.timestamp > config.VANISH_TIME:
            self.kill()

        # Ricochete esquerda/direita
        if not self.left:
            self.rect.x -= config.ENEMY_SPEED // 2
        else:
            self.rect.x += config.ENEMY_SPEED // 2

        self.rect.y += config.ENEMY_SPEED // 2

        # Verificar colisão com paredes e mudar a direção.
        if self.rect.left <= 0 or self.rect.right >= screen.get_width():
            self.left = not self.left  # Reverter direção

        screen.blit(self.image, self.rect)