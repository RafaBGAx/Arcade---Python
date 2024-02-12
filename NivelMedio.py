import pygame
import sys
from ProjetoLabirinto import menulabirinto, salvar_pontuacao, quack, baixarvolume
from VitoriaDerrota import vitoria, derrota
import subprocess

# Initialize Pygame
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load('Musica/musicanivel2.mp3') #le wanski - trauma
pygame.mixer.music.play(-1)
baixarvolume()

icon = pygame.image.load('Imagens/IconJogo.png')
pygame.display.set_icon(icon)
# Set up the display
largura, altura = 650, 650 #tamano da janela
ecraMedio = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Nível Médio")

imgP2 = pygame.image.load('Imagens/ParedeNivel2.png')
paredeN2 = pygame.transform.scale(imgP2, (50, 50))

imgM = pygame.image.load('Imagens/FundoNivel2.png')
fundo_nivel2 = pygame.transform.scale(imgM, (650, 650))


img3_1 = pygame.image.load('Imagens/BackIcon.png') #botao de back
imagemBack_1 = pygame.transform.scale(img3_1, (32.5, 32.5))

img3a_1 = pygame.image.load('Imagens/BackIcon2.png')
imagemBack2_1 = pygame.transform.scale(img3a_1, (32.5, 32.5))

img4 = pygame.image.load('Imagens/ProximoNivel.PNG')
imagemProxNivel = pygame.transform.scale(img4, (167.375, 81.25))


largura_botaob = 32.5
altura_botaob = 32.5

largurapn = imagemProxNivel.get_width()
alturapn = imagemProxNivel.get_height()

posicaobackx = 650 - largura_botaob 
posicaobacky = 0




imgS2 = pygame.image.load('Imagens/SaidaN2.png')
imgSaida2 = pygame.transform.scale(imgS2, (50, (50/4)))
imgSaida2.get_rect()


imgV = pygame.image.load('Imagens/Vitoria.png')
imagemVitoria = pygame.transform.scale(imgV, (650, 650))
ecraVitoria = pygame.Surface((650, 650))

loadpato = pygame.image.load('Imagens/opato.png')
patoicon = pygame.transform.scale(loadpato, (27, 27))

loadpassos = pygame.image.load('Imagens/Passos2.png')
passoicon = pygame.transform.scale(loadpassos, (27, 27))



#______________________________________________________________________________

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



# Labyrinth Layout (1 represents wall, 0 represents path)
labirinto2 = [
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 3, 0, 0, 0, 1],
    [1, 0, 0, 3, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1], #4 representa a saída
    [1, 3, 0, 0, 1, 3, 1, 0, 1, 3, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 0, 3, 1, 0, 1],
    [1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 1, 0, 1, 3, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 3, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1],
    [1, 1, 0, 0, 0 ,0, 0, 0, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1, 1]
]
#MATRIZ DE LABIRINTO, FAZER 3 OU 4 NE
# posicao do jogador
player_x, player_y = 1, 0

cogumelo_atual = 0

pato_atual = 0

pontos = 0

passos = 0


cinzento_claro = (228, 228, 228)
fonte_texto_pontos = (pygame.font.SysFont('Verdana', 18))

fonte_texto_passos = (pygame.font.SysFont('Verdana', 18))

clock = pygame.time.Clock()
fps = 60


passos = 88

# Game Loop
running = True
v_vitoria = False
while running:
    
    clock.tick(fps)
    ecraMedio.blit(fundo_nivel2, (0, 0))
     

    cogumelo_atual = (cogumelo_atual + 1) % 16
    pato_atual = (pato_atual + 1) % 2
    
    ecraMedio.blit(cogumelos[cogumelo_atual], (player_x * 50, player_y * 50))
    
    #CONFIGURAR O BOTAO DE BACK
    retb_1 = imagemBack_1.get_rect(topleft=(posicaobackx, posicaobacky))
    retb2_1 = imagemBack2_1.get_rect(topleft=(posicaobackx, posicaobacky))
    
    pos_rato = pygame.mouse.get_pos()

    for y, row in enumerate(labirinto2):
        for x, cell in enumerate(row):
            if cell == 1:
                ecraMedio.blit(paredeN2, (x * 50, y * 50)) #METER AS PAREDES
            if cell == 4:
                ecraMedio.blit(imgSaida2, (x * 50 , (y * 50 ) + (3*imgSaida2.get_height())))
            if cell == 0:
                pass
            if cell == 3:
                ecraMedio.blit(patos[pato_atual], (x * 50, y * 50))
    
          
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if(650 - largura_botaob <= x <= 650) and (0<= y <= altura_botaob):
                print('Botão clicado') #meter o back
                running = False
                pygame.quit()
                menulabirinto() #voltar ao menu
                sys.exit()
                
    if retb2_1.collidepoint(pos_rato):      
        ecraMedio.blit(imagemBack2_1, (posicaobackx, posicaobacky))
    else:
        ecraMedio.blit(imagemBack_1, (posicaobackx, posicaobacky))
    
    if passos == 0:
        print('Nao podes andar mais')
    else: 
        
        # Handle player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and player_y > 0:  # Adiciona verificação para não sair do labirinto
                if labirinto2[player_y - 1][player_x] == 0:
                    player_y -= 1
                    passos -=  1
                elif labirinto2[player_y - 1][player_x] == 4:
                    v_vitoria = True
                    player_y -= 1
                    passos -=  1
                    print('yayyy')
                elif labirinto2[player_y - 1][player_x]== 3:
                    quack()
                    labirinto2[player_y - 1][player_x] = 0
                    pontos += 1
                    passos -=  1
                    player_y -= 1

            elif event.key == pygame.K_DOWN and player_y < 12:  # Verifica o limite inferior
                if labirinto2[player_y + 1][player_x] == 0:
                    player_y += 1
                    passos -=  1
                elif labirinto2[player_y + 1][player_x] == 4:
                    v_vitoria = True
                    player_x += 1
                    passos -=  1
                    print('yayyy')
                elif labirinto2[player_y + 1][player_x] == 3:
                    quack()
                    labirinto2[player_y + 1][player_x] = 0
                    pontos += 1
                    passos -=  1
                    player_y += 1

            elif event.key == pygame.K_LEFT and player_x > 0:  # Verifica o limite esquerdo
                if labirinto2[player_y][player_x - 1] == 0:  # Corrige a verificação de posição
                    player_x -= 1
                    passos -=  1
                elif labirinto2[player_y][player_x - 1] == 4: 
                    v_vitoria = True
                    player_x += 1
                    passos -=  1
                    print('yayyy')
                elif labirinto2[player_y][player_x - 1] == 3:
                    quack()
                    labirinto2[player_y][player_x - 1] = 0
                    pontos += 1
                    player_x -= 1
                    passos -=  1

            elif event.key == pygame.K_RIGHT and player_x < 12:  # Verifica o limite direito
                if labirinto2[player_y][player_x + 1] == 0:  # Corrige a verificação de posição
                    player_x += 1
                    passos -=  1
                elif labirinto2[player_y][player_x + 1] == 4: 
                    v_vitoria = True
                    player_x += 1
                    passos -=  1
                    print('yayyy')
                elif labirinto2[player_y][player_x + 1] == 3:
                    quack()
                    labirinto2[player_y][player_x + 1] = 0
                    pontos += 1
                    passos -=  1
                    player_x += 1
        if v_vitoria:
            salvar_pontuacao(f'{pontos}')
            vitoria('Dificil')
            pygame.quit()
        if passos == 0 and not v_vitoria:
            pygame.quit()
            derrota('Medio')
            sys.exit()
  
    #NOTA: o pass é uma operacao neutra, nao faz nada, e serve para este tipo de situações do  case _:    
    texto_pontos = fonte_texto_pontos.render(f'{pontos}', True, cinzento_claro)
    texto_passos = fonte_texto_passos.render(f'{passos}', True, cinzento_claro)
    ecraMedio.blit(patoicon, (0, 0))
    ecraMedio.blit(texto_pontos, (patoicon.get_width(), 0))
    ecraMedio.blit(passoicon, ((1.5*patoicon.get_width() + texto_pontos.get_width())*2, 0))
    ecraMedio.blit(texto_passos, (3.0*patoicon.get_width() + texto_pontos.get_width()*2 + passoicon.get_width(), 0))

    pygame.display.flip()
    pygame.time.wait(100)