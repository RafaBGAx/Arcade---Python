import pygame
from spaceship import Player
from config import WIDTH, HEIGHT, BLACK, WHITE, PLAYER_SPEED, ENEMY_CREATION_INTERVAL, enemy_creation_timer, FPS
from enemies import Enemy, RicochetEnemy
from score import Score
import random

pygame.init()
pygame.mixer.init()

# Carregar os sons que vão ser utilizados ao longo do jogo.
enemy_sound = pygame.mixer.Sound('Spaceshooter/sounds/enemy_sound.wav')
die_sound = pygame.mixer.Sound('Spaceshooter/sounds/die_sound.wav')

game_over = False
paused = False

# Configurar a janela do jogo
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Criar uma instância da classe Player para adicionar os controlos e a nave.
player = Player(WIDTH, HEIGHT)

# Criar um grupo de sprites para todos os sprites do jogo, exceto inimigos.
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Grupo de sprites para os inimigos.
all_enemies = pygame.sprite.Group()

# Variáveis para a linha de separação.
line_height = 2
middle_y = HEIGHT // 2

# Criar uma instância da classe Score
score = Score()

# Objeto clock para limitar os fps e prevenir lag e diferenças de performance entre dispositivos.
clock = pygame.time.Clock()

# Loop do jogo
running = True
paused = False
while running:
    elapsed_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            paused = not paused

    # Adquirir o score atual.
    current_score = score.value                
  
    if not paused:

        if elapsed_time - enemy_creation_timer >= ENEMY_CREATION_INTERVAL:
            # Criar um novo inimigo a partir de um determinado tempo.
            for x in range(current_score//10) if current_score >= 10 else range(1):
                if current_score <= 10:  
                    enemy = Enemy(random.randint(0, WIDTH), random.randrange(0, HEIGHT // 3))
                elif current_score <= 20:
                    enemy = RicochetEnemy(random.randint(0, WIDTH), random.randrange(0, HEIGHT // 3))
                elif current_score > 20:
                    # Escolher o tipo de inimigo aleatóriamente.
                    enemy_class = random.choice([Enemy, RicochetEnemy])
                    enemy = enemy_class(random.randint(0, WIDTH), random.randrange(0, HEIGHT // 3))  
                all_enemies.add(enemy)                             


            # Dar reset na variável de timer.
            enemy_creation_timer = elapsed_time    

        # Desenhar elementos do jogo (background)
        screen.fill(BLACK)

        # Atualizar o estado do jogo
        all_sprites.update()
        all_enemies.update(screen)
        player.bullets.update()

        # Desenhar a linha que divide o jogador dos inimigos.
        pygame.draw.line(screen, WHITE, (0, middle_y), (WIDTH, middle_y), line_height)

        # Detecção de colisão
        line_rect = pygame.Rect(0, middle_y - line_height // 2, WIDTH, line_height)
        if player.rect.colliderect(line_rect):
            player.rect.y += PLAYER_SPEED  # Mover o jogador para baixo de acordo com a velocidade.     

        # Percorrer todos os inimigos.
        for enemy in all_enemies:
            collisions = enemy.check_collision(player.bullets)
            # Se o inimigo for acertado por uma bala, eliminar o inimigo e adicionar pontos à pontuação do jogador.
            if collisions:
                enemy.kill()
                score.increase(1)

                # Tocar som de morte de inimigo.
                enemy_sound.play()

            # Se o jogador tocar num inimigo, executar função de game over.
            if pygame.sprite.spritecollide(player, all_enemies, False): 
                game_over = True             

        # Desenhar elementos do jogo (sprites)  
        all_sprites.draw(screen)
        all_enemies.draw(screen)
        player.bullets.draw(screen)

        # Apresentar o score atual e o recorde anterior enquanto o utilizador joga.
        score_text = score.render()
        screen.blit(score_text, (10, 40))
        best_text = score.render_best()
        screen.blit(best_text, (10, 10))

        if game_over == True:
            
            # Tocar o som de game over.
            die_sound.play()

            # Desenhar a tela de game over
            screen.fill(BLACK)
            game_over_font = pygame.font.Font(None, 74)
            game_over_text = game_over_font.render("Game Over", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 8 - 50))

            score.update_high_score()
            score.reset()

            # Matar todos os inimigos quando o jogo terminar.
            for enemy in all_enemies:
                enemy.kill()

            # Apresentar a leaderboard.
            leaderboard_surface = score.render_leaderboard()
            screen.blit(leaderboard_surface, (WIDTH // 2 - leaderboard_surface.get_width() // 2, HEIGHT // 3))

            paused = True

    # Recomeçar o jogo caso Enter seja pressionado.
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        player.die()
        score.reset()
        game_over = False
        paused = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
