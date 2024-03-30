from random import randint, random
from copy import deepcopy

class Turno:
    def __init__(self, partidas, equipes, menor_torcida_classico):
        self.partidas = partidas
        self.equipes = equipes
        self._fitness = float("-inf")
        self.menor_torcida_classico = menor_torcida_classico
    
    def mutacao(self, taxa):
        novas_partidas = deepcopy(self.partidas)
        
        for i in range(len(self.partidas) - 1):
            partida = novas_partidas[i]
            if taxa < random():
                if random() > 0.4:
                    num1 = randint(0, 1)
                    num2 = randint(0, len(self.equipes) - 1)
                    partida[num1] = self.equipes[num2]
                else:
                    partida[0], partida[1] = partida[1], partida[0]

        return Turno(novas_partidas, self.equipes, self.menor_torcida_classico)
    
    def fitness(self):
        penalizacao = 0
        
        # para penalizar equipes com muitas ou nenhuma partida
        partidas_equipes = {}

        for equipe in self.equipes:
            partidas_equipes[equipe.nome] = 0

        # penalizar partidas da mesma cidade
        cidades = {}

        # penalizar mais de uma partida classica
        classicos = 0

        for i in range(len(self.partidas)):
            partida = self.partidas[i]

            if self.partida_unico_time(partida):
                penalizacao -= 1

            if self.classico(partida):
                classicos += 1

            if partida[0].cidade in cidades:
                cidades[partida[0].cidade] += 1
            else:
                cidades[partida[0].cidade] = 1
            
            for equipe in partida:
                partidas_equipes[equipe.nome] += 1
    
        for contagem in partidas_equipes.values():
            penalizacao -= contagem - 1 if contagem > 1 else 0
            penalizacao -= 1 if contagem == 0 else 0

        for contagem in cidades.values():
            penalizacao -= contagem - 1 if contagem > 1 else 0

        if classicos > 1:
            penalizacao -= classicos - 1

        self._fitness = penalizacao
        return penalizacao

    
    def partida_unico_time(self, partida):
        return partida[0] == partida[1]

    def partidas_mesmo_time(self, partida1, partida2):
        return (partida1[0] == partida2[0] or partida1[0] == partida2[1] or
            partida1[1] == partida2[0] or partida1[1] == partida2[1])
    
    def partida_igual(self, partida1, partida2):
        return partida1[0] == partida2[0] and partida1[1] == partida2[1]
    
    def partidas_mesma_cidade(self, partida1, partida2):
        return partida1[0].cidade == partida2[0].cidade
    
    def classico(self, partida):
        return partida[0].torcida >= self.menor_torcida_classico and partida[1].torcida >= self.menor_torcida_classico

    def __str__(self):
        retorno = ""
        for partida in self.partidas:
            retorno += f"{partida[0].nome} vs {partida[1].nome} - ({partida[0].cidade})"

            if self.classico(partida):
                retorno += f" Classico"
            retorno += "\n"
        
        retorno += f"Fitness: {self.fitness()}\n"
        return retorno