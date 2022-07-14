import pygame
from suporte import importar_uma_pasta
from math import sin

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, trocar_vida):
        super().__init__()
        self.importar_assests_do_personagem()
        self.frame_index = 0
        self.velocidade_da_animacao = 0.15
        self.image = self.animacoes['parado'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # movimentos do player
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 3
        self.gravidade = 0.27
        self.velocidade_pulo = -7
        #############################################################################
        self.corrigir_colisao = pygame.Rect(self.rect.topleft, (32,self.rect.height))
        # player status
        self.status = 'parado'
        self.olhando_direita = True
        self.no_chao = False
        self.no_teto = False
        self.na_esquerda = False
        self.na_direita = False

        self.trocar_vida = trocar_vida
        self.invencivel = False
        self.tempo_invencibilidade = 500
        self.tempo_vidas = 0

        self.pulo_audio = pygame.mixer.Sound('./audio/efeitos/audio_pulo.mp3')
        self.pulo_audio.set_volume(0.1)
        self.toque_audio = pygame.mixer.Sound('./audio/efeitos/audio_toque.wav')
        self.toque_audio.set_volume(0.1)

    def importar_assests_do_personagem(self):
        local_personagem = './PNG/'
        self.animacoes = {'parado': [], 'correr': [], 'pulo': [], 'cair': []}

        for animacao in self.animacoes.keys():
            local_completo = local_personagem + animacao
            self.animacoes[animacao] = importar_uma_pasta(local_completo)

    def animar(self):
        animacao = self.animacoes[self.status]

        self.frame_index += self.velocidade_da_animacao
        if self.frame_index >= len(animacao):
            self.frame_index = 0

        image = animacao[int(self.frame_index)]
        if self.olhando_direita:
            self.image = image
            self.rect.bottomleft = self.corrigir_colisao.bottomleft
        else:
            imagem_ao_contrario = pygame.transform.flip(image, True, False)
            self.image = imagem_ao_contrario
            self.rect.bottomright = self.corrigir_colisao.bottomright
        if self.invencivel:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.olhando_direita = True

        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.olhando_direita = False

        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.no_chao:
            self.jump()

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'pulo'
        elif self.direction.y > 1:
            self.status = 'cair'
        else:
            if self.direction.x != 0:
                self.status = 'correr'
            else:
                self.status = 'parado'

    def aplicar_gravidade(self):
        self.direction.y += self.gravidade
        self.corrigir_colisao.y += self.direction.y

    def jump(self):
        self.direction.y = self.velocidade_pulo
        self.pulo_audio.play()

    def tomar_dano(self):
        if not self.invencivel:
            self.toque_audio.play()
            self.trocar_vida(-10)
            self.invencivel = True
            self.tempo_vidas = pygame.time.get_ticks()

    def tempoinvencivel(self):
        if self.invencivel:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_vidas >= self.tempo_invencibilidade:
                self.invencivel = False

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def update(self):
        self.get_input()
        self.get_status()
        self.animar()
        self.tempoinvencivel()
        self.wave_value()