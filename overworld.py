import pygame
from dados_do_jogo import levels
from suporte import importar_uma_pasta
from decoracao import Ceu
from PPlay.gameimage import *

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, velocidade_do_icone,path):
        super().__init__()
        self.frames = importar_uma_pasta(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        if status == 'disponivel':
            self.status = 'disponivel'
        else:
            self.status = 'nao_disponivel'
        self.rect = self.image.get_rect(center=pos)

        self.zona_detectar = pygame.Rect(self.rect.centerx - (velocidade_do_icone / 2), self.rect.centery - (velocidade_do_icone / 2),
                                          velocidade_do_icone, velocidade_do_icone)

    def animar(self):
            self.frame_index += 0.15
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            self.image = self.frames[int(self.frame_index)]

    def update(self):

        if self.status == 'disponivel':
            self.animar()
        else:
            pintar = self.image.copy()
            pintar.fill('salmon', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(pintar,(0,0))

class icone(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		self.pos = pos
		self.image = pygame.image.load('./niveis/icone_node.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)

	def update(self):
		self.rect.center = self.pos

class Overworld:
    def __init__(self, nivel_inicial, nivel_maximo, surface, criar_nivel):

        self.display_surface = surface
        self.nivel_maximo = nivel_maximo
        self.level_atual = nivel_inicial
        self.criar_nivel = criar_nivel

        self.se_movendo = False
        self.direcao_do_movimento = pygame.math.Vector2(0, 0)
        self.speed = 8

        self.setup_nodes()
        self.setup_icone()
        self.ceu = Ceu(15, 'overworld')

        self.tempo_inicial = pygame.time.get_ticks()
        self.permitir_clique = False
        self.duracao = 300

        pygame.mixer.music.load('./audio/audio_menu.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.08)

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        for index, dados_do_node in enumerate(levels.values()):
            if index <= self.nivel_maximo:
                node_sprite = Node(dados_do_node['node_pos'], 'disponivel', self.speed,dados_do_node['node_graphics'])
            else:
                node_sprite = Node(dados_do_node['node_pos'], 'nao_disponivel', self.speed,dados_do_node['node_graphics'])
            self.nodes.add(node_sprite)

    def desenhar_caminho_nodes(self):
        if self.nivel_maximo > 0:
            pontos = [node['node_pos'] for index, node in enumerate(levels.values()) if index <= self.nivel_maximo]
            pygame.draw.lines(self.display_surface, '#191970', False, pontos, 6)

    def setup_icone(self):
        self.icone = pygame.sprite.GroupSingle()
        icone_sprite = icone(self.nodes.sprites()[self.level_atual].rect.center)
        self.icone.add(icone_sprite)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.se_movendo and self.permitir_clique:
            if keys[pygame.K_RIGHT] and self.level_atual < self.nivel_maximo:
                self.direcao_do_movimento = self.pegar_dados_do_movimento('proximo')
                self.level_atual += 1
                self.se_movendo = True
            elif keys[pygame.K_LEFT] and self.level_atual > 0:
                self.direcao_do_movimento = self.pegar_dados_do_movimento('anterior')
                self.level_atual -= 1
                self.se_movendo = True
            elif keys[pygame.K_SPACE]:
                self.criar_nivel(self.level_atual)
                pygame.mixer.music.pause()

    def pegar_dados_do_movimento(self, target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.level_atual].rect.center)

        if target == 'proximo':
            end = pygame.math.Vector2(self.nodes.sprites()[self.level_atual + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.level_atual - 1].rect.center)

        return (end - start).normalize()

    def update_icone_pos(self):
        if self.se_movendo and self.direcao_do_movimento:
            self.icone.sprite.pos += self.direcao_do_movimento * self.speed
            target_node = self.nodes.sprites()[self.level_atual]
            if target_node.zona_detectar.collidepoint(self.icone.sprite.pos):
                self.se_movendo = False
                self.direcao_do_movimento = pygame.math.Vector2(0, 0)

    def input_timer(self):
        if not self.permitir_clique:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_inicial >= self.duracao:
                self.permitir_clique = True

    def mostar_sair(self):
        self.sair = pygame.image.load("./overworld/botao_sair.png").convert_alpha()
        self.sair = pygame.transform.scale(self.sair, (40,40))
        self.sair_rect = self.sair.get_rect(center=(1250, 610))
        self.display_surface.blit(self.sair, self.sair_rect)
        self.click = False

    def mostrar_volume_on(self):
        self.volume_on = pygame.image.load("./overworld/volume_on.png").convert_alpha()
        self.volume_on = pygame.transform.scale(self.volume_on, (30, 30))
        self.volume_on_rect = self.volume_on.get_rect(center=(1250,30))
        self.display_surface.blit(self.volume_on, self.volume_on_rect)
        self.click = False

    def mostrar_volume_off(self):
        self.volume_off = pygame.image.load("./overworld/volume_off.png").convert_alpha()
        self.volume_off = pygame.transform.scale(self.volume_off, (30,30))
        self.volume_off_rect = self.volume_off.get_rect(center=(1200,30))
        self.display_surface.blit(self.volume_off, self.volume_off_rect)
        self.click = False

    def run(self):
        self.input_timer()
        self.input()
        self.update_icone_pos()
        self.icone.update()
        self.nodes.update()
        click = pygame.mouse.get_pressed()

        self.ceu.draw(self.display_surface)
        self.desenhar_caminho_nodes()
        self.nodes.draw(self.display_surface)
        self.icone.draw(self.display_surface)

        self.mostrar_volume_on()
        if self.volume_on_rect.collidepoint(pygame.mouse.get_pos()):
            if click[0] == 1:
                pygame.mixer.music.unpause()
        self.mostrar_volume_off()
        if self.volume_off_rect.collidepoint(pygame.mouse.get_pos()):
            if click[0] == 1:
                pygame.mixer.music.pause()
        self.mostar_sair()
        if self.sair_rect.collidepoint(pygame.mouse.get_pos()):
            if click[0] == 1:
                pygame.quit()
                sys.exit()
