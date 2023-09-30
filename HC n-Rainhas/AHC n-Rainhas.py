import random
import time
from matplotlib import patches, pyplot as plt
import numpy as np

historico_conflitos = []

def contagem_conflitos(estado_tabuleiro):
    conflitos = 0
    for i in range(len(estado_tabuleiro)):
        for j in range(i + 1, len(estado_tabuleiro)):
            if estado_tabuleiro[i] == estado_tabuleiro[j] or abs(estado_tabuleiro[i] - estado_tabuleiro[j]) == j - i:
                conflitos += 1
    return conflitos

def cria_estado_inicial(N):
    return [random.randint(0, N - 1) for _ in range(N)]

def hill_climbing_n_rainhas(N, max_iteracoes):
    global historico_conflitos
    tempo_inicio = time.time()
    estado_atual = cria_estado_inicial(N)
    melhor_conflito = contagem_conflitos(estado_atual)
    historico_conflitos.append(melhor_conflito)
    total_movimentos = 0
    
    while melhor_conflito > 0 and total_movimentos < max_iteracoes:
        melhor_vizinho = None
        
        for coluna in range(N):
            for linha in range(N):
                if estado_atual[coluna] != linha:
                    estado_vizinho = list(estado_atual)
                    estado_vizinho[coluna] = linha
                    vizinho_conflitos = contagem_conflitos(estado_vizinho)
                    
                    if vizinho_conflitos < melhor_conflito:
                        melhor_vizinho = estado_vizinho
                        melhor_conflito = vizinho_conflitos
        
        if melhor_vizinho is not None:
            estado_atual = melhor_vizinho
            historico_conflitos.append(melhor_conflito)
        else:
            # Move to a random state to escape local optima
            coluna_aleatoria = random.randint(0, N - 1)
            random_linha = random.randint(0, N - 1)
            estado_atual[coluna_aleatoria] = random_linha
            melhor_conflito = contagem_conflitos(estado_atual)
            historico_conflitos.append(melhor_conflito)
        
        total_movimentos += 1
    
    tempo_final = time.time()
    return estado_atual, (tempo_final - tempo_inicio), total_movimentos, historico_conflitos

    
    
def mostra_resultados(numero_execucao, conflitos, tempo_decorrido, total_movimentos):
    minutos = int(tempo_decorrido / 60)
    segundos = tempo_decorrido % 60
    print(f'  Conflitos: {conflitos}')
    print(f'  Tempo: {minutos} min {segundos:.2f} seg')
    print(f'  Total de Movimentos: {total_movimentos}')

def plot_historico_conflitos(historico_conflitos):
    plt.plot(historico_conflitos, color='red')
    plt.xlabel('Total de Movimentos')
    plt.ylabel('Numero de conflitos')
    plt.title('Evolução de Conflitos')
    plt.grid(True)
    plt.show()
    
def plot_solucao(solucao, N):
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_xlim((0, N))
    ax.set_ylim((0, N))

    for i in range(N):
        for j in range(N):
            color = 'white' if (i + j) % 2 == 0 else 'black'
            ax.add_patch(patches.Rectangle((j, i), 1, 1, color=color))
    
    contagem = 0
    for rainha in solucao:
        ax.add_patch(patches.Circle((rainha + 0.5, contagem + 0.5), radius=0.4, fill=True, color='red'))
        contagem += 1
    plt.show()

if __name__ == '__main__':
    N = 8 # Número de rainhas
    execucoes = 5
    max_iteracoes = 100  # Limite máximo de movimentos por execução
    qualidade_solucoes = []

    for numero_execucao in range(execucoes):
        print(f'[EXECUÇÃO {numero_execucao + 1}  DE  {execucoes}] PARA N = {N} RAINHAS')
        solucao, tempo_decorrido, total_movimentos, historico_conflitos = hill_climbing_n_rainhas(N, max_iteracoes)
        conflitos = contagem_conflitos(solucao)
        qualidade_solucoes.append(conflitos)
        mostra_resultados(numero_execucao, conflitos, tempo_decorrido, total_movimentos)
        # Plot as solucoes nos tabuleiros
        plot_solucao(solucao, N)

    # Plot the evolution of conflitos during execution
    plot_historico_conflitos(historico_conflitos)



