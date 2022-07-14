import pygame
from blocos import BlocoAnimado

class Inimigo(BlocoAnimado):
    def __init__(self,size,x,y):
        super().__init__(size,x,y,'./niveis/inimigos2/correr')
        self.rect.y += size - self.image.get_size()[1]
        self.speed = 1

    def move(self):
        self.rect.x +=self.speed

    def reverse_image(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image,True,False)

    def reverse(self):
        self.speed *= -1

    def update(self,x_shift):
        self.rect.x += x_shift
        self.animar()
        self.move()
        self.reverse_image()

class Inimigo3(BlocoAnimado):
    def __init__(self,size,x,y):
        super().__init__(size,x,y,'./niveis/inimigos3/correr')
        self.rect.y += size - self.image.get_size()[1]
        self.speed = 1

    def move(self):
        self.rect.x +=self.speed

    def reverse_image(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image,True,False)

    def reverse(self):
        self.speed *= -1

    def update(self,x_shift):
        self.rect.x += x_shift
        self.animar()
        self.move()
        self.reverse_image()