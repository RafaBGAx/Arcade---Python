# Classe para as balas do jogador.

import pygame
import time
from config import BULLET_SPEED, WHITE, VANISH_TIME
import os

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Inicializar configuração inicial da bala.
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.timestamp = time.time()  # Guardar o tempo em que foi criado.
        image_path = os.path.join("images", "bullets.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        

    def update(self):
        # Eliminar objeto após determinado tempo para evitar acúmulo de objetos.
        if time.time() - self.timestamp > VANISH_TIME:
            self.kill()
        # Movimentar a bala para cima.
        self.rect.y -= BULLET_SPEED

    def draw(self, screen):
        # Função para desenhar a bala no ecrã.
        screen.blit(self.image, self.rect)