#fazer o menu inicial para escolher os 3 niveis.
import pygame
import time
import sys
import os
import subprocess

'''pastaprincipal = os.path.dirname(__file__)
imagens = os.path.join(pastaprincipal, 'Imagens')
musica = os.path.join(pastaprincipal, 'Musica')'''

def menulabirinto():
    pygame.init()
    pygame.mixer.init()
    
    icon = pygame.image.load('Imagens/IconJogo.png')
    pygame.display.set_icon(icon)
    
    
    pygame.mixer.music.load('Musica/musicamenu.mp3')  #le wanski - Invincibles
    pygame.mixer.music.play(-1)
    

    

    #CORES---------------------------------------------------------
    branco = (255, 255, 255)
    preto = (0, 0, 0)
    #BOTOES INICIAIS
    cinzento_escuro = (96, 96, 96)
    #botao dos niveis
    verde_cocopassaro = (185, 232, 206)
    verde_cocopassaro_escuro = (105, 149, 124)
    #texto dos botoes
    vermelho_tijolo = (159, 82, 73)
    castanholight = (156, 109, 15)
    vermelho_escuro = (154, 55, 55) #isto nao e verde ns
    verde_agua_escuro = (63, 139, 106)
    #botao do quit
    vermelho_claro = (255, 50, 50)
    vermelho_claro_escuro = (142, 21, 21)
    #botao do back
    laranja_tijolo_escuro = (204, 102, 0)
    laranja_tijolo = (255, 134, 14)
    #---------------

    azul_escuro = ( 0, 0, 170) #ainda nao sei para que

    #--------------------------------------------------------------
    #--------------------------------
    ecrai = pygame.display.set_mode((680, 680), pygame.RESIZABLE, 32) #tela
    pygame.display.set_caption('Labirinto')

    largura_botao = ecrai.get_width()/3 #altura e largura dos botoes
    altura_botao = largura_botao/3
    
            
    imgw = pygame.image.load('Imagens/opato.png')
    pato = pygame.transform.scale(imgw, (75, 75))
    
    imgw2 = pygame.image.load('Imagens/opato2.png')
    pato2 = pygame.transform.scale(imgw2, (75, 75)) #METER AQUI O BOTAO PARA O LOBBY DS PATOS
    
    posicaoxpato = 0
    posicaoypato = ecrai.get_height() - pato.get_height()
    
    retpato = pato.get_rect(topleft=(posicaoxpato, posicaoypato))

    #CARREGAR AS IMAGENS---------------------------------------------------------------------------------------------------------------------

    imtmp = pygame.image.load('Imagens/Facil_1.png')
    NivelFacil = pygame.transform.scale(imtmp, (largura_botao, altura_botao))

    imtmp2 = pygame.image.load('Imagens/Facil2.png')
    NivelFacil2 = pygame.transform.scale(imtmp2, (largura_botao, altura_botao))

    im = pygame.image.load('Imagens/Medio_2.png')
    NivelMedio = pygame.transform.scale(im, (largura_botao, altura_botao))

    im2 = pygame.image.load('Imagens/Medio2.png')
    NivelMedio2 = pygame.transform.scale(im2, (largura_botao, altura_botao))

    imd = pygame.image.load('Imagens/Dificil_2.png')
    NivelDificil = pygame.transform.scale(imd, (largura_botao, altura_botao))

    imd2 = pygame.image.load('Imagens/Dificil2.png')
    NivelDificil2 = pygame.transform.scale(imd2, (largura_botao, altura_botao))


    img = pygame.image.load('Imagens/FundoJogo.PNG')
    imagemfundo = pygame.transform.scale(img, (680, 680))


    img2 = pygame.image.load('Imagens/quit_logo.png')
    imagemQuit = pygame.transform.scale(img2, (68, 68))

    img2a = pygame.image.load('Imagens/quit_logo2.png')
    imagemQuit2 = pygame.transform.scale(img2a, (68, 68))

    img3 = pygame.image.load('Imagens/BackIcon.png')
    imagemBack = pygame.transform.scale(img3, (68, 68))

    img3a = pygame.image.load('Imagens/BackIcon2.png')
    imagemBack2 = pygame.transform.scale(img3a, (68, 68))
    


    #----------------------------------------------------------------------------------------------------------------------------



    fonte_texto = (pygame.font.SysFont('Verdana', 30))
    '''fonte_texto.set_bold(True)'''

    x, y = (0, 0)

    correr = True 
    #--------------------------------------------------------------
    #TELA INICIAL --------------------------------------------------------------------------------------------------------------------------------------------

    pygame.display.flip()
    #1 botao para o nivel facil
    posicaobotaox = (680 - largura_botao)/2
    posicaobotaoy = (680 - altura_botao)/2 #posicao do botão do meio

    posx_botao1 = posicaobotaox
    posy_botao1 = posicaobotaoy - 2*altura_botao #botao de cima

    posx_botao3 = posicaobotaox
    posy_botao3 = posicaobotaoy + 2*altura_botao #botao de baixo



    while correr:
        ecrai.blit(imagemfundo, (0, 0))
        ecrai.blit(imagemBack, (6.8, 0))
        ecrai.blit(imagemQuit, ((680 - imagemQuit.get_width()), 0))
        ecrai.blit(NivelFacil, (posx_botao1, posy_botao1))
        ecrai.blit(NivelMedio, (posicaobotaox, posicaobotaoy))
        ecrai.blit(NivelDificil, (posx_botao3, posy_botao3))
        #isto mete as coisas na tela inicial
        retb = imagemBack.get_rect(topleft=(6.8, 0))
        retb2 = imagemQuit.get_rect(topleft=((680 - imagemQuit.get_width()), 0))
        retf = NivelFacil.get_rect(topleft=(posx_botao1, posy_botao1))
        retm = NivelMedio.get_rect(topleft=(posicaobotaox, posicaobotaoy))
        retd = NivelDificil.get_rect(topleft=(posx_botao3, posy_botao3))
        
        
        pos_rato = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                correr = False
                pygame.display.quit()
                quit()
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                #definir o clique dos botoes
                if(6.8 <= x <= 6.8 + imagemBack.get_width()) and (0<= y <= imagemBack.get_height()):
                    print('Botão clicado') #METER AUQI CODIGO PARA VOLTAR AO MENU PRINCIPAL DO JOGO
                    #MENU PRINCIPAL DO JOGO  
                #botao QUIT           
                if(680 - imagemQuit.get_width()<= x <= 680) and (0<= y <= imagemQuit.get_height()):
                    correr = False
                    pygame.quit() #quando o user clica no 'botao' Quit
                    sys.exit()
                if(posx_botao1 <= x <= posx_botao1 + largura_botao) and (posy_botao1 <= y <= posy_botao1 + altura_botao):
                    pygame.quit()
                    subprocess.run(['python', 'NivelFacil.py']) #quando clica no 'facil'
                    sys.exit()
                if(posicaobotaox <= x <= posicaobotaox + largura_botao) and (posicaobotaoy <= y <= posicaobotaoy + altura_botao):
                    pygame.quit()
                    subprocess.run(['python', 'NivelMedio.py']) #quando clica no 'facil'
                    sys.exit()
                if(posx_botao3 <= x <= posx_botao3 + largura_botao) and (posy_botao3 <= y <= posy_botao3 + altura_botao):
                    pygame.quit()
                    subprocess.run(['python', 'NivelDificil.py']) #quando clica no 'facil'
                    sys.exit()
                if(0 <= x <= pato.get_width()) and (posicaoypato<= y <= ecrai.get_height() ):
                    print('botao clicado')
                    pygame.quit()
                    subprocess.run(['python', 'Patos.py'])
                    sys.exit()      
    #--------------------------------------------------------------------------           
    #METER A COR MAIS ESCURA QUANDO O USER PASSA O RATO POR CIMA DOS BOTOES
    #se eu meter tudo num IF ficam todos os quadrados escuros quando o user passa o rato
        if retb.collidepoint(pos_rato):
            ecrai.blit(imagemBack2, (6.8, 0))
        else:
            ecrai.blit(imagemBack, (6.8, 0))

        if retb2.collidepoint(pos_rato):
            ecrai.blit(imagemQuit2, (680 - imagemQuit.get_width(), 0))
        else:
            ecrai.blit(imagemQuit, (680 - imagemQuit.get_width(), 0))

        if retf.collidepoint(pos_rato):
            ecrai.blit(NivelFacil2, (posx_botao1, posy_botao1))
        else:
            ecrai.blit(NivelFacil, (posx_botao1, posy_botao1))

        if retm.collidepoint(pos_rato):
            ecrai.blit(NivelMedio2,(posicaobotaox, posicaobotaoy))
        else:
            ecrai.blit(NivelMedio,(posicaobotaox, posicaobotaoy))

        if retd.collidepoint(pos_rato):
            ecrai.blit(NivelDificil2, (posx_botao3, posy_botao3))
        else:
            ecrai.blit(NivelDificil, (posx_botao3, posy_botao3))

        if retpato.collidepoint(pos_rato):
            ecrai.blit(pato2, (posicaoxpato, posicaoypato))
        else:
            ecrai.blit(pato, (posicaoxpato, posicaoypato))

            

        pygame.display.flip()
        
        
    pygame.display.update()

if __name__ == '__main__':
    while True:
        menulabirinto()


def salvar_pontuacao(pontos):
    with open("Pontos.txt", 'a') as ficheiro:
        ficheiro.write(f'{pontos}' + "\n")
        
    
def quack(): #meter o som do pato quando o player apanha algum
    pygame.mixer.init()
    quack = pygame.mixer.Sound('Musica/quack.mp3')
    volume = 2
    quack.set_volume(volume)
    quack.play()

def baixarvolume(): #posso mudar isto para regular volume e aceitar parametros mas nao preciso 
    vol = 0.15
    pygame.mixer.music.set_volume(vol)

    



#as imagens de fundo e os botoes foram pedidos ao GPT
#as personagens e as texturas das paredes foram retiradas do site:  https://itch.io/game-assets/tag-characters
