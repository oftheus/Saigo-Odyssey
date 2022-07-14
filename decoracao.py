from definicoes import numero_de_blocos_vertical, tamanho_bloco, largura_tela
import pygame
from blocos import BlocoAnimado, BlocoEstatico
from suporte import importar_uma_pasta
from random import choice, randint

class Ceu:
    def __init__(self, horizonte,style = 'level'):
        self.top = pygame.image.load('./decoracao/ceu/ceu_bottom.png').convert_alpha()
        self.bottom = pygame.image.load('./decoracao/ceu/ceu_top.png').convert_alpha()
        self.middle = pygame.image.load('./decoracao/ceu/ceu_middle.png').convert_alpha()
        self.horizonte = horizonte

        self.top = pygame.transform.scale(self.top, (largura_tela, tamanho_bloco))
        self.bottom = pygame.transform.scale(self.bottom, (largura_tela, tamanho_bloco))
        self.middle = pygame.transform.scale(self.middle, (largura_tela, tamanho_bloco))

        self.style = style
        if self.style == 'overworld':
            arvore_surfaces = importar_uma_pasta('./overworld/arvores')
            self.arvores = []

            for superficie in [choice(arvore_surfaces) for image in range(15)]:
                x = randint(0,largura_tela)
                y = (self.horizonte * tamanho_bloco) + randint(20,40)
                rect = superficie.get_rect(midbottom = (x,y))
                self.arvores.append((superficie,rect))

            nuvem_surfaces = importar_uma_pasta('./overworld/nuvens')
            self.nuvens = []

            for superficie in [choice(nuvem_surfaces) for image in range(10)]:
                x = randint(0, largura_tela)
                y = randint(0, (self.horizonte * tamanho_bloco)-80)
                rect = superficie.get_rect(midbottom=(x, y))
                self.arvores.append((superficie, rect))

    def draw(self, superficie):
        for linha in range(numero_de_blocos_vertical):
            y = linha * tamanho_bloco
            if linha > self.horizonte:
                superficie.blit(self.top, (0, y))
            elif linha == self.horizonte:
                superficie.blit(self.middle, (0, y))
            else:
                superficie.blit(self.bottom, (0, y))

        if self.style == 'overworld':
            for arvore in self.arvores:
                superficie.blit(arvore[0],arvore[1])
            for nuvem in self.nuvens:
                superficie.blit(nuvem[0],nuvem[1])

class Ceu2:
    def __init__(self, horizonte):
        self.top = pygame.image.load('./niveis/decoracao/ceu2/ceu_top.png').convert_alpha()
        self.bottom = pygame.image.load('./niveis/decoracao/ceu2/ceu_bottom.png').convert_alpha()
        self.middle = pygame.image.load('./niveis/decoracao/ceu2/ceu_middle.png').convert_alpha()
        self.horizonte = horizonte

        self.top = pygame.transform.scale(self.top, (largura_tela, tamanho_bloco))
        self.bottom = pygame.transform.scale(self.bottom, (largura_tela, tamanho_bloco))
        self.middle = pygame.transform.scale(self.middle, (largura_tela, tamanho_bloco))

    def draw(self, superficie):
        for linha in range(numero_de_blocos_vertical):
            y = linha * tamanho_bloco
            if linha > self.horizonte:
                superficie.blit(self.top, (0, y))
            elif linha == self.horizonte:
                superficie.blit(self.middle, (0, y))
            else:
                superficie.blit(self.bottom, (0, y))

class Nuvem:
    def __init__(self, horizonte, nivel_largura, nuvem_number):
        nuvem_surf_list = importar_uma_pasta('./decoracao/nuvem')
        min_x = -largura_tela
        max_x = nivel_largura + largura_tela
        min_y = 0
        max_y = horizonte
        self.nuvem_sprites = pygame.sprite.Group()

        for nuvem in range(nuvem_number):
            nuvem = choice(nuvem_surf_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            sprite = BlocoEstatico(0, x, y, nuvem)
            self.nuvem_sprites.add(sprite)

    def draw(self, surface, x_shift):
        self.nuvem_sprites.update(x_shift)
        self.nuvem_sprites.draw(surface)
