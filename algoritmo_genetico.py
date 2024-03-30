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
        self.populacao = [Campeonato() for _ in range(self.num_populacao + 1)]

        for campeonato in self.populacao:
            campeonato.gerar(self.equipes)

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

            if geracoes % 100 == 0 and maior_fitness == self.populacao[0].fitness():
                maior_fitness = self.populacao[0].fitness()
                contador_desastre += 1

            
            if contador_desastre == 3:
                self.desastre()
                contador_desastre = 0

            if geracoes % 1000 == 0:
                print(f"Melhor fitness {geracoes}: {self.populacao[0].fitness()}")

            if geracoes % 10000 == 0:
                break
                

        print(f"Campeonato:\n{self.populacao[0]}")
        print(f"Quantidade de gerações: {geracoes}")

    def selecao(self, populacao_total):
        return NotImplemented()

    def desastre(self):
        for campeonato in self.populacao[1:]:
            campeonato.gerar(self.equipes)   

    def crossover(self, populacao):
        melhor_individuo = populacao[0]

        for i in range(1, len(populacao)):
            campeonato2 = populacao[i]
            novo_campeonato = deepcopy(melhor_individuo)
            for i_turno in range(len(campeonato2.turnos)):
                if self.taxa_crossover < random():
                    turno = novo_campeonato.turnos[i_turno]
                    for i_partida in range(len(turno.partidas)):
                        if random() > 0.5:
                            turno.partidas[i_partida] = novo_campeonato.turnos[i_turno].partidas[i_partida]
                        else:
                            turno.partidas[i_partida] = campeonato2.turnos[i_turno].partidas[i_partida]
            populacao.append(novo_campeonato)
        

        

if __name__ == "__main__":
    algoritmo = AlgoritmoGenetico(10, 0.4, 0.2)

    algoritmo.iniciar()
