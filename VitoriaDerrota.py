import pygame
import sys
import subprocess
from ProjetoLabirinto import menulabirinto
from Patos import patinhos

def vitoria(nivel):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('Musica/musicavitoria.mp3')  #le wanski - La Couleur Du Son
    pygame.mixer.music.play(-1)
    
    icon = pygame.image.load('Imagens/IconJogo.png')
    pygame.display.set_icon(icon)


    ecraVitoria = pygame.display.set_mode((300, 300))
    pygame.display.set_caption('Vitória!')

    icon = pygame.image.load('Imagens/IconJogo.png')
    pygame.display.set_icon(icon)


    imgb = pygame.image.load('Imagens/BackIcon.png')
    imagemBack = pygame.transform.scale(imgb, (20, 20))

    imgba = pygame.image.load('Imagens/BackIcon2.png')
    imagemBack2 = pygame.transform.scale(imgba, (20, 20))
    retb = imagemBack.get_rect(topleft=(0, 0))


    imgV = pygame.image.load('Imagens/Vitoria.png')
    imagemVitoria = pygame.transform.scale(imgV, (300, 300))


    imgPN = pygame.image.load('Imagens/ProximoNivel_1.PNG')
    proxnivel = pygame.transform.scale(imgPN, (150, 73))

    imgPN2 = pygame.image.load('Imagens/ProximoNivel_2.PNG')
    proxnivel2 = pygame.transform.scale(imgPN2, (150, 73))

    posicaopnx = (150 - (proxnivel.get_width()/2))
    posicaopny = (300 - (proxnivel.get_height() + 5))
    retpn = proxnivel.get_rect(topleft=(posicaopnx, posicaopny))

    vitoria = True
    while vitoria:
        pos_rato = pygame.mouse.get_pos()
        ecraVitoria.blit(imagemVitoria, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if(0 <= x <= imagemBack.get_width()) and (0 <= y <= imagemBack.get_height()):
                    print('Botão clicado') #meter o back
                    running = False
                    pygame.quit()
                    menulabirinto() #voltar ao menu
                    sys.exit()
                if(posicaopnx <= x <= posicaopnx + 150) and (posicaopny <= y <= posicaopny + 73):
                    pygame.quit()
                    subprocess.run(['python', f'Nivel{nivel}.py']) #quando clica no 'facil'
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    print('Botao clicado')
                    pygame.quit()
                    subprocess.run(['python', f'Nivel{nivel}.py']) #quando clica no 'facil'
                    sys.exit()
                    
                
        if retpn.collidepoint(pos_rato):      #isto faz com que o back fique escuro quando passa o rato por cima
            ecraVitoria.blit(proxnivel2, (posicaopnx, posicaopny))
        else:
            ecraVitoria.blit(proxnivel, (posicaopnx, posicaopny))
        if retb.collidepoint(pos_rato):
            ecraVitoria.blit(imagemBack2, (0, 0))
        else:
            ecraVitoria.blit(imagemBack, (0, 0))
        
        pygame.display.flip()
        pygame.time.wait(100)

def vitoriafinal():
    pygame.init()
    pygame.mixer.init() 
    pygame.mixer.music.load('Musica/kirbydance.mp3')
    pygame.mixer.music.play(-1)

    largurae = 500
    alturae = 500
    ecraWin = pygame.display.set_mode((largurae, alturae))
    imwin = pygame.image.load('Imagens/Win.png')
    youwin = pygame.transform.scale(imwin, (largurae, alturae))
    
    imgb = pygame.image.load('Imagens/BackIcon.png')
    imagemBack = pygame.transform.scale(imgb, (20, 20))

    imgba = pygame.image.load('Imagens/BackIcon2.png')
    imagemBack2 = pygame.transform.scale(imgba, (20, 20))
    retb = imagemBack.get_rect(topleft=(0, 0))
    
    
    
    imgw = pygame.image.load('Imagens/opato.png')
    pato = pygame.transform.scale(imgw, (75, 75))
    
    imgw2 = pygame.image.load('Imagens/opato2.png')
    pato2 = pygame.transform.scale(imgw2, (75, 75)) #METER AQUI O BOTAO PARA O LOBBY DS PATOS
    
    
    
    posicaoxpato = largurae/2 - pato.get_width()/4
    posicaoypato = alturae/2 + pato.get_height()
    
    retpato = pato.get_rect(topleft=(posicaoxpato, posicaoypato))

    v_win = True
    while v_win:
        pos_rato = pygame.mouse.get_pos()
        ecraWin.blit(youwin, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if(0 <= x <= 20) and (0<= y <= 20):
                    print('Botão clicado') 
                    youwin = False
                    pygame.quit()
                    menulabirinto() #voltar ao menu
                    sys.exit()
                if(posicaoxpato <= x <= posicaoxpato + 75)and(posicaoypato<= y <= posicaoypato + 75):
                    print('Botao clicado')
                    pygame.quit()
                    patinhos()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    print('Botao clicado')
                    pygame.quit()
                    patinhos()
                    sys.exit()
                    
                    
        if retpato.collidepoint(pos_rato):      #METER AQUI O LOBBY DOS PATOS
           ecraWin.blit(pato2, (posicaoxpato, posicaoypato))
        else:
            ecraWin.blit(pato, (posicaoxpato, posicaoypato))
            
        if retb.collidepoint(pos_rato):
            ecraWin.blit(imagemBack2, (0, 0))
        else:
            ecraWin.blit(imagemBack, (0, 0))

        pygame.display.flip()
        pygame.time.wait(100)

def derrota(nivel):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('Musica/musicaderrota.mp3')
    pygame.mixer.music.play(-1)
    
    icon = pygame.image.load('Imagens/IconJogo.png')
    pygame.display.set_icon(icon)
    
    larguraecra = 390
    alturecra = 450
    ecraDerrota = pygame.display.set_mode((larguraecra, alturecra))
    pygame.display.set_caption('derrota...')

    icon = pygame.image.load('Imagens/IconJogo.png')
    pygame.display.set_icon(icon)


    imgb = pygame.image.load('Imagens/BackIcon.png')
    imagemBack = pygame.transform.scale(imgb, (20, 20))

    imgba = pygame.image.load('Imagens/BackIcon2.png')
    imagemBack2 = pygame.transform.scale(imgba, (20, 20))
    retb = imagemBack.get_rect(topleft=(0, 0))

    
    imgd = pygame.image.load('Imagens/derrota.png')
    imderrota = pygame.transform.scale(imgd, (390, 450))
    
    imgbd = pygame.image.load('Imagens/tryagain.png')
    tryagain = pygame.transform.scale(imgbd, (larguraecra/4, alturecra/8))
    
    imgbd2 = pygame.image.load('Imagens/tryagain2.png')
    tryagain2 = pygame.transform.scale(imgbd2, (larguraecra/4, alturecra/8))
    posicaox = (larguraecra/2) - (tryagain.get_width()/2)
    posicaoy = (alturecra/2) - (tryagain.get_height())

    ret_ta = tryagain.get_rect(topleft=(posicaox, posicaoy))
    
 
    largurat = tryagain.get_width()
    alturat = tryagain.get_width()

    v_derrota = True
    while v_derrota:
        ecraDerrota.blit(imderrota, (0, 0))
        pos_rato = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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
                if(posicaox <= x <= posicaox + largurat)and(posicaoy<= y <= posicaoy + alturat):
                    print('Botao clicado')
                    pygame.quit()
                    subprocess.run(['python', f'Nivel{nivel}.py']) #quando clica no 'facil'
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    print('Botao clicado')
                    pygame.quit()
                    subprocess.run(['python', f'Nivel{nivel}.py']) #quando clica no 'facil'
                    sys.exit()
                    
              
        if ret_ta.collidepoint(pos_rato):           
            ecraDerrota.blit(tryagain2, (posicaox, posicaoy))
        else:
            ecraDerrota.blit(tryagain, (posicaox, posicaoy))
        if retb.collidepoint(pos_rato):
            ecraDerrota.blit(imagemBack2, (0, 0))
        else:
            ecraDerrota.blit(imagemBack, (0, 0))
                
        pygame.display.flip()
        pygame.time.wait(100)

if __name__ == '__main__':
    while True:
        vitoriafinal()