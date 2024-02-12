import pygame
import sys
from ProjetoLabirinto import menulabirinto, salvar_pontuacao, quack, baixarvolume
from VitoriaDerrota import vitoriafinal, derrota
import subprocess
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('Musica/musicanivel3.mp3') #le wanski - mangala
pygame.mixer.music.play(-1)
baixarvolume()


icon = pygame.image.load('Imagens/IconJogo.png')
pygame.display.set_icon(icon)

# Set up the display
largura, altura = 1000, 1000 #tamano da janela
ecraDificil = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Nível Díficil')

imgF = pygame.image.load('Imagens/FundoNivel3.png')
fundo_nivel1 = pygame.transform.scale(imgF, (1000, 1000))

imgp = pygame.image.load('Imagens/ParedesN3_2.png')
paredeN3 = pygame.transform.scale(imgp, (50, 50))

imgs = pygame.image.load('Imagens/SaidaN3.png')
saida3 = pygame.transform.scale(imgs, (10, 50))

img3_1 = pygame.image.load('Imagens/BackIcon.png') #botao de back
imagemBack_1 = pygame.transform.scale(img3_1, (50, 50))

img3a_1 = pygame.image.load('Imagens/BackIcon2.png')
imagemBack2_1 = pygame.transform.scale(img3a_1, (50, 50))

loadpato = pygame.image.load('Imagens/opato.png')
patoicon = pygame.transform.scale(loadpato, (36, 36))

loadpassos = pygame.image.load('Imagens/Passos2.png')
passoicon = pygame.transform.scale(loadpassos, (36, 36))

cogumelo_atual = 0

pato_atual = 0

pontos = 0

passos = 130

folha_cogumelos = pygame.image.load('Imagens/Cogumelo.png')  
cogumelo_tamanho = 50
cogumelos = []
for i in range(16):  # Supondo que tenha 16 sprites em uma linha
    cogumelo = folha_cogumelos.subsurface((i * cogumelo_tamanho, 0, cogumelo_tamanho, cogumelo_tamanho))
    cogumelos.append(cogumelo)



patos = []
folha_patost = pygame.image.load('Imagens/Patos.png')
folha_patos = pygame.transform.scale(folha_patost, (300, 200))

for linha in range(4):
    for coluna in range(2):
        pato = folha_patos.subsurface((linha * 50, coluna * 50, 50, 50))
        patos.append(pato)


cinzento_claro = (228, 228, 228)
fonte_texto_pontos = (pygame.font.SysFont('Verdana', 21))



# Labyrinth Layout (1 represents wall, 0 represents path)
labirinto3 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 0, 0, 1, 0, 0, 0, 1, 0, 3, 0, 0, 0, 0, 1, 3, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 3, 0, 1, 0, 1, 3, 1],
    [1, 0, 0, 0, 1, 3, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1], #4 representa a saída
    [1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 3, 1],
    [1, 3, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 3, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 1, 1, 3, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 1, 3, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1],
    [1, 3, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 0, 1, 0, 0, 3, 1, 0, 0, 0, 0, 3, 1, 0, 1, 0, 1],
    [1, 1, 0, 1, 3, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 1, 3, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 4],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    
]
#MATRIZ DE LABIRINTO, FAZER 3 OU 4 NE
# posicao do jogador
player_x, player_y = 4, 19

v_vitoria = False

# Game Loop
running = True
while running:
    
    ecraDificil.blit(fundo_nivel1, (0, 0))

    cogumelo_atual = (cogumelo_atual + 1) % 16
    pato_atual = (pato_atual + 1) % 2
    
    ecraDificil.blit(cogumelos[cogumelo_atual], (player_x * 50, player_y * 50))
    ecraDificil.blit(imagemBack_1, (950, 0))
    
    retb_1 = imagemBack_1.get_rect(topleft=(950, 0))
    retb2_1 = imagemBack2_1.get_rect(topleft=(950, 0))
    
    pos_rato = pygame.mouse.get_pos()
    
    for y, row in enumerate(labirinto3):
        for x, cell in enumerate(row):
            if cell == 1:
                ecraDificil.blit(paredeN3, (x * 50, y * 50))
            if cell == 4:
                ecraDificil.blit(saida3, (((x * 50) + (50 - saida3.get_width()) , y * 50)))
            if cell == 0:
                pass
            if cell == 3:
                ecraDificil.blit(patos[pato_atual], (x * 50, y * 50))
    
          
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if(950 <= x <= 1000) and (0<= y <= 50):
                print('Botão clicado') #meter o back
                running = False
                pygame.quit()
                menulabirinto() #voltar ao menu
                sys.exit()
            
                
    if retb2_1.collidepoint(pos_rato):      
        ecraDificil.blit(imagemBack2_1, (950, 0))
    else:
        ecraDificil.blit(imagemBack_1, (950, 0))

        # Handle player movement
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP and player_y > 0:  # Adiciona verificação para não sair do labirinto
            if labirinto3[player_y - 1][player_x] == 0:
                player_y -= 1
                passos -=  1
            elif labirinto3[player_y - 1][player_x] == 4:
                print('yayyy')
                v_vitoria = True
                player_y -= 1
                passos -=  1
                # Código para quando ganha
            elif labirinto3[player_y - 1][player_x] == 3:
                quack()
                labirinto3[player_y - 1][player_x] = 0
                pontos += 1
                player_y -= 1
                passos -=  1

        elif event.key == pygame.K_DOWN and player_y < 19:  # Verifica o limite inferior
            if labirinto3[player_y + 1][player_x] == 0:
                player_y += 1
                passos -=  1
            elif labirinto3[player_y + 1][player_x] == 4:
                print('yayyy')
                v_vitoria = True
                player_y += 1
                passos -= 1
                # Código para quando ganha
            elif labirinto3[player_y + 1][player_x] == 3:
                quack()
                labirinto3[player_y + 1][player_x] = 0
                pontos += 1
                player_y += 1
                passos -=  1


        elif event.key == pygame.K_LEFT and player_x > 0:  # Verifica o limite esquerdo
            if labirinto3[player_y][player_x - 1] == 0:  # Corrige a verificação de posição
                player_x -= 1
                passos -=  1
            elif labirinto3[player_y][player_x - 1] == 4: 
                print('yayyy')
                v_vitoria = True
                player_x -= 1
                passos -=  1
                # Código para quando ganha
            elif labirinto3[player_y][player_x - 1] == 3:
                quack()
                labirinto3[player_y][player_x - 1] = 0
                pontos += 1
                player_x -= 1
                passos -=  1

        elif event.key == pygame.K_RIGHT and player_x < 19:  # Verifica o limite direito
            if labirinto3[player_y][player_x + 1] == 0:  # Corrige a verificação de posição
                player_x += 1
                passos -=  1
            elif labirinto3[player_y][player_x + 1] == 4: 
                print('yayyy')
                v_vitoria = True
                player_x += 1
                passos -= 1
                # Código para quando ganha
            elif labirinto3[player_y][player_x + 1] == 3:
                quack()
                labirinto3[player_y][player_x + 1] = 0
                pontos += 1
                player_x += 1
                passos -=  1
        if v_vitoria:
            salvar_pontuacao(f'{pontos}')
            vitoriafinal()
                    
                      
    if passos == 0 and not v_vitoria:
        pygame.quit()
        derrota('Dificil')
        sys.exit()
        
        
        
    #NOTA: o pass é uma operacao neutra, nao faz nada, e serve para este tipo de situações do  case _:               
    texto_pontos = fonte_texto_pontos.render(f'{pontos}', True, cinzento_claro) #se tiver tempo meto uma imagem de um pato neste sitio :)
    texto_passos = fonte_texto_pontos.render(f'{passos}', True, cinzento_claro)
    ecraDificil.blit(patoicon, (0, 0))
    ecraDificil.blit(texto_pontos, (patoicon.get_width(), 0))
    ecraDificil.blit(passoicon, (1.5*patoicon.get_width() + texto_pontos.get_width(), 0))
    ecraDificil.blit(texto_passos, (1.5*patoicon.get_width() + texto_pontos.get_width() + passoicon.get_width(), 0))
    pygame.display.flip()
    pygame.time.wait(100)

