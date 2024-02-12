import pygame
from config import PLAYER_SPEED, WIDTH, HEIGHT, GAME_SCORE
from bullets import Bullet
import os

pygame.mixer.init()
bullet_sound = pygame.mixer.Sound(os.path.join('sounds', 'bullet_sound.wav'))

class Player(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        # Configuração inicial da nave do jogador.
        self.width = width
        self.height = height
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        # Carregar a imagem png da nave.
        image_path = os.path.join("images", "spaceship.png")  # Assuming "player_ship.png" is your PNG file
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height - 50) # Posição inicial no centro do ecrã.

        self.game_score = GAME_SCORE

        # Lista para armazenar as balas disparadas
        self.bullets = pygame.sprite.Group()
        self.can_shoot = True  # Initialize the can_shoot flag

    def update(self):
        keys = pygame.key.get_pressed()
        # Teclas de movimento, WASD e setas.
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < self.width:
            self.rect.x += PLAYER_SPEED
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 0:
            self.rect.y -= PLAYER_SPEED
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < self.height:
            self.rect.y += PLAYER_SPEED

        # Tecla para invocar balas, spacebar.
        if keys[pygame.K_SPACE] and self.can_shoot:
            self.shoot_bullet()
            self.can_shoot = False  # Utilizar uma flag para prevenir spam de balas.
        elif not keys[pygame.K_SPACE]:
            self.can_shoot = True  # Dar reset na flag.

    # Função para disparar.
    def shoot_bullet(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        self.bullets.add(bullet)
        bullet_sound.play()

    def die(self):
        # Dá reset na posição do jogador para ele tentar novamente.
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
