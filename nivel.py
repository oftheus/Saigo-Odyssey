import definicoes
import pygame
from suporte import importar_csv,importar_graficos
from definicoes import tamanho_bloco, altura_tela, largura_tela
from blocos import Bloco, BlocoEstatico, Moeda_Ouro, Moeda_Prata, Moeda_Esmeralda, Samurai1, Samurai2
from inimigo import Inimigo, Inimigo3
from decoracao import Ceu2, Nuvem
from player import Player
from dados_do_jogo import levels
from particulas import Efeitos_de_Explosao

class Nivel:
    def __init__(self,level_atual,superficie,criar_overworld,trocar_moedas,trocar_vida,trocar_ouro,trocar_esmeralda):

        # configuração do nível
        self.display_surface = superficie
        self.mudanca_de_fases = 0
        self.current_x = None

        #audio
        self.moeda_prata_som = pygame.mixer.Sound('./audio/efeitos/audio_moeda_prata.wav')
        self.moeda_prata_som.set_volume(0.1)
        self.moeda_ouro_som = pygame.mixer.Sound('./audio/efeitos/audio_moeda_ouro.wav')
        self.moeda_ouro_som.set_volume(0.1)
        self.moeda_esmeralda_som = pygame.mixer.Sound('./audio/efeitos/audio_esmeralda.wav')
        self.moeda_esmeralda_som.set_volume(0.1)
        self.explosao_som = pygame.mixer.Sound('./audio/efeitos/audio_explosao.wav')
        self.explosao_som.set_volume(0.1)

        #overworld
        self.criar_overworld = criar_overworld
        self.level_atual = level_atual
        nivel_dados = levels[self.level_atual]
        self.novo_nivel_maximo = nivel_dados['unlock']

        #player
        player_layout = importar_csv(nivel_dados['player'])
        self.player = pygame.sprite.GroupSingle()
        self.fim = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, trocar_vida)

        #moedas
        self.trocar_moedas = trocar_moedas
        self.trocar_ouro = trocar_ouro
        self.trocar_esmeralda = trocar_esmeralda

        #inimigo explosao
        self.explosao_sprites = pygame.sprite.Group()

        #blocos
        terreno_layout = importar_csv(nivel_dados['terreno'])
        self.terreno_sprites = self.criar_bloco(terreno_layout, 'terreno')

        grama_layout = importar_csv(nivel_dados['grama'])
        self.grama_sprites = self.criar_bloco(grama_layout, 'grama')

        moeda_ouro_layout = importar_csv(nivel_dados['moedas_ouro'])
        self.moeda_ouro_sprites = self.criar_bloco(moeda_ouro_layout, 'moedas_ouro')

        moeda_prata_layout = importar_csv(nivel_dados['moedas_prata'])
        self.moeda_prata_sprites = self.criar_bloco(moeda_prata_layout, 'moedas_prata')

        moeda_esmeralda_layout = importar_csv(nivel_dados['moedas_esmeralda'])
        self.moeda_esmeralda_sprites = self.criar_bloco(moeda_esmeralda_layout, 'moedas_esmeralda')

        objetos_layout = importar_csv(nivel_dados['objetos'])
        self.objetos_sprites = self.criar_bloco(objetos_layout, 'objetos')

        inimigo_layout = importar_csv(nivel_dados['inimigos'])
        self.inimigo_sprites = self.criar_bloco(inimigo_layout, 'inimigos')

        inimigo3_layout = importar_csv(nivel_dados['inimigos3'])
        self.inimigo3_sprites = self.criar_bloco(inimigo3_layout, 'inimigos3')

        retangulo_layout = importar_csv(nivel_dados['rect'])
        self.retangulo_sprites = self.criar_bloco(retangulo_layout, 'rect')

        samurai1_layout = importar_csv(nivel_dados['samurai1'])
        self.samurai1_sprites = self.criar_bloco(samurai1_layout, 'samurai1')

        samurai2_layout = importar_csv(nivel_dados['samurai2'])
        self.samurai2_sprites = self.criar_bloco(samurai2_layout, 'samurai2')

        self.ceu = Ceu2(15)
        nivel_largura = len(terreno_layout[0]) * tamanho_bloco
        self.nuvem = Nuvem(400, nivel_largura, 30)

    def criar_bloco(self,layout,tipo):
        sprite_group = pygame.sprite.Group()

        for linha_index, linha in enumerate(layout):
            for col_index, val in enumerate(linha):
                if val != '-1':
                    x = col_index * tamanho_bloco
                    y = linha_index * tamanho_bloco

                    if tipo == 'terreno':
                        blocos_terreno = importar_graficos('./niveis/fase1/tileset.png')
                        tile_surface = blocos_terreno[int(val)]
                        sprite = BlocoEstatico(tamanho_bloco, x, y, tile_surface)

                    if tipo == 'grama':
                        blocos_grama = importar_graficos('./niveis/fase1/aspectos.png')
                        tile3_surface = blocos_grama[int(val)]
                        sprite = BlocoEstatico(tamanho_bloco, x, y, tile3_surface)

                    if tipo == 'objetos':
                        blocos_objetos = importar_graficos('./niveis/fase1/aspectos.png')
                        tile3_surface = blocos_objetos[int(val)]
                        sprite = BlocoEstatico(tamanho_bloco, x, y, tile3_surface)

                    if tipo == 'inimigos':
                        sprite = Inimigo(tamanho_bloco,x,y)

                    if tipo == 'inimigos3':
                        sprite = Inimigo3(tamanho_bloco,x,y)

                    if tipo == 'rect':
                        sprite = Bloco(tamanho_bloco,x,y)

                    if tipo == 'moedas_ouro':
                        if val == '0':
                            sprite = Moeda_Ouro(tamanho_bloco,x,y,'./niveis/moedas_ouro/ouro',1)

                    if tipo == 'moedas_prata':
                        if val == '0':
                            sprite = Moeda_Prata(tamanho_bloco,x,y,'./niveis/moedas_prata/prata',1)

                    if tipo == 'moedas_esmeralda':
                        if val == '0':
                            sprite = Moeda_Esmeralda(tamanho_bloco,x,y,'./niveis/moedas_esmeralda/esmeralda',1)

                    if tipo == 'samurai1':
                        if val == '0':
                            sprite = Samurai1(tamanho_bloco,x,y, './niveis/samurai1',1)

                    if tipo == 'samurai2':
                        if val == '0':
                            sprite = Samurai2(tamanho_bloco,x,y, './niveis/samurai2',1)
                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self,layout,trocar_vida):
        for linha_index, linha in enumerate(layout):
            for col_index, val in enumerate(linha):
                x = col_index * tamanho_bloco
                y = linha_index * tamanho_bloco
                if val == '0':
                    sprite = Player((x, y), self.display_surface, trocar_vida)
                    self.player.add(sprite)
                if val == '1':
                    hat_surface = pygame.image.load('./icone.png').convert_alpha()
                    sprite = BlocoEstatico(tamanho_bloco,x,y,hat_surface)
                    self.fim.add(sprite)

    def colisao_inimigo(self):
        for inimigo in self.inimigo_sprites.sprites():
            if pygame.sprite.spritecollide(inimigo,self.retangulo_sprites,False):
                inimigo.reverse()

    def colisao_inimigo3(self):
        for inimigo3 in self.inimigo3_sprites.sprites():
            if pygame.sprite.spritecollide(inimigo3,self.retangulo_sprites,False):
                inimigo3.reverse()

    def colisao_do_movimento_horizontal(self):
        player = self.player.sprite
        player.corrigir_colisao.x += player.direction.x * player.speed
        sprites_que_colidem = self.terreno_sprites.sprites()
        for sprite in sprites_que_colidem:
            if sprite.rect.colliderect(player.corrigir_colisao):
                if player.direction.x < 0:
                    player.corrigir_colisao.left = sprite.rect.right
                    player.na_esquerda = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.corrigir_colisao.right = sprite.rect.left
                    player.na_direita = True
                    self.current_x = player.rect.right

    def colisao_do_movimento_vertical(self):
        player = self.player.sprite
        player.aplicar_gravidade()
        sprites_que_colidem = self.terreno_sprites.sprites()

        for sprite in sprites_que_colidem:
            if sprite.rect.colliderect(player.corrigir_colisao):
                if player.direction.y > 0:
                    player.corrigir_colisao.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.no_chao = True
                elif player.direction.y < 0:
                    player.corrigir_colisao.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.no_teto = True

        if player.no_chao and player.direction.y < 0 or player.direction.y > 1:
            player.no_chao = False

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < largura_tela/4 and direction_x < 0:
            self.mudanca_de_fases = 3
            player.speed = 0
        elif player_x > largura_tela - (largura_tela/2) and direction_x > 0:
            self.mudanca_de_fases = -3
            player.speed = 0
        else:
            self.mudanca_de_fases = 0
            player.speed = 3

    def verificar_player_no_chao(self):
        if self.player.sprite.no_chao:
            self.player_no_chao = True
        else:
            self.player_no_chao = False

    def conferir_morte(self): #derrota
        if self.player.sprite.rect.top > altura_tela:
            self.criar_overworld(self.level_atual, 0)
            definicoes.GAME_STATE = 3

    def conferir_vitoria(self): #vitoria
        if pygame.sprite.spritecollide(self.player.sprite, self.fim, False):
            self.criar_overworld(self.level_atual, self.novo_nivel_maximo)
            definicoes.GAME_STATE = 2

    def colisao_moeda_prata(self):
        moedas_prata_colididas = pygame.sprite.spritecollide(self.player.sprite, self.moeda_prata_sprites, True)
        if moedas_prata_colididas:
            self.moeda_prata_som.play()
            for Moeda_Prata in moedas_prata_colididas:
                self.trocar_moedas(Moeda_Prata.value)

    def colisao_moeda_ouro(self):
        moedas_ouro_colididas = pygame.sprite.spritecollide(self.player.sprite, self.moeda_ouro_sprites, True)
        if moedas_ouro_colididas:
            self.moeda_ouro_som.play()
            for Moeda_Ouro in moedas_ouro_colididas:
                self.trocar_ouro(Moeda_Ouro.valor)

    def conferir_colisao_esmeralda(self):
        esmeralda_colididas = pygame.sprite.spritecollide(self.player.sprite, self.moeda_esmeralda_sprites, True)
        if esmeralda_colididas:
            self.moeda_esmeralda_som.play()
            for Moeda_Esmeralda in esmeralda_colididas:
                self.trocar_esmeralda(Moeda_Esmeralda.val)

    def conferir_colisao_inimigos(self):
        inimigos_colisao = pygame.sprite.spritecollide(self.player.sprite, self.inimigo_sprites, False)

        if inimigos_colisao:
            for enemy in inimigos_colisao:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.explosao_som.play()
                    self.player.sprite.direction.y = -5
                    explosao_sprite = Efeitos_de_Explosao(enemy.rect.center, 'explosao')
                    self.explosao_sprites.add(explosao_sprite)
                    enemy.kill()
                else:
                    self.player.sprite.tomar_dano()

    def conferir_colisao_inimigos3(self):
        inimigos3_colisao = pygame.sprite.spritecollide(self.player.sprite, self.inimigo3_sprites, False)

        if inimigos3_colisao:
            for enemy in inimigos3_colisao:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.explosao_som.play()
                    self.player.sprite.direction.y = -5
                    explosao_sprite = Efeitos_de_Explosao(enemy.rect.center, 'explosao')
                    self.explosao_sprites.add(explosao_sprite)
                    enemy.kill()
                else:
                    self.player.sprite.tomar_dano()

    def mostrar_pause_on(self):
        self.pause_on = pygame.image.load("./niveis/pause.png").convert_alpha()
        self.pause_on = pygame.transform.scale(self.pause_on, (30, 30))
        self.pause_on_rect = self.pause_on.get_rect(center=(1250,30))
        self.display_surface.blit(self.pause_on, self.pause_on_rect)
        self.click = False
        click = pygame.mouse.get_pressed()
        if self.pause_on_rect.collidepoint(pygame.mouse.get_pos()):
            if click[0] == 1:
                definicoes.GAME_STATE = 1

    def run(self):
        self.ceu.draw(self.display_surface)
        self.nuvem.draw(self.display_surface, self.mudanca_de_fases)

        self.objetos_sprites.update(self.mudanca_de_fases)
        self.objetos_sprites.draw(self.display_surface)

        self.terreno_sprites.update(self.mudanca_de_fases)
        self.terreno_sprites.draw(self.display_surface)

        self.grama_sprites.update(self.mudanca_de_fases)
        self.grama_sprites.draw(self.display_surface)

        self.inimigo_sprites.update(self.mudanca_de_fases)
        self.inimigo3_sprites.update(self.mudanca_de_fases)
        self.retangulo_sprites.update(self.mudanca_de_fases)
        self.colisao_inimigo()
        self.colisao_inimigo3()
        self.inimigo_sprites.draw(self.display_surface)
        self.inimigo3_sprites.draw(self.display_surface)
        self.explosao_sprites.update(self.mudanca_de_fases)
        self.explosao_sprites.draw(self.display_surface)

        self.moeda_ouro_sprites.update(self.mudanca_de_fases)
        self.moeda_ouro_sprites.draw(self.display_surface)

        self.samurai1_sprites.update(self.mudanca_de_fases)
        self.samurai1_sprites.draw(self.display_surface)

        self.samurai2_sprites.update(self.mudanca_de_fases)
        self.samurai2_sprites.draw(self.display_surface)

        self.moeda_prata_sprites.update(self.mudanca_de_fases)
        self.moeda_prata_sprites.draw(self.display_surface)

        self.moeda_esmeralda_sprites.update(self.mudanca_de_fases)
        self.moeda_esmeralda_sprites.draw(self.display_surface)

        self.player.update()
        self.colisao_do_movimento_horizontal()
        self.verificar_player_no_chao()
        self.colisao_do_movimento_vertical()
        self.scroll_x()
        self.player.draw(self.display_surface)

        self.fim.update(self.mudanca_de_fases)
        self.fim.draw(self.display_surface)

        self.conferir_morte()
        self.conferir_vitoria()
        self.colisao_moeda_prata()
        self.colisao_moeda_ouro()
        self.conferir_colisao_esmeralda()
        self.conferir_colisao_inimigos()
        self.conferir_colisao_inimigos3()

        self.mostrar_pause_on()


