# PAJARO (JUGADOR)
import pygame
import random
import config
import Ai

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
        self.inputs = 3
        self.vision = [0.5, 1, 0.5]
        self.ai = Ai.Ai(self.inputs)
        self.ai.generar_red()
        self.fitness = 0


    def draw(self,win):
        #print ("dibuja")
        pygame.draw.rect(win, self.color, self.pajaro)

    def colision_suelo(self,suelo):
        return pygame.Rect.colliderect(self.pajaro, suelo.recta)

    def colision_tuberia(self):
        for tuberia in config.tuberias:
            return pygame.Rect.colliderect(self.pajaro, tuberia.ractangulo_abajo) or pygame.Rect.colliderect(self.pajaro, tuberia.ractangulo_arriba)  # True si hay colision con alguna tuberia

    def avanzar(self,suelo):
        self.gravedad(suelo)
        self.fitness += 1 # cuanto más aguante vivo, mejor es

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

    @staticmethod
    def distancia_mas_cercana():
        for tuberia in config.tuberias:
            if not tuberia.passed:
                return tuberia

    def saltar(self):
        if not self.salto and not self.pajaro.y < 30: # si no está saltando y no ha subido demasiado
            self.salto = True
            self.velocidad_gravedad = -5
        if self.velocidad_gravedad >= 3: # no se puede saltar otra vez hasta que la gravedad no sea minimo 3
            self.salto = False

    #Ai

    def  get_vision(self):
        if config.tuberias: # calcular solo si hay tuberias en pantalla
            # y_tub_arriba
            self.vision[0] = max(0,self.pajaro.center[1] - self.distancia_mas_cercana().ractangulo_arriba.bottom) / 500
            #pygame.draw.line(config.win, self.color, self.pajaro.center, (self.pajaro.center[0], self.distancia_mas_cercana().ractangulo_arriba.bottom))

            # y_tub_abajo
            self.vision[2] = max(0,self.distancia_mas_cercana().ractangulo_abajo.top - self.pajaro.center[1]) / 500
            #pygame.draw.line(config.win, self.color, self.pajaro.center,(self.pajaro.center[0], self.distancia_mas_cercana().ractangulo_abajo.top))

            # x_tub
            self.vision[1] = max(0,self.distancia_mas_cercana().x - self.pajaro.center[0]) / 500
            #pygame.draw.line(config.win, self.color, self.pajaro.center, (self.distancia_mas_cercana().x, self.pajaro.center[1]), 1)



    def decidir(self):
        self.decision = self.ai.forward(self.vision)
        if self.decision > config.__UMBRAL_DE_SALTO__:
            self.saltar()

    def clone(self):
        clone = Pajaro()
        clone.fitness = self.fitness
        clone.ai = self.ai.clone()
        clone.ai.generar_red()
        return clone