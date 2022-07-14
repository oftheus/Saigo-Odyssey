import pygame
from suporte import importar_uma_pasta

class Efeitos_de_Explosao(pygame.sprite.Sprite):
	def __init__(self,pos,type):
		super().__init__()
		self.frame_index = 0
		self.velocidade_da_animacao = 0.5
		if type == 'explosao':
			self.frames = importar_uma_pasta('./boom')
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)

	def animar(self):
		self.frame_index += self.velocidade_da_animacao
		if self.frame_index >= len(self.frames):
			self.kill()
		else:
			self.image = self.frames[int(self.frame_index)]

	def update(self,x_shift):
		self.animar()
		self.rect.x += x_shift
