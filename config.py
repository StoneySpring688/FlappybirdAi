# SETTINGS DEL PROGRAMA
import pygame
import componentes

winH = 720
winW = 550
win=pygame.display.set_mode((winW,winH))
pygame.display.set_caption('Flappy Bird')

suelo = componentes.Suelo(winW)
tuberias = []