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
        self.populacao = [Campeonato(self.equipes) for _ in range(self.num_populacao)]
        self.populacao = sorted(self.populacao, key=lambda campeonato: campeonato.fitness(), reverse=True)

    def iniciar(self):
        geracoes = 0

        """ print(f"Campeonato:\n{self.populacao[0]}")
        print(f"Fitness:\n{self.populacao[0].fitness()}")
        return """

        maior_fitness = self.populacao[0].fitness()
        contador_desastre = 0
        while(self.populacao[0].fitness() != 0):
            
            populacao_crossover = self.crossover(self.populacao)

            mutacoes = [campeonato.mutacao(self.taxa_mutacao) for campeonato in populacao_crossover]

            self.populacao = self.selecao(self.populacao + mutacoes)

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

            #if geracoes % 1000 == 0:
                #print(f"Melhor fitness {geracoes}: {self.populacao[0].fitness()}")

            """ if geracoes % 10000 == 0:
                break """
                

        print(f"Campeonato:\n{self.populacao[0]}")
        print(f"Quantidade de gerações: {geracoes}")

    def selecao(self, populacao_total):
        nova_populacao = list(populacao_total)

        nova_populacao = sorted(populacao_total, key=lambda campeonato: campeonato.fitness(), reverse=True)[:self.num_populacao]

        return nova_populacao



    def desastre(self):
        for campeonato in self.populacao[1:]:
            campeonato.gerar()   

    def crossover(self, populacao):
        melhor_individuo = populacao[0]

        nova_populacao = []
        for i in range(1, len(populacao)):
            campeonato2 = populacao[i]
            novos_turnos = list(melhor_individuo.turnos)
            for j in range(len(campeonato2.turnos)):
                if self.taxa_crossover > random():
                    if random() > 0.5:
                        novos_turnos[j] = melhor_individuo.turnos[j]
                    else:
                        novos_turnos[j] = campeonato2.turnos[j]
            nova_populacao.append(Campeonato(self.equipes, novos_turnos))
        
        return nova_populacao
        

if __name__ == "__main__":
    algoritmo = AlgoritmoGenetico(50, 0.1, 0.9)

    algoritmo.iniciar()
