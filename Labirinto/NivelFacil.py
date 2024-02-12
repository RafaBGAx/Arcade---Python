import pygame
import sys
import subprocess
import time
from ProjetoLabirinto import menulabirinto, salvar_pontuacao, quack, baixarvolume
from VitoriaDerrota import vitoria, derrota

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load('Musica/musicanivel1.mp3')  #le wanski - La Couleur Du Son
pygame.mixer.music.play(-1)
baixarvolume()

icon = pygame.image.load('Imagens/IconJogo.png')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
fps = 60

#IMAGENS QUE SAO PRECISAS:
#______________________________________________________________________________

imgF = pygame.image.load('Imagens/FundoNivel1.png') #imagem de fundo
fundo_nivel1 = pygame.transform.scale(imgF, (400, 400))

#______________________________________________________________________________

imgP = pygame.image.load('Imagens/ParedeNivel1.png') #textura das paredes
paredeN1 = pygame.transform.scale(imgP, (50, 50))
paredeN1.get_rect()

#______________________________________________________________________________

img3_1 = pygame.image.load('Imagens/BackIcon.png') #botao de back
imagemBack_1 = pygame.transform.scale(img3_1, (20, 20))

img3a_1 = pygame.image.load('Imagens/BackIcon2.png')
imagemBack2_1 = pygame.transform.scale(img3a_1, (20, 20))



loadpato = pygame.image.load('Imagens/opato.png')
patoicon = pygame.transform.scale(loadpato, (27, 27))

loadpassos = pygame.image.load('Imagens/Passos2.png')
passoicon = pygame.transform.scale(loadpassos, (27, 27))

imgS = pygame.image.load('Imagens/SaidaNivel1.png')
imgSaida = pygame.transform.scale(imgS, (10, 50))
imgSaida.get_rect()

folha_patost = pygame.image.load('Imagens/Patos.png')
folha_patos = pygame.transform.scale(folha_patost, (300, 200))

folha_cogumelos = pygame.image.load('Imagens/Cogumelo.png')  
cogumelo_tamanho = 50
#-------------------------------------------------------------------------------------------------------------------
#definicao do ecra

largura, altura = 400, 400 #tamano da janela
ecraFacil = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Nível Fácil")

#-------------------------------------------------------------------------------------------------------------------
#texto:
cinzento_claro = (228, 228, 228)
fonte_texto_passos = (pygame.font.SysFont('Verdana', 18))

#______________________________________________________________________________

labirinto1 = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 3, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 0, 3, 1, 0, 0, 4], #4 representa a saída
        [1, 0, 1, 0, 1, 0, 1, 1], #3 sao patos
        [1, 0, 1, 3, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1]
    ]
    #MATRIZ DE LABIRINTO, FAZER 3 OU 4 NE
    # posicao do jogador

player_x, player_y = 1, 7


#aqui é criada a lista de 'cogumelos' para parecer que ele se mexe

cogumelos = []
for i in range(16):  # Supondo que tenha 16 sprites em uma linha
    cogumelo = folha_cogumelos.subsurface((i * cogumelo_tamanho, 0, cogumelo_tamanho, cogumelo_tamanho))
    cogumelos.append(cogumelo) #tenho 16 sprites de um cogumelo
cogumelo_atual = 0

patos = []
for linha in range(4):
    for coluna in range(2):
        pato = folha_patos.subsurface((linha * 50, coluna * 50, 50, 50))
        patos.append(pato)
pato_atual = 0

#botao de back que fica no canto superior direito
largura_botaob = 20
altura_botaob = 20
posicaobackx = largura - largura_botaob 
posicaobacky = 0
retb2_1 = imagemBack2_1.get_rect(topleft=(posicaobackx, posicaobacky)) #é preciso isto para dps ver
 
 
passos = 25
pontos = 0
running = True
v_vitoria = False
while running:
    clock.tick(fps) #meter os fps
        
    ecraFacil.blit(fundo_nivel1, (0, 0)) #meter o fundo do nivel
        
    cogumelo_atual = (cogumelo_atual + 1) % 16 #meter cada imagem do coiso a passar
    pato_atual = (pato_atual + 1) % 2
        
    ecraFacil.blit(cogumelos[cogumelo_atual], (player_x * 50, player_y * 50)) #o cogumelo tem as coordenadas do jogador * a escala
    
    pos_rato = pygame.mouse.get_pos()
    for y, row in enumerate(labirinto1):
            for x, cell in enumerate(row):
                    if cell == 1:
                        ecraFacil.blit(paredeN1, (x * 50, y * 50))   #desenhar as paredes nos sitios em que a matriz é 1         
                    if cell == 4:
                        ecraFacil.blit(imgSaida, ((x * 50) + (50 - imgSaida.get_width()) , y * 50)) #imagem da saida no 4
                    if cell == 0:
                        pass
                    if cell == 3:
                        ecraFacil.blit(patos[pato_atual], (x * 50, y * 50)) #meter os patos no 3
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if(400 - largura_botaob <= x <= 400) and (0<= y <= altura_botaob):
                print('Botão clicado') #meter o back
                running = False
                pygame.quit()
                menulabirinto() #voltar ao menu
                sys.exit()
                        
    if retb2_1.collidepoint(pos_rato):      #isto faz com que o back fique escuro quando passa o rato por cima
        ecraFacil.blit(imagemBack2_1, (posicaobackx, posicaobacky))
    else:
        ecraFacil.blit(imagemBack_1, (posicaobackx, posicaobacky))
        
    if passos == 0:
        print('Nao podes andar mais')
    else:       

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and player_y > 0: 
                if labirinto1[player_y - 1][player_x] == 0:
                    player_y -= 1
                    passos -= 1
                elif labirinto1[player_y - 1][player_x] == 4:
                    player_y -= 1
                    passos -= 1
                    v_vitoria = True
                    print('yayyy')
                    # Código para quando ganha
                elif labirinto1[player_y - 1][player_x]== 3:
                    quack()
                    labirinto1[player_y - 1][player_x] = 0
                    pontos += 1
                    passos -= 1
                    player_y -= 1
                        

            elif event.key == pygame.K_DOWN and player_y < 7: 
                if labirinto1[player_y + 1][player_x] == 0:
                    player_y += 1
                    passos -= 1
                elif labirinto1[player_y + 1][player_x] == 4:
                    player_y += 1
                    passos -= 1
                    v_vitoria = True
                    print('yayyy')
                    # Código para quando ganha
                elif labirinto1[player_y + 1][player_x]== 3:
                    quack()
                    labirinto1[player_y + 1][player_x] = 0
                    pontos += 1
                    passos -= 1
                    player_y += 1

            elif event.key == pygame.K_LEFT and player_x > 0:  
                if labirinto1[player_y][player_x - 1] == 0:  
                    player_x -= 1
                    passos -= 1
                elif labirinto1[player_y][player_x - 1] == 4:
                    player_x -= 1 
                    passos -= 1
                    v_vitoria = True
                    print('yayyy')
                    # Código para quando ganha
                elif labirinto1[player_y][player_x - 1]== 3:
                    quack()
                    labirinto1[player_y][player_x - 1] = 0
                    pontos += 1
                    passos -= 1
                    player_x -= 1 

            elif event.key == pygame.K_RIGHT and player_x < 7: 
                if labirinto1[player_y][player_x + 1] == 0:  
                    player_x += 1
                    passos -= 1
                elif labirinto1[player_y][player_x + 1] == 4: 
                    player_x += 1
                    passos -= 1
                    v_vitoria = True
                    print('yayyy')
                    # Código para quando ganha
                elif labirinto1[player_y][player_x + 1]== 3:
                    quack()
                    labirinto1[player_y][player_x + 1] = 0
                    pontos += 1
                    passos -= 1
                    player_x += 1
        if v_vitoria:
            salvar_pontuacao(f'{pontos}')
            vitoria('Medio')
            pygame.quit()
        
    if passos == 0 and not v_vitoria:
        pygame.quit()
        derrota('Facil')
        sys.exit()
        
            
    texto_pontos = fonte_texto_passos.render(f'{pontos}', True, cinzento_claro)
    texto_passos = fonte_texto_passos.render(f'{passos}', True, cinzento_claro)            
        
        #NOTA: o pass é uma operacao neutra, nao faz nada, e serve para situações do tipo case _:  pass
    ecraFacil.blit(patoicon, (0, 0))
    ecraFacil.blit(texto_pontos, (patoicon.get_width(), 0))
    ecraFacil.blit(passoicon, (1.5*patoicon.get_width() + texto_pontos.get_width(), 0))
    ecraFacil.blit(texto_passos, (1.5*patoicon.get_width() + texto_pontos.get_width() + passoicon.get_width(), 0))
    pygame.display.flip()
    
    pygame.time.wait(100)