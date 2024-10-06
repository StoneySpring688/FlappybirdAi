import operator
import random
from operator import index


class Especie:
    def __init__(self,pajaro):
        self.pajaros = []
        self.fitness_medio = 0
        self.umbral_compatibilidad = 1.2
        self.pajaros.append(pajaro)
        self.mejor_fitness = pajaro.fitness
        self.mejor_ai = pajaro.ai.clone()
        self.mejor_pajaro = pajaro.clone()
        self.inadaptacion = 0

    def compatible(self,ai):
        compatibilidad = self.diferencial_pesos(self.mejor_ai,ai)
        return compatibilidad > self.umbral_compatibilidad

    @staticmethod
    def diferencial_pesos(ai1,ai2):
        diferencial = 0
        for i in range(0,len(ai1.conexiones)):
            diferencial += abs(ai1.conexiones[i].peso - ai2.conexiones[i].peso)
        return diferencial

    def añadir_a_especie(self,pajaro):
        self.pajaros.append(pajaro)
        if pajaro.fitness > self.mejor_fitness: # TODO: revisar
            self.inadaptacion = 0
            self.mejor_fitness = pajaro.fitness
            # self.mejor_ai = pajaro.ai.clone()
            self.mejor_pajaro = pajaro.clone()
        else:
            self.inadaptacion += 1

    def pajaros_por_fitness(self):
        self.pajaros.sort(key=operator.attrgetter('fitness'),reverse=True)

    def fitness(self):
        fitness = 0
        for pajaro in self.pajaros:
            fitness += pajaro.fitness
        if self.pajaros:
            self.fitness_medio = int(fitness / len(self.pajaros))
        else:
            self.fitness_medio = 0

    def reproducir(self):
        idx = 0
        if len(self.pajaros) > 1:
            idx = random.randint(1,len(self.pajaros))-1 # como ya se ha añadido una copia del mejor en la poblacion, se excluye de la reproduccion

        try:
            nene = self.pajaros[idx].clone()
            nene.ai.mutar()
            return nene
        except IndexError:
            exit(1)


