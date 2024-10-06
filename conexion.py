import random

class Conexion:
    def __init__(self,nodo_origen,nodo_destino,peso):
        self.nodo_origen = nodo_origen
        self.nodo_destino = nodo_destino
        self.peso = peso

    def mutar(self):
        if random.uniform(0,1) < 0.1:
            self.peso = random.uniform(-1,1)
        else:
            self.peso += random.gauss(0.,1)/10
            if self.peso > 1:
                self.peso = 1
            if self.peso < -1:
                self.peso = -1

    def clone(self,nodo_origen,nodo_destino):
        return Conexion(nodo_origen,nodo_destino,self.peso)