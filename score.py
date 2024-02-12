import pygame
from config import WHITE, GAME_SCORE
import os

# Classe para guardar a pontuação do jogador.
class Score:
    def __init__(self):
        self.value = GAME_SCORE
        self.font = pygame.font.Font(None, 36)
        self.high_scores = self.load_leaderboard()  # Carregar scores do ficheiro e guardar na variável.

    # Função para adicionar um ponto ao score.
    def increase(self, points=1):
        self.value += points

    # Função para dar reset ao score.
    def reset(self):
        self.value = 0

    # Apresentar o score atual enquanto o utilizador joga.
    def render(self):
        return self.font.render(f"Pontuação: {self.value}", True, WHITE)
    
    # Apresentar a melhor pontuação anterior. 
    def render_best(self):
        scores = self.get_leaderboard()
        best_score = scores[0]
        return self.font.render(f"Recorde atual: {best_score}", True, WHITE)
    
    def load_leaderboard(self):
        # Carregar os dez melhores scores, se o ficheiro existir.
        file_path = "leaderboard.txt"

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return [int(line.strip()) for line in file.readlines()]
        else:
            return [0] * 10  # Inicializar com scores default.

    def save_leaderboard(self):
        # Salva os scores para um ficheiro que será a nossa leaderboard.
        file_path = "leaderboard.txt"

        with open(file_path, 'w') as file:
            for score in self.high_scores:
                file.write(f"{score}\n")
                
    # Dá update na scoreboard com o score atual.
    def update_high_score(self):
        self.high_scores.append(self.value)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:10]  # Filtrar a informação no ficheiro por ordem descendente e manter apenas os dez scores mais altos.

        # Salvar os highscores atualizados para o ficheiro.
        self.save_leaderboard()

    def get_leaderboard(self):
        # Retorna os dez melhores scores numa lista.
        return self.high_scores[:10]
    
    # Dá render de uma leaderboard gráfica.
    def render_leaderboard(self):
        leaderboard_font = pygame.font.Font(None, 36)
        leaderboard_surface = pygame.Surface((300, 450))  # Tamanho total da leaderboard como um todo.
        leaderboard_surface.fill((0, 0, 0))  # Background.

        # Adicionar um título.
        title_text = leaderboard_font.render("Top 10 Scores", True, WHITE)
        leaderboard_surface.blit(title_text, (40, 0))

        # Criar a leaderboard.
        for i, score_value in enumerate(self.get_leaderboard()):
            leaderboard_text = leaderboard_font.render(f"#{i + 1}: {score_value}", True, WHITE)
            leaderboard_surface.blit(leaderboard_text, (80, 40 + i * 40))

        return leaderboard_surface