import csv

class Equipe:
    def __init__(self, id, nome, cidade, torcida):
        self.id = id
        self.nome = nome
        self.cidade = cidade
        self.torcida = torcida
    
    def __str__(self):
        return f"{self.nome} - {self.cidade} - {self.torcida}"


def pegarEquipes(path = "./times.csv"):
    file = open(path, mode='r', encoding="UTF-8")
    cvs_reader = csv.reader(file)
    next(cvs_reader)

    equipes = []
    id = 1
    for row in cvs_reader:
        equipes.append(Equipe(id, row[0], row[1], int(row[2])))
        id += 1
        
    file.close()

    equipes.sort(key=lambda equipe: equipe.torcida, reverse=True)
    return equipes

if __name__ == "__main__":
    equipes = pegarEquipes()

    for equipe in equipes:
        print(equipe)