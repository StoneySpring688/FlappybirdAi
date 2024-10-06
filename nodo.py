import math


def sigmoide(x):
    return 1 / (1 + math.exp(-x))

class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.output = 0
        self.input = 0
        self.conexiones = []
        self.capa = 0

    def calcular_output(self):
        for i in range(0,len(self.conexiones)):
            self.conexiones[i].nodo_destino.input += self.conexiones[i].peso * self.output

    def activar(self):
        if self.capa == 1:
            self.output = sigmoide(self.input)
        self.calcular_output()

    def reiniciar(self):
        self.input = 0