import pygame

class UI:
	def __init__(self,surface):

		# setup
		self.display_surface = surface

		# vida
		self.barra_de_vida = pygame.image.load('./ui/barra_de_vida.png').convert_alpha()
		self.barra_de_vida_topleft = (54,39)
		self.bar_max_width = 152
		self.bar_height = 4

		# moedas
		self.coin = pygame.image.load('./ui/coin.png').convert_alpha()
		self.coin_rect = self.coin.get_rect(topleft = (40,61))
		self.font = pygame.font.Font('./ui/ARCADEPI.ttf',30)

		self.ouro = pygame.image.load('./ui/0.png').convert_alpha()
		self.ouro_rect = self.ouro.get_rect(topleft=(123, 65))
		self.font = pygame.font.Font('./ui/ARCADEPI.ttf', 30)

		self.esmeralda = pygame.image.load('./ui/2.png').convert_alpha()
		self.esmeralda_rect = self.esmeralda.get_rect(topleft=(193, 63))
		self.font = pygame.font.Font('./ui/ARCADEPI.ttf', 30)

	def mostrar_vida(self,current,full):
		self.display_surface.blit(self.barra_de_vida,(20,10))
		viida_atual_ratio = current / full
		bar_atual_width = self.bar_max_width * viida_atual_ratio
		barra_de_vida_rect = pygame.Rect(self.barra_de_vida_topleft,(bar_atual_width,self.bar_height))
		pygame.draw.rect(self.display_surface,'#dc4949',barra_de_vida_rect)

	def mostrar_moedas(self,amount):
		self.display_surface.blit(self.coin,self.coin_rect)
		qtd_moedas_surf = self.font.render(str(amount),False,'#33323d')
		qtd_moedas_rect = qtd_moedas_surf.get_rect(midleft = (self.coin_rect.right,self.coin_rect.centery))
		self.display_surface.blit(qtd_moedas_surf,qtd_moedas_rect)

	def mostrar_ouro(self,amount):
		self.display_surface.blit(self.ouro,self.ouro_rect)
		qtd_ouro_surf = self.font.render(str(amount),False,'#33323d')
		qtd_ouro_rect = qtd_ouro_surf.get_rect(midleft = (self.ouro_rect.right + 2,self.ouro_rect.centery + 2))
		self.display_surface.blit(qtd_ouro_surf,qtd_ouro_rect)

	def mostrar_esmeralda(self,amount):
		self.display_surface.blit(self.esmeralda,self.esmeralda_rect)
		qtd_esmeralda_surf = self.font.render(str(amount),False,'#33323d')
		qtd_esmeralda_rect = qtd_esmeralda_surf.get_rect(midleft = (self.esmeralda_rect.right + 6,self.esmeralda_rect.centery + 4))
		self.display_surface.blit(qtd_esmeralda_surf,qtd_esmeralda_rect)