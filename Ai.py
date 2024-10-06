import nodo
import conexion
import random

class Ai:
    def __init__(self, inputs,clone=False):
        self.conexiones = []
        self.nodos = []
        self.inputs = inputs
        self.red = []
        self.capas = 2
        self.bias_i = None
        self.out_node_i = None

        i = None
        if not clone:
            for id in range(0,self.inputs): # nodos de input
                i = id
                self.nodos.append(nodo.Nodo(id))
                self.nodos[id].capa = 0

            self.nodos.append(nodo.Nodo(3)) # bias
            self.nodos[3].capa = 0
            self.bias_i = i+1

            self.nodos.append(nodo.Nodo(4)) # nodo de output
            self.nodos[4].capa = 1
            self.out_node_i = i+2

            for n in range(0,4) : # hacer las conexiones
                self.conexiones.append(conexion.Conexion(self.nodos[n],self.nodos[4],random.uniform(-1,1))) # conexion : origen, destino, peso (entre -1 y 1)
        else:
            pass

    def conectar_nodos(self):
        for n in range(0,len(self.nodos)):
            self.nodos[n].conexiones = [] # resetear las conexiones
        for n in range(0,len(self.conexiones)):
            self.conexiones[n].nodo_origen.conexiones.append(self.conexiones[n]) # guardar las conexiones de cada nodo

    def generar_red(self):
        self.conectar_nodos()
        self.red = []  # borrar redes anteriores
        for j in range(0,self.capas):
            for n in range(0,len(self.nodos)):
                if self.nodos[n].capa == j :
                    self.red.append(self.nodos[n]) # llenar la lista ordenada por capas

    def forward(self,vision):
        for n in range(0, self.inputs):
            self.nodos[n].output = vision[n] # pasar el input a la red como output de la primera capa(antes de aplicar los pesos)
        self.nodos[3].output = 1 # bias

        for n in range(0,len(self.red)):
            self.red[n].activar() # activar los nodos de la red

        out = self.nodos[4].output
        for i in range(0,len(self.nodos)):
            self.nodos[i].reiniciar()
        #print(out)
        return out

    def clone(self):
        clone = Ai(self.inputs,True)
        for nodo in self.nodos:
            clone.nodos.append(nodo)
        for conexion in self.conexiones:
            clone.conexiones.append(conexion.clone(clone.getNodo(conexion.nodo_origen.nombre),clone.getNodo(conexion.nodo_destino.nombre)))

        clone.capas = self.capas
        clone.conectar_nodos()

        return clone

    def getNodo(self,nombre):
        for nodo in self.nodos:
            if nodo.nombre == nombre:
                return nodo

    def mutar(self):
        if random.uniform(0,1) < 0.8:
            for n in range(0,len(self.conexiones)):
                self.conexiones[n].mutar()