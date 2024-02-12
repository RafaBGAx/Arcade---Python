import pygame
import sys
import subprocess
import os

pygame.init()

ecrainicial = pygame.display.set_mode((700, 600))

#---- Caminho dos jogos--------------#
caminho_absoluto = os.path.abspath('fuga!/fuga!.exe')
caminho_absoluto1 = os.path.abspath('Flappybird/main.exe')
caminho_absoluto2 = os.path.abspath('SpaceShooter/main.exe')
caminho_absoluto3 = os.path.abspath('Labirinto/ProjetoLabirinto.exe')
caminho_absoluto4 = os.path.abspath('pacman/pacman.exe')


#--------Imagens do menu principal-----#
img = pygame.image.load('imagens_m/MenuInicial.png')
fundo = pygame.transform.scale(img, (700, 600))

imgPlay = pygame.image.load('imagens_m/PlayMenuInicial.png')
Play = pygame.transform.scale(imgPlay, (311, 64))

imgPlay2 = pygame.image.load('imagens_m/PlayMenuInicial2.png')
imgPlay2 = pygame.transform.scale(imgPlay2, (311, 64))

imagemQuit = pygame.image.load('imagens_m/ExitMenuInicial.png')
Quit = pygame.transform.scale(imagemQuit, (311, 64))

imagemQuit2 = pygame.image.load('imagens_m/ExitMenuInicial2.png')
Quit2 = pygame.transform.scale(imagemQuit2, (311, 64))

#-------Imagens dos icons dos jogos ----------#

flapy = pygame.image.load('imgj/fllapy1.png')
flapy = pygame.transform.scale(flapy, (64, 64))

flapy12 = pygame.image.load('imgj/fllapy12.png')
flapy12 = pygame.transform.scale(flapy12, (64, 64))

fuga = pygame.image.load('imgj/icon_fuga.png')
fuga = pygame.transform.scale(fuga, (64, 64))

fuga12 = pygame.image.load('imgj/icon_fuga1.png')
fuga12 = pygame.transform.scale(fuga12, (64, 64))

nav = pygame.image.load('imgj/nave1.png')
nav = pygame.transform.scale(nav, (64, 64))

nav12 = pygame.image.load('imgj/nave12.png')
nav12 = pygame.transform.scale(nav12, (64, 64))

lab = pygame.image.load('imgj/lab1.png')
lab = pygame.transform.scale(lab, (64, 64))

lab12 = pygame.image.load('imgj/lab12.png')
lab12 = pygame.transform.scale(lab12, (64, 64))


pac = pygame.image.load('imgj/pac1.png')
pac = pygame.transform.scale(pac, (64, 64))

pac12 = pygame.image.load('imgj/pac12.png')
pac12 = pygame.transform.scale(pac12, (64, 64))


#----Sons--------------------------#
musica = pygame.mixer.Channel(1)
musica2 = pygame.mixer.Channel(2)
musica3 = pygame.mixer.Channel(3)
musica4 = pygame.mixer.Channel(4)
musica5 = pygame.mixer.Channel(5)
musica_m =pygame.mixer.Channel(6)
som_n1 = pygame.mixer.Sound('sons_m/bip.mp3')
som_n1.set_volume(0.3)

som_n2 = pygame.mixer.Sound('sons_m/botão_j.mp3')
som_n2.set_volume(0.3)
som_menu = pygame.mixer.Sound('sons_m/musica_menu.wav')
som_menu.set_volume(0.05)


pygame.display.set_caption('Jogos Arcade')

posicaoplayx = 355 - Play.get_width() / 2
posicaoplayy = 580 - (2 * Play.get_height())

posicaoquitx = 355 - (Quit.get_width() / 2)
posicaoquity = 580 - (Quit.get_height())

#------Imagem do menu 2 ----#
img_bg = pygame.image.load('imgj/menu_final12.jpg')
fonte = pygame.font.SysFont('comicsansms', 20, True, False)


#----- função para estilizar uma mensagem ------#
def exibe_mensagem(msg, tamanho, cor):
  
    fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)
    mensagem = f'{msg}' 
    texto_formatado = fonte.render(mensagem, True, cor)
    return texto_formatado

#---------- Função para exibir o menu dos jogos ---------#
def menu_jogos():
    hover = (184, 184, 184) 
    som_j = True
    som_j1= True
    som_j2 = True
    som_j3 = True
    som_j4 = True
    while True:
        ecrainicial.blit(img_bg, (0, 0))

        ecrainicial.blit(flapy, (170, 180))
        flapyt = exibe_mensagem('FlappyBird',20,(255,255,255))
        flapy_rect = flapy.get_rect(topleft=(170,180))
       
        
        if flapy_rect.collidepoint(pygame.mouse.get_pos()):
           if som_j == True and not musica.get_busy():
               musica.play(som_n2)  
           som_j = False
           flapy1 = pygame.transform.scale(flapy12, (70, 70))
           ecrainicial.blit(flapy1, (170, 180))
           flapyt = exibe_mensagem('FlappyBird',25,hover)
           if pygame.mouse.get_pressed()[0]:
            musica_m.stop()
            subprocess.run(caminho_absoluto1, shell=True)
        else:
          som_j = True
        ecrainicial.blit(flapyt, (150, 250))


        ecrainicial.blit(fuga, (250, 320))
        fugat = fonte.render('Fuga!',True,(255,255,255))
        fuga_rect = fuga.get_rect(topleft=(250,320))
        
        if fuga_rect.collidepoint(pygame.mouse.get_pos()):
           if som_j1 == True and not musica2.get_busy():
               musica2.play(som_n2)  
           som_j1 = False
           fuga1 = pygame.transform.scale(fuga12, (70, 70))
           ecrainicial.blit(fuga1, (250, 320))
           fugat = exibe_mensagem('Fuga!',25,hover)
           if pygame.mouse.get_pressed()[0]:
            musica_m.stop()
            subprocess.run(caminho_absoluto, shell=True)
        else:
          som_j1 = True
        ecrainicial.blit(fugat, (255, 400))
        

        ecrainicial.blit(nav, (480, 180))
        navet = fonte.render('SpaceShooter',True,(255,255,255))
        nave_rect = nav.get_rect(topleft=(480,180))
        if nave_rect.collidepoint(pygame.mouse.get_pos()):
           if som_j2 == True and not musica2.get_busy():
               musica2.play(som_n2)  
           som_j2 = False
           nave1 = pygame.transform.scale(nav12, (70, 70))
           ecrainicial.blit(nave1, (480, 180))
           navet = exibe_mensagem('SpaceShooter',25,hover)
           if pygame.mouse.get_pressed()[0]:
            musica_m.stop()
            subprocess.run(caminho_absoluto2, shell=True)
        else:
          som_j2 = True
        ecrainicial.blit(navet, (440, 250))
       
       
       
        ecrainicial.blit(lab, (400, 320))
        labt = fonte.render('Labirinto',True,(255,255,255))
        lab_rect = lab.get_rect(topleft=(400,320))
        if lab_rect.collidepoint(pygame.mouse.get_pos()):
           if som_j3 == True and not musica3.get_busy():
               musica3.play(som_n2)  
           som_j3 = False
           lab1 = pygame.transform.scale(lab12, (70, 70))
           ecrainicial.blit(lab1, (400, 320))
           labt = exibe_mensagem('Labirinto',25,hover)
           if pygame.mouse.get_pressed()[0]:
            musica_m.stop()
            subprocess.run(caminho_absoluto3, shell=True)
        else:
           som_j3 = True
        ecrainicial.blit(labt, (390, 400))
       
       
        ecrainicial.blit(pac, (325, 180))
        pact = fonte.render('Pac-man',True,(255,255,255))
        pac_rect = pac.get_rect(topleft=(325,180)) 
        if pac_rect.collidepoint(pygame.mouse.get_pos()):
           if som_j4 == True and not musica4.get_busy():
               musica4.play(som_n2)  
           som_j4 = False
           pac1 = pygame.transform.scale(pac12, (70, 70))
           ecrainicial.blit(pac1, (325, 180))
           pact = exibe_mensagem('Pac-man',25,hover)
           if pygame.mouse.get_pressed()[0]:
            musica_m.stop()
            subprocess.run(caminho_absoluto4, shell=True)
        else:
           som_j4 = True
        
        
        ecrainicial.blit(pact, (320, 250))



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Sair do loop e retornar ao chamador

        pygame.display.update()


#---------- Função para exibir o menu principal------------#
def main():
    som_p = True
    somp_1 = True
    while True:
        
        ecrainicial.blit(fundo, (0, 0))
        if not  musica_m.get_busy():
          musica_m.play(som_menu,loops=-1)

        botaoplay = Play.get_rect(topleft=(posicaoplayx, posicaoplayy))
        botaoquit = Quit.get_rect(topleft=(posicaoquitx, posicaoquity))

        pos_rato = pygame.mouse.get_pos()

        ecrainicial.blit(Play, (posicaoplayx, posicaoplayy))
        if botaoplay.collidepoint(pygame.mouse.get_pos()):
             if som_p == True and not musica.get_busy():
               musica.play(som_n1)  
             ecrainicial.blit(imgPlay2, (posicaoplayx, posicaoplayy))
             som_p = False
          
             if pygame.mouse.get_pressed()[0]:
               menu_jogos()
        else:
            som_p = True
        ecrainicial.blit(Quit, (posicaoquitx, posicaoquity))
        
        if botaoquit.collidepoint(pygame.mouse.get_pos()):
             if som_p1 == True and not musica2.get_busy():
               musica2.play(som_n1)  
             ecrainicial.blit(Quit2, (posicaoquitx, posicaoquity))
             som_p1 = False
             if pygame.mouse.get_pressed()[0]:
                pygame.quit()
                sys.exit()
        else:
            som_p1 = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
       
main()
# Adicionado para iniciar o jogo

