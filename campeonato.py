from equipe import Equipe, pegarEquipes
from random import shuffle, randint, random
from copy import deepcopy
from turno import Turno

class Campeonato:

    def __init__(self, turnos = [], menor_torcida_maiores = 0):
        self.turnos = turnos
        self.menor_torcida_maiores = menor_torcida_maiores

    def fitness(self):
        punicao = 0

        todas_partidas = []
        for turno in self.turnos:
            punicao += turno.fitness()
            todas_partidas.extend(turno.partidas)

        dict_partidas = {}

        for partida in todas_partidas:
            partida_tuple = (partida[0].nome, partida[1].nome)

            if partida_tuple in dict_partidas:
                punicao -= 1
            else:
                dict_partidas[partida_tuple] = 1

        return punicao
    
    def gerar(self, equipes):
        self.menor_torcida_maiores = sorted(equipes, key=lambda equipe: equipe.torcida, reverse=True)[1].torcida
        self.turnos = self.gerarTurnos(equipes)

    def gerarPartidas(self, equipes):
        partidas = []
        for i, equipe1 in enumerate(equipes):
            for j, equipe2 in enumerate(equipes):
                if i != j:
                    partidas.append([equipe1, equipe2])

        return partidas
    
    def gerarTurnos(self, equipes):
        partidas = self.gerarPartidas(equipes)

        shuffle(partidas)

        return [Turno(partidas[x:x+len(equipes)//2], equipes, self.menor_torcida_maiores) for x in range(0, len(partidas), len(equipes)//2)]

    
    def mutacao(self, taxa):
        novos_turnos = [turno.mutacao(taxa) for turno in self.turnos]
        return Campeonato(novos_turnos, self.menor_torcida_maiores)
    
    def crossover(self, taxa):
        novosTurnos = deepcopy(self.turnos)

        num1 = randint(0, len(self.turnos) - 1)
        num2 = randint(0, len(self.turnos) - 1)

        turno1 = novosTurnos[num1]
        turno2 = novosTurnos[num2]

        for i in range(len(turno1.partidas) - 1):
            for j in range(i, len(turno2.partidas)):
                if taxa < random():
                    turno1.partidas[i], turno2.partidas[j] = turno2.partidas[j], turno1.partidas[i]
                    turno1._fitness = float("-inf")
                    turno2._fitness = float("-inf")
        
        return Campeonato(novosTurnos, self.menor_torcida_maiores)

    
    def __str__(self):
        retorno = ""

        for i, turno in enumerate(self.turnos):
            retorno += f"Turno {i}:\n{turno}\n"

        return retorno
        
if __name__ == "__main__":
    num_populacao = 4
    equipes = pegarEquipes()
    campeonatos = [Campeonato() for _ in range(num_populacao + 1)]

    for campeonato in campeonatos:
        campeonato.gerar(equipes)

    geracoes = 0
    while(campeonatos[0].fitness() != 0):
        mutacoes = [campeonato.mutacao(0.2) for campeonato in campeonatos]

        crossovers = [campeonato.crossover(0.3) for campeonato in mutacoes]       

        todos_campeonatos = campeonatos + mutacoes + crossovers

        campeonatos = sorted(todos_campeonatos, key=lambda campeonato: campeonato.fitness(), reverse=True)[:num_populacao]
        geracoes += 1
        
        if (geracoes % 1000 == 0):
            print(f"Melhor fitness: {campeonatos[0].fitness()}")

    print(f"Campeonato:\n{campeonatos[0]}")
