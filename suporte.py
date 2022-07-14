from csv import reader
from definicoes import tamanho_bloco
from os import walk
import pygame

def importar_uma_pasta(path):
    surface_list = []

    for _,__,image_files in walk(path):
        for image in image_files:
            local_completo = path + '/' + image
            image_surf = pygame.image.load(local_completo).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

def importar_csv(path):
    terreno_mapa = []
    with open(path) as mapa:
        nivel = reader(mapa,delimiter = ',')
        for linha in nivel:
            terreno_mapa.append(list(linha))
        return terreno_mapa

def importar_graficos(path):
    superficie = pygame.image.load(path).convert_alpha()
    bloco_num_x = int(superficie.get_size()[0] / tamanho_bloco)
    bloco_num_y = int(superficie.get_size()[1] / tamanho_bloco)

    cut_blocos = []
    for linha in range(bloco_num_y):
        for col in range(bloco_num_x):
            x = col * tamanho_bloco
            y = linha * tamanho_bloco
            nova_superficie = pygame.Surface((tamanho_bloco, tamanho_bloco),flags = pygame.SRCALPHA)
            nova_superficie.blit(superficie, (0,0),pygame.Rect(x,y,tamanho_bloco,tamanho_bloco))
            cut_blocos.append(nova_superficie)
    return cut_blocos



