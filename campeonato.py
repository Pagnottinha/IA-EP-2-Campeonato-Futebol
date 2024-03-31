from equipe import Equipe, pegarEquipes
from random import shuffle, randint, random

class Campeonato:

    def __init__(self, equipes, turnos = []):
        self.equipes = equipes
        self.torcida_classico = equipes[2].torcida

        if len(turnos) == 0:
            self.gerar()
        else:
            self.turnos = turnos

    def fitness(self):
        punicao = 0
       
        dict_partidas = {}
        for partida in range(0, len(self.turnos), 2):
            partida_tuple = (self.turnos[partida], self.turnos[partida+1])
            if partida_tuple in dict_partidas:
                punicao -= 1
            else:
                dict_partidas[partida_tuple] = 1

        for turno in range(0, len(self.turnos), len(self.equipes)):
            punicao += self._fitness_turno(self.turnos[turno:turno+len(self.equipes)])

        return punicao
    
    def _fitness_turno(self, turno):
        penalizacao = 0
        
        # para penalizar equipes com muitas ou nenhuma partida
        partidas_equipes = {}

        for equipe in self.equipes:
            partidas_equipes[equipe.id] = 0

        # penalizar partidas da mesma cidade
        cidades = {}

        # penalizar mais de uma partida classica
        classicos = 0

        for i in range(0, len(turno), 2):
            id_equipe1 = turno[i]
            id_equipe2 = turno[i+1]
            if id_equipe1 == id_equipe2:
                penalizacao -= 1

            if self.classico(turno[i:i+2]):
                classicos += 1

            equipe1 = self.equipes[id_equipe1 - 1]
            if equipe1.cidade in cidades:
                cidades[equipe1.cidade] += 1
            else:
                cidades[equipe1.cidade] = 1
            
            partidas_equipes[id_equipe1] += 1
            partidas_equipes[id_equipe2] += 1
    
        for contagem in partidas_equipes.values():
            penalizacao -= contagem - 1 if contagem > 1 else 0
            penalizacao -= 1 if contagem == 0 else 0

        for contagem in cidades.values():
            penalizacao -= contagem - 1 if contagem > 1 else 0

        if classicos > 1:
            penalizacao -= classicos - 1

        return penalizacao

    def classico(self, partida):
        equipe1 = self.equipes[partida[0] - 1]
        equipe2 = self.equipes[partida[1] - 1]

        return equipe1.torcida >= self.torcida_classico and equipe2.torcida >= self.torcida_classico
    
    def gerar(self):
        turnos = self.gerarTurnos()
        self.turnos = turnos

    def gerarPartidas(self):
        partidas = []
        for equipe1 in self.equipes:
            for equipe2 in self.equipes:
                if equipe1.id != equipe2.id:
                    partidas.extend([equipe1.id, equipe2.id])

        return partidas
    
    def gerarTurnos(self):
        partidas = self.gerarPartidas()

        shuffle(partidas)

        return partidas

    def time_aleatorio(self):
        num = randint(0, len(self.equipes) - 1)
        return self.equipes[num]

    def mutacao(self, taxa):
        novos_turnos = list(self.turnos)

        for i in range(0, len(novos_turnos)):
            if random() > taxa:
                equipe = self.time_aleatorio()
                novos_turnos[i] = equipe.id

        return Campeonato(self.equipes, novos_turnos)
    
    """ def crossover(self, taxa):
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
        
        return Campeonato(novosTurnos, self.menor_torcida_maiores) """

    def print_turno(self, turno):
        texto_turno = ""
        
        for i in range(0, len(turno), 2):
            equipe1 = self.equipes[turno[i] - 1]
            equipe2 = self.equipes[turno[i+1] - 1]

            texto_turno += f"{equipe1.nome} x {equipe2.nome} ({equipe1.cidade})"
            
            if self.classico(turno[i:i+2]):
                texto_turno += " - Classico"

            texto_turno += "\n"

        return texto_turno
    
    def __str__(self):
        retorno = ""

        for i in range(0, len(self.turnos), len(self.equipes)):
            retorno += f"Turno {i // len(self.equipes) + 1}:\n"
            retorno += self.print_turno(self.turnos[i:i+len(self.equipes)])
            retorno += "\n"

        return retorno
        
if __name__ == "__main__":
    campeonato = Campeonato(pegarEquipes())
    print(campeonato)
    print(campeonato.mutacao(0.5))
