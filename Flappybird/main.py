					################################################################################################################
					##                                                                                                            ##
					##                                                                                                            ##
					##                                     Projeto de PI - Flappy Bird                                            ##
					##                                                                                                            ##
					##                                                                                                            ##
                    ################################################################################################################

import pygame
from pygame.locals import *
import random
import time, sys

pygame.init()
pygame.mixer.init()

#Tick rate do jogo
clock = pygame.time.Clock()
fps = 60


#Sons do jogo
som_colisão = pygame.mixer.Sound('Flappybird/sounds/hit.wav')
som_click = pygame.mixer.Sound('Flappybird/sounds/wing.wav')
som_click_channel = pygame.mixer.Channel(0)
som_score = pygame.mixer.Sound('Flappybird/sounds/point.wav')
som_morte = pygame.mixer.Sound('Flappybird/sounds/die.wav')

#Tamanho da tela do jogo
screen_width = 864    #Largura da tela
screen_height = 936   #Altura da tela

#Display da tela e caption da tela
screen = pygame.display.set_mode((screen_width, screen_height))     #Dar display a tela
pygame.display.set_caption('Jogo do Pirigaito')                      #Caption do jogo

start_screen = pygame.image.load('Flappybird/img/start.png')



#Variaveis para o jogo
ground_scroll = 0         #Movimento do chão
scroll_speed = 4          #Velocidade do movimento
flying = False           # Variavel para dizer que fly é falso até algo diga o contrario no codigo
game_over = False        # Mesma cena que fly mas para o game_over
tubo_gap = 150            # 150 pixeis de gap no tubo
tubo_frequency = 1500  # 1500 milisegundos entre tubos
last_tubo = pygame.time.get_ticks() - tubo_frequency
score = 0              #Variavel para score começar a 0
passar_tubo = False    #Variavel para aumentar score caso passe o tubo
som_colisão_played = False
start_screen = True


#fonte do score
font = pygame.font.SysFont('Bauhaus 93', 60)

#cor da fonte
branco = (255, 255, 255)


#Imagens do jogo
fundo = pygame.image.load('Flappybird/img/fundo.png')              #fundo
ground_img = pygame.image.load('Flappybird/img/ground.png')        #chao
button_img = pygame.image.load('Flappybird/img/restart.png')       #reset
icone = pygame.image.load('Flappybird/img/flappy.ico')             #icone da screen
start = pygame.image.load('Flappybird/img/start.png')

pygame.display.set_icon(icone)    # display do icone 

def draw_text(text, font, text_col, x, y):          #variavel para criar o texto , a cor e a localização
	img = font.render(text, True, text_col)
	screen.blit(img,(x,y))
	
def reset_game():                         #variavel para o reset game
	tubo_group.empty()
	flappy.rect.x = 100
	flappy.rect.y = int(screen_height / 2)
	score = 0
	return score
	

class pirigaito(pygame.sprite.Sprite):             #Sprit eclass para fazer a animação do passaro , velocidade , click para ele voar etc
	def __init__(self, x, y):                      #Construtor com variaveis self , x e y
		pygame.sprite.Sprite.__init__(self)        #Construtor da parte do self
		self.images = []                           #Lista para as imagens
		self.index = 0                             #Index para 0 para fazer mais tarde um loop das 3 imagens para mostrar o passaro a voar
		self.counter = 0                           #Contador para as imagens
		for num in range(1, 4):                    #Aqui começa o loop para mudar as imagens de forma a animar o passaro
			img = pygame.image.load(f'Flappybird/img/pirigaito{num}.png')       #Load nas imagens
			self.images.append(img)                                  #Da append a lista das imagens que estão na pasta de assets no codigo
		self.image = self.images[self.index]                         
		self.rect = self.image.get_rect()                            #Fazer o retangulo do sprite no passaro para trabalhar mais tarde com colisões , posicionamento etc
		self.rect.center = [x, y]                                    #Centar o retangulo no passaro
		self.vel = 0                                                 
		self.clicked = False
		

	def update(self):

		if flying == True:     #Instruções para trabalhar com as velocidades e manter uma velocidade maxima
			#gravidade
			self.vel += 0.5        
			if self.vel > 8:
				self.vel = 8
			if self.rect.bottom < 768:
				self.rect.y += int(self.vel)

		if game_over == False:    #Instruções para verificar se o jogo foi perdido ou não
			

			#Animação do pirigaito
			self.counter += 1
			flap_cooldown = 5

			if self.counter > flap_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images):
					self.index = 0
			self.image = self.images[self.index]

			#Fazer as rotações do passaro para simular gravidade 
			self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
		else:
			self.image = pygame.transform.rotate(self.images[self.index], -90)


#Class Sprite para os tubos (deu trabalho meter estes tubos ngl)
class tubo(pygame.sprite.Sprite):
	def __init__(self, x, y, position):       #Construtor
		pygame.sprite.Sprite.__init__(self) 
		self.image = pygame.image.load('Flappybird/img/tubos.png')  #Load ao asset do tubo
		self.rect = self.image.get_rect()    #Retangulo para o tubo
		#position 1  é para os tubos do top, -1 é para os tubos do chão
		if position == 1:   #Aqui é a parte que coloca os tubos no topo
			self.image = pygame.transform.flip(self.image, False, True)   
			self.rect.bottomleft = [x, y - int(tubo_gap / 2)]
		if position == -1:   #Aqui é a parte que coloca os tubos no chão
			self.rect.topleft = [x, y + int(tubo_gap / 2)]

	def update(self):             
		self.rect.x -= scroll_speed    
		if self.rect.right < 0:
			self.kill()

class Button():             #Class para o botão de restart
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
	 
	 
	 #Meter o botão a dar direito para dar reset   
	def draw(self):
		
		action = False
		
		pos = pygame.mouse.get_pos()
		
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				action = True
		
		#botão
		screen.blit(self.image, (self.rect.x, self.rect.y))
		
		return action 

        

#Grupos dos Sprites
pirigaito_group = pygame.sprite.Group()
tubo_group = pygame.sprite.Group()

flappy = pirigaito(100, int(screen_height / 2))

pirigaito_group.add(flappy)

#colocar botão
button = Button(screen_width // 2 - 50 , screen_height // 2 - 100, button_img)


#Aqui é o loop do jogo , onde se coloca tudo que configuramos anteriormente dentro e se configura para funcionar tudo """"direito""""".
run = True
while run:
    

	clock.tick(fps)
 
	

	#fundo
	screen.blit(fundo, (0,0))

	pirigaito_group.draw(screen)
	pirigaito_group.update()
	tubo_group.draw(screen)

	#chão
	screen.blit(ground_img, (ground_scroll, 768))
 

 
	#scores
	if len(tubo_group) > 0:
		if pirigaito_group.sprites()[0].rect.left > tubo_group.sprites()[0].rect.left\
			and pirigaito_group.sprites()[0].rect.right < tubo_group.sprites()[0].rect.right\
			and passar_tubo == False:
			passar_tubo = True
		if passar_tubo == True:
			if pirigaito_group.sprites()[0].rect.left > tubo_group.sprites()[0].rect.right:
				score += 1
				passar_tubo = False
				som_score.play()
	
	 #Desenhar o score no ecra
	draw_text(str(score), font, branco, int(screen_width / 2), 20)
  
	#colisões
	if pygame.sprite.groupcollide(pirigaito_group, tubo_group, False, False) or flappy.rect.top < 0:
		if not game_over:  
			game_over = True
			flying = False
			if not som_colisão_played:
				som_colisão.play()
				
                
				 

	#verificar se o pirigaito bateu no chão
	if flappy.rect.bottom >= 768:
		if not game_over:
			game_over = True
			flying = False
			if not som_colisão_played:
				som_colisão.play()
				

 
	if game_over == False and flying == True:
	 
	

		#criar novos tubos
		time_now = pygame.time.get_ticks()
		if time_now - last_tubo > tubo_frequency:
			tubo_height = random.randint(-100, 100)
			btm_tubo = tubo(screen_width, int(screen_height / 2) + tubo_height, -1)
			top_tubo = tubo(screen_width, int(screen_height / 2) + tubo_height, 1)
			tubo_group.add(btm_tubo)
			tubo_group.add(top_tubo)
			last_tubo = time_now


		#animar o chão para faze-lo se mexer para a esquerda
		ground_scroll -= scroll_speed
		if abs(ground_scroll) > 35:
			ground_scroll = 0

		tubo_group.update()

	#verificar se o jogo acabou e meter botao reset a dar
	if game_over == True:
		if button.draw() == True:
			game_over = False
			score = reset_game()
    
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if game_over == False:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					som_click.play()
					flying = True
					flappy.vel = -10
    

	pygame.display.update()

pygame.quit()