from google.colab import files
uploaded = files.upload()

"""
Trabalho de Big Data - Comparacao de Algoritmos de Busca
Busca Sequencial | Busca Jump | Busca Binaria
Codigo simples para rodar no Google Colab
"""

import math
import time
import timeit
import tracemalloc
import numpy as np

# ------------------------------------------------------------------
# 1. BUSCA SEQUENCIAL - O(n)
# ------------------------------------------------------------------
def busca_sequencial(arr, alvo):
    num_comp = 0
    for i in range(len(arr)):
        num_comp += 1
        if arr[i] == alvo:
            return i, num_comp
    return -1, num_comp


# ------------------------------------------------------------------
# 2. BUSCA JUMP (Salto) - O(sqrt(n)) -- exige lista ORDENADA
# ------------------------------------------------------------------
def busca_jump(arr, alvo):
    n = len(arr)
    passo = int(math.sqrt(n))
    num_comp = 0

    inicio = 0
    fim = passo
    # Encontra o bloco onde o alvo pode estar
    while fim < n and arr[min(fim, n) - 1] < alvo:
        num_comp += 1
        inicio = fim
        fim += passo
    fim = min(fim, n)

    # Busca sequencial dentro do bloco
    for i in range(inicio, fim):
        num_comp += 1
        if arr[i] == alvo:
            return i, num_comp

    return -1, num_comp


# ------------------------------------------------------------------
# 3. BUSCA BINARIA - O(log n) -- exige lista ORDENADA
# ------------------------------------------------------------------
def busca_binaria(arr, alvo):
    baixo, alto = 0, len(arr) - 1
    num_comp = 0

    while baixo <= alto:
        num_comp += 1
        meio = (baixo + alto) // 2
        if arr[meio] == alvo:
            return meio, num_comp
        elif arr[meio] < alvo:
            baixo = meio + 1
        else:
            alto = meio - 1

    return -1, num_comp


# ------------------------------------------------------------------
# FUNCAO AUXILIAR: roda um algoritmo medindo tempo, comparacoes e memoria
# ------------------------------------------------------------------
def rodar_teste(nome_algoritmo, funcao_busca, arr, alvo):
    print("-" * 50)
    print(f"Metodo: {nome_algoritmo}")

    tracemalloc.start()

    # timeit mede so a funcao de busca (varias repeticoes p/ precisao)
    tempo = timeit.timeit(lambda: funcao_busca(arr, alvo), number=1)

    # roda uma vez "de verdade" para pegar indice e num_comp
    indice, num_comp = funcao_busca(arr, alvo)

    memoria_atual, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Total de elementos (N): {len(arr)}")
    print(f"Indice Encontrado: {indice} (-1 significa que nao existe)")
    print(f"Tempo de execucao: {tempo:.6f}s | Comparacoes realizadas: {num_comp}")
    print(f"Memoria usada (pico): {memoria_pico / 1024:.2f} KB")

    return {
        "algoritmo": nome_algoritmo,
        "N": len(arr),
        "tempo": tempo,
        "comparacoes": num_comp,
        "memoria_kb": memoria_pico / 1024,
        "indice": indice,
    }


# ------------------------------------------------------------------
# LEITURA DOS CASOS DE TESTE (arquivos N.txt dentro do zip)
# ------------------------------------------------------------------
import os
import glob
import zipfile

PASTA_ZIP = "/content/Casos_de_Teste.zip"   # suba o zip para o Colab com este nome
PASTA_EXTRAIDA = "/content/Casos_de_Teste"

def preparar_arquivos():
    # Extrai o zip (so na primeira vez)
    if not os.path.exists(PASTA_EXTRAIDA):
        with zipfile.ZipFile(PASTA_ZIP, "r") as z:
            z.extractall("/content")

    # Procura a pasta "Construir" dentro do zip, onde estao os N.txt
    caminhos = glob.glob(f"{PASTA_EXTRAIDA}/**/*.txt", recursive=True)
    return sorted(caminhos, key=lambda p: int(os.path.basename(p).replace(".txt", "")))


def ler_array(caminho):
    with open(caminho) as f:
        numeros = f.read().split()
    return np.array([int(x) for x in numeros])


# ------------------------------------------------------------------
# EXECUCAO PARA TODOS OS CASOS DE TESTE
# ------------------------------------------------------------------
if __name__ == "__main__":

    arquivos = preparar_arquivos()
    print(f"Encontrados {len(arquivos)} casos de teste.\n")

    resultados = []

    for caminho in arquivos:
        arr = ler_array(caminho)
        N = len(arr)

        # Alvo de teste: pega um numero que existe no array (ex: o do meio)
        arr_ordenado = np.sort(arr)
        alvo = arr_ordenado[N // 2]

        print("=" * 60)
        print(f"Arquivo: {os.path.basename(caminho)} | N = {N} | Alvo = {alvo}")

        resultados.append(rodar_teste("Busca Sequencial", busca_sequencial, arr, alvo))
        resultados.append(rodar_teste("Busca Jump", busca_jump, arr_ordenado, alvo))
        resultados.append(rodar_teste("Busca Binaria", busca_binaria, arr_ordenado, alvo))

    print("\n" + "=" * 60)
    print("RESUMO GERAL")
    print("=" * 60)
    for r in resultados:
        print(r)

    # ---- Opcional: transformar em tabela para exportar/plotar ----
    import pandas as pd
    df = pd.DataFrame(resultados)
    print("\nTabela final:")
    print(df)
    # df.to_csv("resultados.csv", index=False)  # descomente para salvar
