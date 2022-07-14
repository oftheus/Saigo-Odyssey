import pygame
pygame.init()
numero_de_blocos_vertical = 20
tamanho_bloco = 32
GAME_STATE = 4
largura_tela = 1280
altura_tela = numero_de_blocos_vertical * tamanho_bloco
tela = pygame.display.set_mode((largura_tela, altura_tela))
audio_jogo = pygame.mixer.Sound('./audio/audio_jogo.mp3')

