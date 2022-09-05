# Universidade de Brasília - Departamento de Ciências da Computação
# Teoria e Aplicação de Grafos
# Professor: Dibio Leandro Borges
# Aluno: Eduardo Ferreira Marques Calvacante
# 202006368
# Projeto 2 - ALgoritmo de Emparelhamento Máximo com preferências(Gale-shapley).
# 
# Referencias: https://medium.com/@satyalumesh/gale-shapley-algorithm-for-stable-matching-easyexpalined-17ee51ec0dfa
# https://en.wikipedia.org/wiki/Gale%E2%80%93Shapley_algorithm
# https://github.com/Vishal-Kancharla/Gale-Shapley-Algorithm
# https://github.com/remialban/GaleShapley

from os.path import dirname, join
import re

# Função que lê o arquivo
# para que possa montar o grafo escola/professores/preferencias 

def grafo():

    # o grafo de cada um se dará por meio de dicionários
    grafoProfessor = {}
    grafoEscolas = {}

    current_dir = dirname(__file__) # depedendo da IDe, é necessario desta mudança de diretorio
    file_path = join(current_dir, "./entradaProj2TAG.txt") 
    file = open(file_path, 'r') # inicializa arquivo com as conexões(deve estar no mesmo diretorio)

    # criação do grafo dos professores
    # prof = professor individual
    for line in file:
        if line.startswith('(P'):
            prof = re.sub('\D', ',', line).split(',')
            prof = [int(x) for x in  filter(None, prof)]
            grafoProfessor[prof[0]] = {'id': prof[0], 'hab': prof[1], 'prefere': prof[2:], 'escolhido': -1, 'free': True}
# id = id do professo ex: P5 | hab: habilistações do prof | escolhido: escola alocada | free: i want to break free!
        
        if line.startswith('(E'):
            escola = re.sub('\D', ',', line).split(',')
            escola = [int(x) for x in  filter(None, escola)]
            
            vagas = [int(i) for i in range(1, len(escola))]
            if len(vagas) < 2:
                vagas.append(-1)
            grafoEscolas[escola[0]] = {'id': escola[0], 'habPref': vagas, 'vagasPrenchidas': [False, False],
                                       'profs': [-1, -1]}
# id = id da escola ex: E5 | habPref: habilitações preferidas | vagasPrenchidas: vgas preenchidas pelos professores | pos: possibilidade para o maxímo
    
    file.close() # fechar o arquivo para que meu PC não exploda
    return grafoProfessor, grafoEscolas


### alocamento
def pair(idP, grafoP, grafoE):
    
    for i in (grafoP[idP]['prefere']):
        idE = i #id da escola
        prof = grafoP[idP] # professor a ser alocado
        sch = grafoE[idE] # escola
        cond = sch['habPref'][1] # variavel de auxilio caso as vagas não sejam 2
        if (prof['free']) and (prof['hab'] >= sch['habPref'][0]) or ((prof['hab'] >= sch['habPref'][1]) and (cond != -1)):
            
            if (sch['vagasPrenchidas'][0] == False) and (prof['hab'] >= sch['habPref'][0]):
                
                prof['free'] = False # professor alocado
                prof['escolhido'] = sch['id']
                
                sch['vagasPrenchidas'][0] = True
                sch['profs'][0] = prof['id']
                
                return True

            if (sch['vagasPrenchidas'][1] == False) and ((prof['hab'] >= sch['habPref'][1]) and (cond != -1)):
                
                prof['free'] = False # professor alocado
                prof['escolhido'] = sch['id']
                
                sch['vagasPrenchidas'][1] = True
                sch['profs'][1] = prof['id']
                
                return True
    # caso o professor não possa ser alocado(vagas preenchidas) então teremos que fazer a substituição
    # de professores com habilitações maiores que as necessárias para as escolas
    return False


# Caso o professor não seja alocado, precisamos substituir, para alcançar o máximo
def failedPair(idP, grafoP, grafoE):
    
    for i in (grafoP[idP]['prefere']):
        prof = grafoP[idP] # professor a ser alocado
        sch = grafoE[i] # escola
        cond = sch['habPref'][1] # variavel de auxilio caso as vagas não sejam 2
        
        if (prof['hab'] >= sch['habPref'][0]) or ((prof['hab'] >= sch['habPref'][1]) and (cond != -1)):
            if(prof['hab'] >= sch['habPref'][0]) and (sch['profs'][0] != prof['id']) and (cond != prof['id']):
                
                prof['free'] = False
                prof['escolhido'] = sch['id']
                sch['vagasPrenchidas'][0] = True
                
                profAnterior = sch['profs'][0]
                grafoP[profAnterior]['free'] = True
                sch['profs'][0] = prof['id'] # Professor substituido
                
                return 

            if (prof['hab'] >= sch['habPref'][1] and (sch['habPref'][1] != -1)) and (sch['profs'][0] != prof['id']) and (cond != prof['id']):
                
                prof['free'] = False
                prof['escolhido'] = sch['id']
                sch['vagasPrenchidas'][1] = True
                
                antigo = sch['profs'][1]
                grafoP[profAnterior]['free'] = True
                sch['profs'][1] = prof['id'] # Professor substituido
                
                return 
    return

##### algoritmo de pareamento máximo(caso tantas repetições) estável, baseado na referencias principal
def galeShapley(grafoP, grafoE):
    
    profsLivres = []
    for i in grafoP.keys():
        if grafoP[i]['free'] == True:
            profsLivres.append(i)
    
    #iniciamos uma fila. o Professoe é alocado para cada escola, logo o pareamento é envesiado para os professores
    while len(profsLivres) != 0:
        prof = profsLivres[0] #id prof
        profsLivres.pop(0) # joga 'fora' o professor que será alocado 
        
        if profsLivres:
            if (pair(prof, grafoP, grafoE) == False): # caso o professor não possa ser alocado
                
                failedPair(prof, grafoP, grafoE)

def printGale(grafoP, grafoE):
    
    contaAlocados = 0
    for i in grafoE:
        sch = grafoE[i]['profs']
        
        # contagem dos professores alocados
        if sch[0] != -1:
            contaAlocados += 1
        if sch[1] != -1:
            contaAlocados += 1
        
        
        print(f"Escola {i} alocado com os professores: {sch}")

    print(f'Máximo de professores alocados: {contaAlocados}')
        

### "main"

grafoP, grafoE = grafo()
# o algoritmo de gale-shapley pode ser utilizado para alcançar o maximo, fazendo-se váris iterações
for i in range(50):
    galeShapley(grafoP, grafoE)

print("Emparalhamento estável Máximo (-1 significa que nao houve professor alocado) \n")
printGale(grafoP, grafoE)















