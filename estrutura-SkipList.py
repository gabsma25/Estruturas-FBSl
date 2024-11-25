import random
import time
import matplotlib.pyplot as plt
import numpy as np
'''aprovado'''
# Configurações da Skip List
MAX_LEVEL = 6  # Máximo de níveis da Skip List
P = 0.5        # Probabilidade para elevar um nó

class Node:
    def __init__(self, key, level):
        self.key = key
        self.forward = [None] * (level + 1)  # Lista para manter os ponteiros para os próximos nós em cada nível

class SkipList:
    def __init__(self):
        self.level = 0  # Começa com nível 0
        self.header = Node(float('-inf'), MAX_LEVEL)  # Cabeçalho com chave infinita

    def random_level(self):
        level = 0
        while random.random() < P and level < MAX_LEVEL:
            level += 1
        return level

    def insert(self, key):
        update = [None] * (MAX_LEVEL + 1)  # Lista para manter os nós de atualização
        current = self.header

        # Localizando onde o nó deve ser inserido
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        # Verifica se o nó já existe
        current = current.forward[0]
        if not current or current.key != key:
            new_level = self.random_level()

            # Atualiza o nível da SkipList se necessário
            if new_level > self.level:
                for i in range(self.level + 1, new_level + 1):
                    update[i] = self.header
                self.level = new_level

            # Criação do novo nó
            new_node = Node(key, new_level)
            for i in range(new_level + 1):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node

    def delete(self, key):
        update = [None] * (MAX_LEVEL + 1)
        current = self.header

        # Localizando o nó a ser excluído
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current and current.key == key:
            # Atualiza os ponteiros para excluir o nó
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]

            # Ajusta o nível da SkipList
            while self.level > 0 and not self.header.forward[self.level]:
                self.level -= 1

    def find_min(self):
        # Retorna o menor valor (primeiro elemento após o cabeçalho)
        return self.header.forward[0].key if self.header.forward[0] else None

# Função para ler o dataset do arquivo
def read_dataset(file_name):
    with open(file_name, 'r') as file:
        return [int(line.strip()) for line in file]

# Função para executar os testes de benchmark
def benchmark_skiplist(skiplist, dataset):
    times = {"insertion": 0, "find_min": 0, "deletion": 0}

    # Teste de inserção
    start = time.time()
    for num in dataset:
        skiplist.insert(num)
    times["insertion"] = time.time() - start

    # Teste de busca do menor elemento
    start = time.time()
    min_value = skiplist.find_min()
    times["find_min"] = time.time() - start

    # Teste de exclusão de todos os elementos
    start = time.time()
    for num in dataset:
        skiplist.delete(num)
    times["deletion"] = time.time() - start

    return times, min_value

# Função para normalizar os tempos
def normalize_times(times):
    max_time = max(times.values())
    return {k: v / max_time for k, v in times.items()}

# Função para plotar o gráfico de desempenho
def plot_performance(times, normalized_times):
    labels = list(times.keys())
    absolute = list(times.values())
    normalized = list(normalized_times.values())

    x = np.arange(len(labels))

    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax1.bar(x - 0.2, absolute, 0.4, label='Absolute Time (s)', color='b')
    ax1.set_ylabel('Time (seconds)')
    ax1.set_title('Skip List Performance')
    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()
    ax2.bar(x + 0.2, normalized, 0.4, label='Normalized Time', color='orange')
    ax2.set_ylabel('Normalized Time')
    ax2.legend(loc='upper right')

    plt.xticks(x, labels)
    plt.show()

# Função principal
def main():
    # Carregar dataset
    dataset = read_dataset("dataset_100000_numbers.txt")

    skiplist = SkipList()

    # Executar benchmark
    times, min_value = benchmark_skiplist(skiplist, dataset)

    # Normalizar tempos
    normalized_times = normalize_times(times)

    # Exibir resultados
    print("Tempo absoluto (em segundos):")
    for op, time in times.items():
        print(f"  {op}: {time:.6f} segundos")
    print(f"Menor valor encontrado: {min_value}")

    print("\nTempos normalizados:")
    for op, time in normalized_times.items():
        print(f"  {op}: {time:.6f}")

    # Gerar gráfico de desempenho
    plot_performance(times, normalized_times)

if __name__ == "__main__":
    main()
