import pygame
import sys
import os
import time
from ProjetoLabirinto import menulabirinto, baixarvolume, quack
import random



def patinhos(): #isto serve para o lobby dos patos. 
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('Musica/lobbypatos.mp3') 
    pygame.mixer.music.play(-1)
    baixarvolume()
    
    
    
    ecrapatos = pygame.display.set_mode([600,700])

    imglobby = pygame.image.load('Imagens/LobyPatos.png')
    loby = pygame.transform.scale(imglobby, (600, 700))

    folha_patost = pygame.image.load('Imagens/Patos.png')
    folha_patos = pygame.transform.scale(folha_patost, (300, 200))

    folha_cogumelos = pygame.image.load('Imagens/Cogumelo.png')  
    cogumelo_tamanho = 50

    img3_1 = pygame.image.load('Imagens/BackIcon.png') #botao de back
    imagemBack_1 = pygame.transform.scale(img3_1, (20, 20))

    img3a_1 = pygame.image.load('Imagens/BackIcon2.png')
    imagemBack2_1 = pygame.transform.scale(img3a_1, (20, 20))
    retb = imagemBack_1.get_rect(topleft=(0, 0))
    
    folha_patoamarelot = pygame.image.load('Imagens/ducky_2.png')
    folha_patoamarelo = pygame.transform.scale(folha_patoamarelot, (192, 126))
    #---------------------

    player_x, player_y = (0, 0)
        
    posx = 100
    posy = 100
    speedx = 3
    speedy = 3
    
    
    patosfinais = 0

    patoamarelo = []
    for linha in range(3):
        for coluna in range(5):
            pato_a = folha_patoamarelo.subsurface((coluna*32, 31.5, 32, 31.5))
            patoamarelo.append(pato_a)
    pato_a_atual = 0
    
    
    cogumelos = []
    for i in range(16):  # Supondo que tenha 16 sprites em uma linha
        cogumelo = folha_cogumelos.subsurface((i * cogumelo_tamanho, 0, cogumelo_tamanho, cogumelo_tamanho))
        cogumelos.append(cogumelo) #tenho 16 sprites de um cogumelo
    cogumelo_atual = 0

    patos = []
    for linha in range(1):
        for coluna in range(5):
            pato = folha_patos.subsurface((coluna * 50, 50, 50, 50))
            patos.append(pato)
    pato_atual = 0



    try:
        with open('Pontos.txt', 'r') as arquivo_pontos:
            for linha in arquivo_pontos:
                patosfinais += int(linha.strip()) #isto soma os valores do ficheiro para saber quantos patos aparecem
    except FileNotFoundError:
        print("Arquivo Pontos.txt não encontrado.")
    except ValueError:
        print("Erro ao converter a pontuação para número.")
    
    posicoes_patos = [{ 
    'posicao': [random.randint(0, 550), random.randint(0, 650)],
    'velocidade': [random.choice([-3, 3]), random.choice([-3, 3])]
    } for _ in range(patosfinais)]
#isto cria uma lista de dicionarios, cada dicionario é criado pelo ciclo for até ao numero de patos acabar
#cada dicionario pega num valor interio aleatorio até 550 (largura da tela - tamanho do bicho)
#e num valor int aleatorio ate 650 (altura da tela menos a do bicho), convem que ele caiba
#e escolhe uma 'velocidade', que na realidade é apenas um numero random de posições seguintes que cada sprite tem, ou seja
# tal como na linha 142 tem posx += speedx, ao iterar cada pato para o por a mexer, vai buscar um valor random de unidades
#assim o movimento parece aleatorio

    proximo_quack = pygame.time.get_ticks() + 5000
    intervalo_quack = 5000
    anda = True
    fps = 60
    clock = pygame.time.Clock()
    while anda: 
        clock.tick(60)
        ecrapatos.blit(loby, (0, 0))
        
        
        cogumelo_atual = (cogumelo_atual + 1) % 16 #meter cada imagem do coiso a passar
        pato_atual = (pato_atual + 1) % len(patos)
        pato_a_atual = (pato_a_atual + 1) % len(patoamarelo)
        
        rect_player = pygame.Rect(player_x*50, player_y*50, 50, 50)


        '''retp = pato.get_rect()'''
        if patosfinais >= 100: #isto serve para nao haver patos infinitos no ecra eventualmente
                with open("Pontos.txt", 'w') as ficheiro:
                    pass
        
        pos_rato = pygame.mouse.get_pos()
        for event in pygame.event.get(): #check for events
            if event.type == pygame.QUIT: #exiting events
                    keep_going = False
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and (player_x + 1 <= 600 - cogumelo_tamanho): 
                        player_x += 1
                    if event.key == pygame.K_LEFT and (player_x - 1 >= 0):
                        player_x -= 1
                    if event.key == pygame.K_UP and (player_y - 1 >= 0):
                        player_y -= 1
                    if event.key == pygame.K_DOWN and (player_y + 1 <= 700 - cogumelo_tamanho):
                        player_y += 1
            
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if(0 <= x <= 20) and (0<= y <= 20):
                print('Botão clicado') #meter o back
                running = False
                pygame.quit()
                menulabirinto() #voltar ao menu
                sys.exit()
        
        if retb.collidepoint(pos_rato):      #isto faz com que o back fique escuro quando passa o rato por cima
            ecrapatos.blit(imagemBack2_1, (0,0))
        else:
            ecrapatos.blit(imagemBack_1, (0, 0))
        

        if posx - 32 <= 0 or posx + 32 >= 600:
            speedx = -speedx
        if posy - 31.5 <= 0 or posy + 31.5 >= 700:
            speedy = -speedy

        posx += speedx
        posy += speedy

        ecrapatos.blit(patoamarelo[pato_a_atual], (posx, posy))

        for pato in posicoes_patos:
            pato['posicao'][0] += pato['velocidade'][0] #isto muda a posicao de cada pato, para ele andar aleatoriamente
            pato['posicao'][1] += pato['velocidade'][1]

            
            if pato['posicao'][0] - 50 <= 0 or pato['posicao'][0] + 50 >= 600: #quando ele atinge as bordas direita e esquerda volta para tras
                pato['velocidade'][0] = -pato['velocidade'][0]
            if pato['posicao'][1] - 50 <= 0 or pato['posicao'][1] + 50 >= 700: #quando ele atinge as bordas de cima e de baixo
                pato['velocidade'][1] = -pato['velocidade'][1]

            ecrapatos.blit(patos[pato_atual], pato['posicao']) #mete-se o pato a aparecer a cada iteracao do loop
            

        ecrapatos.blit(cogumelos[cogumelo_atual], (player_x * 50, player_y * 50))
        
        if patosfinais <= 0: #se nao houver patos n faz sentido haver o barulho
            pass
        else:
            tempo_atual = pygame.time.get_ticks()

            if patosfinais > 10:
                intervalo_quack = max(1000, 2000 - (patosfinais - 10) * 100)
            else:
                intervalo_quack = 4000
            if tempo_atual >= proximo_quack:
                quack()
                proximo_quack = tempo_atual + intervalo_quack
        
        
        pygame.display.flip()
        clock.tick(60) 
        pygame.time.wait(100)

    
if __name__ == '__main__':
    while True:
        patinhos()
