# Universidade de Brasília - Departamento de Ciências da Computação
# Teoria e Aplicação de Grafos
# Professor: Dibio Leandro Borges
# Aluno: Eduardo Ferreira Marques Calvacante
# 202006368
# Projeto 1 - ALgoritmo de Bron-Kerbosch
# 
# Referencias: https://www.w3schools.com/python/ref_func_open.asp
# https://en.wikipedia.org/wiki/Bron–Kerbosch_algorithm
# https://www.youtube.com/watch?v=j_uQChgo72I
# 
# 

# Função que lê o arquivo alterado(retirando desnecessidades)
# para que possa montar o grafo dos golfinhos
from os.path import dirname, join

def grafoGolfinhos():
    
    current_dir = dirname(__file__) # depedendo da IDe, é necessario desta mudança de diretorio
    file_path = join(current_dir, "./soc-dolphins.mtx") 
    file = open(file_path, 'r') # inicializa arquivo com as conexões(deve estar no mesmo diretorio)

    linhaInfo = file.readlines()
    #print(linhaInfo)
    qntGolfinhos, qntArestas = map(int, linhaInfo.pop(0).split()) # quantidade de golfinhos e arestas
    
    listaAdjacencia = [[] for i in range(qntGolfinhos)] # criando lista de adjacencias
    
    for i in range(qntArestas):
        # montagem do grafo nao direcionado
        vertOri, vertDest = map(int, linhaInfo[i].split())
        listaAdjacencia[vertOri -1].append(vertDest)
        listaAdjacencia[vertDest -1].append(vertOri)
        
    file.close()

    return listaAdjacencia, qntArestas, qntGolfinhos

# Conjunto R: vértices que seriam parte do clique(ps. inicia vazio).
# Conjunto P: vértices que têm ligação com todos os vértices de R (candidatos).
# Conjunto X: vértices já analisados e que não levam a uma extensão do conjunto R. Usado
#para evitar comparação excessiva (ps. inicia
#vazio).


########### ALgoritmo-Bosch sem pivotamento(simples)
def bronKerboschSimples(grafo, R,P,X):
    if ((len(P) == 0) and (len(X) == 0)): #reporta R como clique maixmal 

        print("Cliques maximais com " + str(len(R)) + " vértices: ", sorted(list(R)))
        return 

    P_auxiliar = P.copy() # copia auxiliar para que a recursao nao pare tão cedo
    for vertex in P: 
        Raux = R + [vertex] # Uniao (U) R U {v}
        P_auxiliar2 = [item for item in P_auxiliar if item in grafo[vertex-1]] #Intersecção entre P e N(v)
        Xaux = [items for items in X if items in grafo[vertex-1]] # Intersecção entre X e N(v)

        bronKerboschSimples(grafo, Raux, P_auxiliar2, Xaux) # bactraking recursivo

        P_auxiliar.remove(vertex) # P <- P\{v}
        X.append(vertex) # X <- X U {v}

########### Algoritmo com Pivotamento
def bronKerboschPivotamento (grafo, R,P,X):
    if ((len(P) == 0) and (len(X) == 0)): #reporta R como clique maixmal 

        print("Cliques maximais com " + str(len(R)) + " vértices: ", sorted(list(R)))
        return 

    P_auxiliar = P.copy() # copia auxiliar para que a recursao nao pare tão cedo

    grau = -1
    for vertex in P_auxiliar + X:
        qntArestas = len(grafo[vertex - 1])
        if(qntArestas > grau):
            grau = qntArestas
            vMaiorGrau = vertex  # Vértice de maior grau
    
    P = [i for i in P if i not in grafo[vMaiorGrau-1]]  # Lista com os vértices não adjacentes a vMaiorGrau

    for vertex in P: 
        Raux = R + [vertex] # Uniao (U) R U {v}
        P_auxiliar2 = [item for item in P_auxiliar if item in grafo[vertex-1]] #Intersecção entre P e N(v)
        Xaux = [items for items in X if items in grafo[vertex-1]] # Intersecção entre X e N(v)

        bronKerboschPivotamento(grafo, Raux, P_auxiliar2, Xaux) # bactraking recursivo

        P_auxiliar.remove(vertex) # P <- P\{v}
        X.append(vertex) # X <- X U {v}

def coeficienteMedio(grafo, qntGolfinhos):
    # ni(ni-1)/2
    #2ti / ni(ni-1) | ti = trinagulos encontrados 
    # C = 1/N * E ci

    coeficientesLocais = 0 #coeficiente locais

    for vertex in grafo:
        lenGrafo = len(vertex)

        if lenGrafo <= 1: # não é necessario processar os vértices sem vizinho
        
            coe = 0
        else:
            vizinhos = 0

            for i in vertex:

                vizinhos += len([item for item in grafo[i-1] if item in vertex])

            vizinhos /= 2 # divisao por dois já que é contado duas vezes os vizinhos

            coe = (2*vizinhos)/(lenGrafo*(lenGrafo-1)) # trinagulos encontrados 
        
        coeficientesLocais += coe
    
    return coeficientesLocais/qntGolfinhos
    


# "main"
listaAdjacencia, qntArestas, qntGolfinhos = grafoGolfinhos() # criação do grafo, qnt de arestas e de golfinhos
P = [i for i in range(1, qntGolfinhos+1)]
R, X = [], []

#print(listaAdjacencia)
print("Algoritmo sem pivotamento")
bronKerboschSimples(listaAdjacencia, R, P, X) # chamada do algoritmo sem pivotamento
print("")
print("Algoritmo com pivotamento")
bronKerboschPivotamento(listaAdjacencia, R,P,X)
print("")
print("Coeficiente médio de Aglomeração do Grafo: {0:.5}".format(coeficienteMedio(listaAdjacencia, qntGolfinhos)))
