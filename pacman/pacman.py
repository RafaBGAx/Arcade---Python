import pygame
import sys
import os
from mapa import boards
import random

pygame.init()
pygame.mixer.init()
WIDTH = 1000
HEIGHT = 1000
level = boards
color = 'red'
total_score = 0
lives = 3
life_image = pygame.transform.scale(pygame.image.load('assets/mod_images/cora.png'), (30, 30))
game_won = False
restart_pressed = False
music = pygame.mixer.music.load('assets/mod_images/music.mp3')
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Player:
    def __init__(self, x, y):
        self.images_normal = [pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)) for i in range(1, 5)]
        self.images_powered_up = [pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)) for i in range(5, 10)]
        self.images = self.images_normal
        self.rect = self.images[0].get_rect(center=(x, y))
        self.base_speed = 6  # Velocidade
        self.current_speed = self.base_speed
        self.current_image = 0
        self.animation_timer = pygame.time.get_ticks()
        self.current_direction = None
        self.is_moving = False
        self.score = 0
        self.can_eat_ghosts = False
        self.ghost_eating_timer = 0
        self.is_powered_up = False
        self.power_up_timer = 0
        self.initial_x = x
        self.initial_y = y
        self.teleport_points = [(930, 450), (1, 450)]
        self.teleport_cooldown = 500  # Tempo teletransportes
        self.last_teleport_time = 0
        total_score = 0
        

    def eat_point(self, point_type):
     global total_score  
     if point_type == 1:  # Ponto branco
        self.score += 10
        total_score += 10
     elif point_type == 2:  # Ponto grande
        self.score += 50
        total_score += 50
        self.activate_power_up()

    def can_move(self, dx, dy):
        next_rect = self.rect.move(dx, dy)

        num1 = (HEIGHT - 50) // 32
        num2 = (WIDTH // 30)

        map_row = next_rect.centery // num1
        map_col = next_rect.centerx // num2

        if map_col < 29:
            current_tile = level[map_row][map_col]

            if current_tile in [1, 2]:
                self.eat_point(current_tile)
                level[map_row][map_col] = 0  # Remover o ponto do mapa

            elif current_tile in [7, 8] and self.can_eat_ghosts:
                self.eat_ghost()

            if current_tile in [3, 4, 5, 6, 7, 8, 9]:
                if self.current_direction == 0 and next_rect.centerx % num2 >= 15:
                    next_col = (next_rect.centerx + 15) // num2
                    if level[map_row][next_col] < 3:
                        return True
                elif self.current_direction == 1 and next_rect.centerx % num2 <= 15:
                    prev_col = (next_rect.centerx - 15) // num2
                    if level[map_row][prev_col] < 3:
                        return True
                elif self.current_direction == 2 and next_rect.centery % num1 >= 15:
                    next_row = (next_rect.centery + 15) // num1
                    if level[next_row][map_col] < 3:
                        return True
                elif self.current_direction == 3 and next_rect.centery % num1 <= 15:
                    prev_row = (next_rect.centery - 15) // num1
                    if level[prev_row][map_col] < 3:
                        return True
            else:
                return True

        return False

    def move(self, keys):
        if keys[pygame.K_RIGHT]:
            self.current_direction = 0
            self.is_moving = True
        elif keys[pygame.K_LEFT]:
            self.current_direction = 1
            self.is_moving = True
        elif keys[pygame.K_DOWN]:
            self.current_direction = 2
            self.is_moving = True
        elif keys[pygame.K_UP]:
            self.current_direction = 3
            self.is_moving = True

        if self.is_moving:
            dx, dy = 0, 0
            if self.current_direction == 0:
                dx = self.current_speed
            elif self.current_direction == 1:
                dx = -self.current_speed
            elif self.current_direction == 2:
                dy = self.current_speed
            elif self.current_direction == 3:
                dy = -self.current_speed

            if self.can_move(dx, dy):
                self.rect.x += dx
                self.rect.y += dy

    def activate_power_up(self):
        self.is_powered_up = True
        self.power_up_timer = pygame.time.get_ticks()
        self.images = self.images_powered_up
        self.current_image = 0  # RR a imagem
        self.current_speed = self.base_speed * 1.5  # Aumenta velocidade

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.animation_timer > 200:
            self.animation_timer = now
            self.current_image = (self.current_image + 1) % 4

    def update(self):
        self.update_animation()

        if self.is_powered_up:
            elapsed_time = pygame.time.get_ticks() - self.power_up_timer
            if elapsed_time >= 6500:  #tempo de poder
                self.is_powered_up = False
                self.images = self.images_normal
                self.current_speed = self.base_speed

    def draw(self, screen, direction):
        player_images = self.images

        if self.current_direction is not None:
            self.update_animation()

        if self.current_direction is None:
            self.current_direction = 0

        if self.current_direction == 0:
            screen.blit(player_images[self.current_image], self.rect.topleft)
        elif self.current_direction == 1:
            screen.blit(pygame.transform.flip(player_images[self.current_image], True, False), self.rect.topleft)
        elif self.current_direction == 2:
            screen.blit(pygame.transform.rotate(player_images[self.current_image], 270), self.rect.topleft)
        elif self.current_direction == 3:
            screen.blit(pygame.transform.rotate(player_images[self.current_image], 90), self.rect.topleft)
    
    def check_collision_with_ghosts(self, ghosts):
        global total_score
        for ghost in ghosts:
            if self.rect.colliderect(ghost.rect):
                if self.is_powered_up:
                    self.score += 200
                    total_score += 200
                    ghost.reset_position(ghost.initial_x, ghost.initial_y)
                else:
                    return True
        return False
    
    def reset_state(self):
        self.rect.x = self.initial_x - 15
        self.rect.y = self.initial_y - 20
        self.is_moving = False 
        self.current_direction = None
        self.current_image = 0
        self.animation_timer = pygame.time.get_ticks()
        self.score = 0
        self.can_eat_ghosts = False
        self.ghost_eating_timer = 0
        self.is_powered_up = False
        self.power_up_timer = 0
        self.images = self.images_normal
        self.current_speed = self.base_speed
    
    def check_teleport(self):
        current_time = pygame.time.get_ticks()

        for teleport_point in self.teleport_points:
            teleport_rect = pygame.Rect(teleport_point[0] - 5, teleport_point[1] - 5, 10, 10)
            if teleport_rect.colliderect(self.rect) and current_time - self.last_teleport_time > self.teleport_cooldown:
                next_teleport_point = self.teleport_points[(self.teleport_points.index(teleport_point) + 1) % len(self.teleport_points)]
                self.rect.center = next_teleport_point
                self.is_moving = False
                self.last_teleport_time = current_time  
                break

class Ghost:
    def __init__(self, x, y, color):
        self.images = [pygame.transform.scale(pygame.image.load(f'assets/{color}_images/{i}.png'), (45, 45)) for i in range(1, 6)]
        self.images_power = [pygame.transform.scale(pygame.image.load(f'assets/mod_images/{i}.png'), (45, 45))for i in range(1, 2)]
        self.rect = self.images[0].get_rect(center=(x, y))
        self.speed = 3
        self.current_image = 0
        self.animation_timer = pygame.time.get_ticks()
        self.direction = 0
        self.change_direction_timer = pygame.time.get_ticks()
        self.is_moving = False
        self.change_direction_interval = 2000
        self.start_moving = False
        self.start_moving = False
        self.timer_started = False
        self.timer_duration = 1000
        self.is_vulnerable = False 
        self.vulnerable_timer = 0
        self.initial_x = x
        self.initial_y = y

    def can_move(self, dx, dy):
        next_rect = self.rect.move(dx, dy)

        num1 = (HEIGHT - 50) // 32
        num2 = (WIDTH // 30)

        map_row = next_rect.centery // num1
        map_col = next_rect.centerx // num2

        if map_col < 29:
            current_tile = level[map_row][map_col]

            if current_tile in [3, 4, 5, 6, 7, 8]:
                if self.direction == 0 and next_rect.centerx % num2 >= 15:
                    next_col = (next_rect.centerx + 15) // num2
                    if level[map_row][next_col] < 3:
                        return True
                elif self.direction == 1 and next_rect.centerx % num2 <= 15:
                    prev_col = (next_rect.centerx - 15) // num2
                    if level[map_row][prev_col] < 3:
                        return True
                elif self.direction == 2 and next_rect.centery % num1 >= 15:
                    next_row = (next_rect.centery + 15) // num1
                    if level[next_row][map_col] < 3:
                        return True
                elif self.direction == 3 and next_rect.centery % num1 <= 15:
                    prev_row = (next_rect.centery - 15) // num1
                    if level[prev_row][map_col] < 3:
                        return True
            else:
                return True

        return False

    def can_turn(self):
        turns = [False, False, False, False]
        num1 = (HEIGHT - 50) // 32
        num2 = (WIDTH // 30)
        num3 = 15

        if self.rect.centerx // 30 < 29:
            current_tile = level[self.rect.centery // num1][self.rect.centerx // num2]

            if current_tile in [3, 4, 5, 6, 7, 8]:
                if self.direction == 0:
                    if self.rect.centerx % num2 >= 15 and level[self.rect.centery // num1][(self.rect.centerx + num3) // num2] < 3:
                        turns[0] = True
                elif self.direction == 1:
                    if self.rect.centerx % num2 <= 15 and level[self.rect.centery // num1][(self.rect.centerx - num3) // num2] < 3:
                        turns[1] = True
                elif self.direction == 2:
                    if self.rect.centery % num1 >= 15 and level[(self.rect.centery + num3) // num1][self.rect.centerx // num2] < 3:
                        turns[2] = True
                elif self.direction == 3:
                    if self.rect.centery % num1 <= 15 and level[(self.rect.centery - num3) // num1][self.rect.centerx // num2] < 3:
                        turns[3] = True

        return turns

    def move(self, keys):
        if not self.start_moving:
            if any(keys):
                self.start_moving = True
                self.timer_started = pygame.time.get_ticks()

        if self.start_moving:
            if not self.timer_started: 
                self.timer_started = pygame.time.get_ticks()

            elapsed_time = pygame.time.get_ticks() - self.timer_started

            if elapsed_time >= self.timer_duration:

                dx, dy = 0, 0
                if self.direction == 0:
                    dx = self.speed
                elif self.direction == 1:
                    dx = -self.speed
                elif self.direction == 2:
                    dy = self.speed
                elif self.direction == 3:
                    dy = -self.speed

                if self.can_move(dx, dy):
                    self.rect.x += dx
                    self.rect.y += dy
                else:
                    self.direction = random.choice([0, 1, 2, 3])
            else:
                dx, dy = 0, -self.speed
                if self.can_move(dx, dy):
                    self.rect.x += dx
                    self.rect.y += dy
    
     

    def update_animation(self):
        if pygame.time.get_ticks() - self.animation_timer > 150:
            self.current_image = (self.current_image + 1) % 5
            self.animation_timer = pygame.time.get_ticks()

    def draw(self, screen, player_powered_up):
        ghost_images = self.images_power if player_powered_up else self.images

        if player_powered_up:
            screen.blit(ghost_images[0], self.rect.topleft)
        elif 0 <= self.current_image < len(ghost_images):
            if self.direction == 0:
                screen.blit(ghost_images[self.current_image], self.rect.topleft)
            elif self.direction == 1:
                screen.blit(pygame.transform.flip(ghost_images[self.current_image], True, False), self.rect.topleft)
            elif self.direction == 2:
                screen.blit(pygame.transform.rotate(ghost_images[self.current_image], 270), self.rect.topleft)
            elif self.direction == 3:
                screen.blit(pygame.transform.rotate(ghost_images[self.current_image], 90), self.rect.topleft)   
    
    def reset_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def reset_state(self):
        self.rect.x = self.initial_x - 30
        self.rect.y = self.initial_y - 20
        self.start_moving = False
        self.timer_started = False
        self.is_moving = False
        self.direction = 0
        self.change_direction_timer = pygame.time.get_ticks()
        self.animation_timer = pygame.time.get_ticks()
        self.timer_duration = 1500
    
def draw_board(screen, lives, life_image):
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, 1.5708, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], 1.5708, 3.1416, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], 3.1416,
                                4.7124, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 4.7124,
                                6.2832, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
    
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {total_score}", True, (255, 255, 255))
    screen.blit(score_text, (WIDTH - 975, 960))
    
    for i in range(lives):
        screen.blit(life_image, (850 + i * 40, 955))

def are_all_points_eaten():
    for row in level:
        if any(tile in [1, 2] for tile in row):
            return False
    return True

def handle_events(ghosts):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    for ghost in ghosts:
        if any(keys):
            ghost.start_moving = True

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

pacman = Player(500, 535)
ghosts = [
    Ghost(900, 100, 'amarelo'),
    Ghost(450, 460, 'red'),
    Ghost(500, 460, 'roxo'),
    Ghost(550, 460, 'verde')
]

clock = pygame.time.Clock()
music = pygame.mixer.Sound('assets/mod_images/music.mp3')
music.set_volume(0.25)
canal = pygame.mixer.Channel(1)
texto = True
level = [row[:] for row in boards]
while True:
    handle_events(ghosts)

    keys = pygame.key.get_pressed()
    pacman.move(keys)
    direction = pacman.current_direction
    pacman.update_animation()
    pacman.update()
    pacman.check_teleport()
    
    
    if not canal.get_busy():
        
      canal.play(music,loops=-1)
    
    if pacman.check_collision_with_ghosts(ghosts):
        lives -= 1
        if lives > 0:
            pacman.reset_state()
            pacman.is_moving = False

            for ghost in ghosts:
                ghost.reset_state()
        else:
            #Perdeu
            canal.stop()
            screen.fill((0, 0, 0)) 
            font = pygame.font.Font(None, 72)
            text = font.render("Perdeu!", True, (255, 255, 255))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

            font_small = pygame.font.Font(None, 36)
            restart_text = font_small.render("Prima 'r' para recomeçar!", True, (255, 255, 255))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
            restart_text1 = font_small.render("Prima 'ESC' para voltar ao menu ", True, (255, 255, 255))
            screen.blit(restart_text1, (WIDTH // 2 - restart_text1.get_width() // 2, HEIGHT // 2 + 100))

            pygame.display.flip()

            restart_pressed = False
            while not restart_pressed:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE: #tecla esc para sair
                            pygame.quit()
                            sys.exit()
                        elif event.key == pygame.K_r: #tecla r para dar rr ao jogo
                            restart_pressed = True
                            total_score = 0
                            lives = 3
                            pacman.reset_state()
                            for ghost in ghosts:
                                ghost.reset_state()
                            level = [row[:] for row in boards]
                            game_won = False 

    else:
        if are_all_points_eaten() and not game_won:
            # Ganhou
            canal.stop()
            screen.fill((0, 0, 0)) 
            font = pygame.font.Font(None, 72)
            text = font.render("Ganhou!", True, (255, 255, 255))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

            font_small = pygame.font.Font(None, 36)
            restart_text = font_small.render("Press 'r' to restart", True, (255, 255, 255))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
            restart_text1 = font_small.render("Prima 'ESC' para voltar ao menu ", True, (255, 255, 255))
            screen.blit(restart_text1, (WIDTH // 2 - restart_text1.get_width() // 2, HEIGHT // 2 + 100))

            pygame.display.flip()

            restart_pressed = False
            while not restart_pressed:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE: #tecla ESC para sair
                            pygame.quit()
                            sys.exit()
                        elif event.key == pygame.K_r: #tecla r para dar rr
                            restart_pressed = True
                            total_score = 0
                            lives = 3
                            pacman.reset_state()
                            for ghost in ghosts:
                                ghost.reset_state()
                            level = [row[:] for row in boards]
                            game_won = False

    for ghost in ghosts:
        ghost.update_animation()
        ghost.move(keys)
    
    if are_all_points_eaten() and not game_won:
        game_won = True

    screen.fill((0, 0, 0))
            
    pacman.draw(screen, direction)
    for ghost in ghosts:
        ghost.draw(screen, pacman.is_powered_up)

    draw_board(screen, lives, life_image)
    
    pygame.display.flip()

    clock.tick(30)
 