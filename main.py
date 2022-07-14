import definicoes
import pygame, sys
from definicoes import *
from nivel import Nivel
from overworld import Overworld
from ui import UI
from definicoes import GAME_STATE, tela

class Game:
	def __init__(self):
		self.nivel_maximo = 0
		self.vida_total = 100
		self.vida_atual = 100
		self.moedas = 0
		self.ouro = 0
		self.esmeralda = 0

		self.overworld = Overworld(0,self.nivel_maximo,tela,self.criar_nivel)
		self.status = 'overworld'

		self.ui = UI(tela)

	def criar_nivel(self, level_atual):
		self.level = Nivel(level_atual, tela, self.criar_overworld, self.trocar_moedas, self.trocar_vida,self.trocar_ouro,self.trocar_esmeralda)
		self.status = 'level'
		definicoes.audio_jogo.play(loops= -1)
		definicoes.audio_jogo.set_volume(0.1)

	def criar_overworld(self,level_atual,novo_nivel_maximo):
		if novo_nivel_maximo > self.nivel_maximo:
			self.nivel_maximo = novo_nivel_maximo
		self.overworld = Overworld(level_atual,self.nivel_maximo,tela,self.criar_nivel)
		self.status = 'overworld'
		definicoes.audio_jogo.stop()

	def trocar_moedas(self,amount):
		self.moedas += amount

	def trocar_ouro(self,quant):
		self.ouro += quant

	def trocar_esmeralda(self,qtd):
		self.esmeralda += qtd

	def trocar_vida(self,amount):
		self.vida_atual += amount

	def verificar_game_over(self):
		if self.vida_atual <= 0:
			self.vida_atual = 100
			self.moedas = 0
			self.ouro = 0
			self.esmeralda = 0
			self.nivel_maximo = 0
			self.overworld = Overworld(0,self.nivel_maximo,tela,self.criar_nivel)
			self.status = 'overworld'
			definicoes.audio_jogo.stop()

	def run(self):
		if self.status == 'overworld':
			self.overworld.run()
		else:
			self.level.run()
			self.ui.mostrar_vida(self.vida_atual, self.vida_total)
			self.ui.mostrar_moedas(self.moedas)
			self.ui.mostrar_ouro(self.ouro)
			self.ui.mostrar_esmeralda(self.esmeralda)
			self.verificar_game_over()

pygame.init()
clock = pygame.time.Clock()
game = Game()

#Nome e ícone
pygame.display.set_caption("SAIGO ODISSEY")
icone = pygame.image.load('icone.png').convert_alpha()
pygame.display.set_icon(icone)
click = False
#Game Loop
while True:
    click = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if definicoes.GAME_STATE == 1:
        tela.fill('white')
        pause = pygame.image.load("./niveis/paused.png").convert_alpha()
        continuar4 = pygame.image.load("./niveis/continue.png").convert_alpha()
        quit = pygame.image.load("./niveis/quit.png").convert_alpha()
        volume_off = pygame.image.load("./niveis/mute_preto.png").convert_alpha()
        volume_off= pygame.transform.scale(volume_off, (30,30))
        pause_rect = pause.get_rect(center=(600, 120))
        continuar4_rect = continuar4.get_rect(center=(600, 320))
        quit_rect = quit.get_rect(center=(600, 520))
        volume_off_rect = volume_off.get_rect(center=(1250,30))
        tela.blit(volume_off, volume_off_rect)
        tela.blit(pause, pause_rect)
        tela.blit(continuar4, continuar4_rect)
        tela.blit(quit, quit_rect)
        if volume_off_rect.collidepoint(pygame.mouse.get_pos()):
            if click[0] == 1:
                 definicoes.audio_jogo.stop()
        if continuar4_rect.collidepoint(pygame.mouse.get_pos()):
            if click[0] == 1:
                 definicoes.GAME_STATE = 4
        if quit_rect.collidepoint(pygame.mouse.get_pos()):
            if click[0] == 1:
                pygame.quit()
                sys.exit()

    if definicoes.GAME_STATE == 2:
        tela.fill('white')
        vitoria = pygame.image.load("./niveis/vitoria.png").convert_alpha()
        continuar2 = pygame.image.load("./niveis/continue.png").convert_alpha()

        vitoria_rect = vitoria.get_rect(center=(600, 250))
        continuar2_rect = continuar2.get_rect(center=(600, 550))

        tela.blit(vitoria, vitoria_rect)
        tela.blit(continuar2, continuar2_rect)

        if continuar2_rect.collidepoint(pygame.mouse.get_pos()):
           if click[0] == 1:
            definicoes.GAME_STATE = 4

    if definicoes.GAME_STATE == 3:
        tela.fill('white')
        derrota = pygame.image.load("./niveis/derrota.png").convert_alpha()
        continuar = pygame.image.load("./niveis/continue.png").convert_alpha()

        derrota_rect = derrota.get_rect(center=(600, 250))
        continuar_rect = continuar.get_rect(center=(600,450))

        tela.blit(derrota, derrota_rect)
        tela.blit(continuar,continuar_rect)
        if continuar_rect.collidepoint(pygame.mouse.get_pos()):
            if click[0] == 1:
                definicoes.GAME_STATE = 4

    if definicoes.GAME_STATE == 4:
        game.run()

    pygame.display.update()
    clock.tick(60)