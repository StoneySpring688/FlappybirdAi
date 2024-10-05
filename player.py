# PAJARO (JUGADOR)
import pygame
import random
import config

class Pajaro:
    def __init__(self):
        # Pajaro
        self.x,self.y = 50,200
        self.pajaro = pygame.Rect(self.x, self.y, 20, 20)
        self.color = (random.randint(100,255),random.randint(100,255),random.randint(100,255))
        self.velocidad_gravedad = 0
        self.salto = False
        self.muerto = False
        # Ai
        self.decision = None

    def draw(self,win):
        #print ("dibuja")
        pygame.draw.rect(win, self.color, self.pajaro)

    def colision_suelo(self,suelo):
        return pygame.Rect.colliderect(self.pajaro, suelo.recta)

    def colision_tuberia(self):
        for tuberia in config.tuberias:
            return pygame.Rect.colliderect(self.pajaro, tuberia.ractangulo_abajo) or pygame.Rect.colliderect(self.pajaro, tuberia.ractangulo_arriba)  # True si hay colision con alguna tuberia

    def gravedad(self,suelo):
        if not (self.colision_suelo(suelo) or self.colision_tuberia()): # no hay colision con el suelo o no ha subido demasiado
            #print(self.velocidad_gravedad,self.y)
            self.velocidad_gravedad += 0.25
            self.pajaro.y += self.velocidad_gravedad
            if self.velocidad_gravedad > 5: # capar la gravedad
                self.velocidad_gravedad = 5
        else:
            self.salto = False
            self.velocidad_gravedad = 0
            self.muerto = True

    def saltar(self):
        if not self.salto and not self.pajaro.y < 30: # si no está saltando y no ha subido demasiado
            self.salto = True
            self.velocidad_gravedad = -5
        if self.velocidad_gravedad >= 3: # no se puede saltar otra vez hasta que la gravedad no sea minimo 3
            self.salto = False

    #Ai
    def decidir(self):
        self.decision = random.uniform(0,1)
        if self.decision > 0.6: # TODO cambiar a 0.73
            self.saltar()