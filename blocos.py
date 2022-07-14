import pygame
from suporte import importar_uma_pasta

class Bloco(pygame.sprite.Sprite):
	def __init__(self,size,x,y):
		super().__init__()
		self.image = pygame.Surface((size, size))
		self.rect = self.image.get_rect(topleft = (x,y))

	def update(self,x_shift):
		self.rect.x += x_shift

class BlocoEstatico(Bloco):
	def __init__(self,size,x,y,superficie):
		super().__init__(size,x,y)
		self.image = superficie

class BlocoAnimado(Bloco):
	def __init__(self,size,x,y,path):
		super().__init__(size,x,y)
		self.frames = importar_uma_pasta(path)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]

	def animar(self):
		self.frame_index += 0.15
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	def update(self,x_shift):
		self.animar()
		self.rect.x += x_shift

class Moeda_Ouro (BlocoAnimado):
	def __init__(self,size,x,y,path,valor):
		super().__init__(size,x,y,path)
		center_x = x + int(size / 2)
		center_y = y + int(size / 2)
		self.rect = self.image.get_rect(center = (center_x,center_y))
		self.valor = valor

class Moeda_Prata (BlocoAnimado):
	def __init__(self,size,x,y,path,value):
		super().__init__(size,x,y,path)
		center_x = x + int(size / 2)
		center_y = y + int(size / 2)
		self.rect = self.image.get_rect(center = (center_x,center_y))
		self.value = value

class Moeda_Esmeralda (BlocoAnimado):
	def __init__(self,size,x,y,path,val):
		super().__init__(size,x,y,path)
		center_x = x + int(size / 2)
		center_y = y + int(size / 2)
		self.rect = self.image.get_rect(center = (center_x,center_y))
		self.val = val

class Samurai1 (BlocoAnimado):
	def __init__(self,size,x,y,path,vall):
		super().__init__(size,x,y,path)
		center_x = x + int(size / 2)
		center_y = y + int(size / 4)
		self.rect = self.image.get_rect(center = (center_x,center_y))
		self.vall = vall

class Samurai2 (BlocoAnimado):
	def __init__(self,size,x,y,path,valll):
		super().__init__(size,x,y,path)
		center_x = x + int(size / 2)
		center_y = y + int(size / 3)
		self.rect = self.image.get_rect(center = (center_x,center_y))
		self.vall = valll