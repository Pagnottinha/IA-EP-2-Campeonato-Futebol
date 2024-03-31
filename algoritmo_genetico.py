from campeonato import Campeonato
from equipe import pegarEquipes
from copy import deepcopy, copy
from random import random

class AlgoritmoGenetico:
    def __init__(self, numero_populacao, taxa_mutacao, taxa_crossover):
        self.num_populacao = numero_populacao
        self.taxa_mutacao = taxa_mutacao
        self.taxa_crossover = taxa_crossover

        self.equipes = pegarEquipes()
        self.populacao = [Campeonato(self.equipes) for _ in range(self.num_populacao + 1)]

        self.populacao = sorted(self.populacao, key=lambda campeonato: campeonato.fitness(), reverse=True)

    def iniciar(self):
        geracoes = 0

        """ print(f"Campeonato:\n{self.populacao[0]}")
        print(f"Fitness:\n{self.populacao[0].fitness()}")
        return """

        maior_fitness = self.populacao[0].fitness()
        contador_desastre = 0
        while(self.populacao[0].fitness() != 0):
            mutacoes = [campeonato.mutacao(self.taxa_mutacao) for campeonato in self.populacao]

            #crossovers = [campeonato.crossover(self.taxa_crossover) for campeonato in self.populacao]       

            todos_campeonatos = self.populacao + mutacoes #+ crossovers

            self.crossover(todos_campeonatos)

            self.populacao = sorted(todos_campeonatos, key=lambda campeonato: campeonato.fitness(), reverse=True)[:self.num_populacao]

            geracoes += 1

            if geracoes % 100 == 0:
                if maior_fitness == self.populacao[0].fitness():
                    contador_desastre += 1
                else:
                    maior_fitness = self.populacao[0].fitness()
                    contador_desastre = 0
            
            if contador_desastre == 3:
                self.desastre()
                contador_desastre = 0

            if geracoes % 1000 == 0:
                print(f"Melhor fitness {geracoes}: {self.populacao[0].fitness()}")

            """ if geracoes % 10000 == 0:
                break """
                

        print(f"Campeonato:\n{self.populacao[0]}")
        print(f"Quantidade de gerações: {geracoes}")

    def selecao(self, populacao_total):
        return NotImplemented()

    def desastre(self):
        for campeonato in self.populacao[1:]:
            campeonato.gerar()   

    def crossover(self, populacao):
        melhor_individuo = populacao[0]

        for i in range(1, len(populacao)):
            campeonato2 = populacao[i]
            novos_turnos = list(melhor_individuo.turnos)
            for j in range(len(campeonato2.turnos)):
                if random() > self.taxa_crossover:
                    if random() > 0.5:
                        novos_turnos[j] = melhor_individuo.turnos[j]
                    else:
                        novos_turnos[j] = campeonato2.turnos[j]
            populacao.append(Campeonato(self.equipes, novos_turnos))
        

        

if __name__ == "__main__":
    algoritmo = AlgoritmoGenetico(15, 0.6, 0.3)

    algoritmo.iniciar()
