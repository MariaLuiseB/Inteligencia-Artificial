import math
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import randint, random


historico_conflitos = []

def contagem_conflitos(estado_tabuleiro):
    conflitos = 0
    for i in range(len(estado_tabuleiro)):
        for j in range(i + 1, len(estado_tabuleiro)):
            if estado_tabuleiro[i] == estado_tabuleiro[j] or abs(estado_tabuleiro[i] - estado_tabuleiro[j]) == j - i:
                conflitos += 1
    return conflitos

def configura_aleatorio(N):
    return [randint(0, N - 1) for _ in range(N)]


def simulated_annealing(N, max_iteracoes):
    tempo_inicio = time.time()

    global historico_conflitos
    total_movimentos = 0
    estado_atual = configura_aleatorio(N)
    qtd_conflitos_atual = contagem_conflitos(estado_atual)

    melhor_estado = estado_atual.copy()
    melhor_qtd_confiltos = qtd_conflitos_atual

    T = 1.0
    T_min = 0.0001
    alpha = 0.95

    while T > T_min:
        for i in range(max_iteracoes): # 1000 é o numero de iteracoes para cada temperatura
            novo_estado = estado_atual.copy() 
            i = randint(0, N - 1) 
            novo_estado[i] = randint(0, N - 1)

            # Calcula a temperatura do novo estado
            nova_qtd_conflitos = contagem_conflitos(novo_estado)
            # Calcula a diferenca entre a temperatura atual e a nova temperatura 
            delta_t = nova_qtd_conflitos - qtd_conflitos_atual

           
            if delta_t < 0 or random() < math.exp(-delta_t / T):
                estado_atual = novo_estado # Atualiza o estado atual
                qtd_conflitos_atual = nova_qtd_conflitos # Atualiza a temperatura atual
                total_movimentos += 1

                if qtd_conflitos_atual < melhor_qtd_confiltos:
                    melhor_estado = estado_atual.copy()
                    melhor_qtd_confiltos = qtd_conflitos_atual
                    # Atualiza o histórico de conflitos
                    historico_conflitos.append(qtd_conflitos_atual)
               
                
        T *= alpha

    tempo_final = time.time()
    
    return melhor_estado, (tempo_final - tempo_inicio), T, total_movimentos

def plot_solucao(solucao, N):
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal') # parametro 111 é para criar um subplot de 1 linha, 1 coluna e o terceiro parametro é o indice do subplot
    ax.set_xlim((0, N)) # define o limite do eixo x
    ax.set_ylim((0, N)) # define o limite do eixo y

   # Plotando as rainhas de vermelho no tabuleiro de xadrez
    for row, col in enumerate(solucao): 
        ax.add_patch(patches.Circle((col + 0.5, row + 0.5), 0.4, color='red'))

    # Adicionando as linhas pretas do tabuleiro de xadrez
    for i in range(N + 1):
        ax.axhline(i, color='black', linewidth=1)
        ax.axvline(i, color='black', linewidth=1)

    ax.set_xticks([]) # remove os ticks do eixo x
    ax.set_yticks([]) # remove os ticks do eixo y
    plt.show()

def mostra_resultados(numero_execucao, conflitos, tempo_decorrido, melhor_temperatura, total_movimentos):
    #print(f' Estado final: {estado_final} \nNumero: {len(estado_final)}')
    minutos = int(tempo_decorrido / 60)
    segundos = int(tempo_decorrido % 60)   # Calcula os segundos completos
    milissegundos = int(tempo_decorrido * 1000)
    print(f'    Tempo: {minutos} min {segundos:.2f} seg e {milissegundos:.2f} ms')
    print(f'    Conflitos: {conflitos}')
    print(f'    Melhor temperatura: {melhor_temperatura:.4f}')
    print(f'    Total de movimentos: {total_movimentos}')
    
    

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
            color = 'white' if (i + j) % 2 == 0 else 'black' # Alterna as cores dos quadrados
            ax.add_patch(patches.Rectangle((j, i), 1, 1, color=color))
    
    contagem = 0
    for rainha in solucao:
        ax.add_patch(patches.Circle((rainha + 0.5, contagem + 0.5), radius=0.4, fill=True, color='red')) # Desenha as rainhas de vermelho
        contagem += 1
    plt.show()



if __name__ == "__main__":
    N = 32
    execucoes = 5
    max_iteracoes = 200  # Limite máximo de movimentos por execução

    for numero_execucao in range(execucoes):
        print(f'[EXECUÇÃO {numero_execucao + 1}  DE  {execucoes}] N RAINHAS = {N}')
        solucao, tempo_decorrido, melhor_temperatura, total_movimentos = simulated_annealing(N, max_iteracoes)
        conflitos = contagem_conflitos(solucao)
        mostra_resultados(numero_execucao, conflitos, tempo_decorrido, melhor_temperatura, total_movimentos)

    # plot_solucao(solucao, N)
    # mostra evolucao dos conflitos
    plot_historico_conflitos(historico_conflitos)

    
        
    
    


