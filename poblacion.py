# POBLACION (CONJUNTO DE PLAYERS)
import config
import player
import math
import especies
import operator

class Poblacion:
    def __init__(self,n=1):
        self.pajaros = []
        self.n = n
        self.generacion = 1
        self.especies = []
        for i in range(0,n):
            self.pajaros.append(player.Pajaro())

    def update_pajaros_vivos(self):
        for pajaro in self.pajaros:
            if not pajaro.muerto:
                #print(self.pajaro.muerto)
                pajaro.get_vision()
                pajaro.decidir()
                pajaro.draw(config.win)
                pajaro.avanzar(config.suelo)

    def selection(self):
        print('SANDIVIDIO EN ESPECIES')
        self.clasificar_especies()

        print("FITNESS")
        self.fitness()

        self.eliminar_extintos()

        print("LOS QUE NO SE ADAPTARoN MURIERON")
        self.purgar()

        print("ELEGIR AL MEJOR UNGA UNGA")
        self.especies_por_fitness()

        print("SAN CASAO Y TIENEN NENES")
        self.avanzar_generacion()

        print("#######################")

    def clasificar_especies(self):
        for especie in self.especies:
            especie.pajaros = []
        for pajaro in self.pajaros:
            darwin_aprueba = False
            for especie in self.especies:
                if especie.compatible(pajaro.ai):
                    especie.añadir_a_especie(pajaro)
                    darwin_aprueba = True
                    break
            if not darwin_aprueba:
                self.especies.append(especies.Especie(pajaro))

    def fitness(self):
        # el fitness de cada pajaro vivo se calcula de forma automática conforme avanza el programa, ya que su fitness  es el tiempo que aguantan vivos
        for especie in self.especies:
            especie.fitness() # calculate_average_fitness

    def especies_por_fitness(self):
        for especie in self.especies:
            especie.pajaros_por_fitness() # sort_players_by-fitness
        self.especies.sort(key=operator.attrgetter('mejor_fitness'),reverse=True)

    def eliminar_extintos(self):
        for especie in self.especies:
            if len(especie.pajaros) == 0:
                self.especies.remove(especie)

    def purgar(self):
        pajaros_purgar = []
        especies_purgar = []

        for especie in self.especies:
            if especie.inadaptacion >= 8:
                if len(self.especies) > len(especies_purgar) + 1:
                    especies_purgar.append(especie)
                    for pajaro in especie.pajaros:
                        pajaros_purgar.append(pajaro)
                else:
                    especie.inadaptacion = 0 # si es la ultima en sobrevivir, entonces ya debe estar bien adaptada
        for pajaros in pajaros_purgar:
            self.pajaros.remove(pajaros)
        for especie in especies_purgar:
            self.especies.remove(especie)

    def avanzar_generacion(self):
        nenes = []

        # clonar el mejor unga unga a la siguiente generación
        for especie in self.especies:
            nenes.append(especie.mejor_pajaro.clone()) # champion

        # llenar la población con nenes
        nenes_por_especie = math.floor(self.n - len(self.especies)/len(self.especies))
        for especie in self.especies:
            for i in range(0, nenes_por_especie):
                nenes.append(especie.reproducir())

        while len(nenes) < self.n:
            nenes.append(self.especies[0].reproducir()) #  rellenar la generación con niños de la mejor especie

        self.pajaros = []
        for nene in nenes:
            self.pajaros.append(nene)
        self.generacion += 1

    def sanExtintoLosMuTontos(self):
        extintos = True
        for pajaro in self.pajaros:
            if not pajaro.muerto:
                extintos = False
        return extintos