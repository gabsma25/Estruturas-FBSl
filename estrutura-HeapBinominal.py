import time
import matplotlib.pyplot as plt

# Classe para a estrutura Heap Binomial
class BinomialHeap:
    class Node:
        def __init__(self, key):
            self.key = key
            self.degree = 0
            self.child = None
            self.sibling = None

    def __init__(self):
        self.head = None

    def merge(self, other):
        # Método para mesclar duas heaps binomiais
        if not self.head:
            self.head = other.head
            return
        if not other.head:
            return
        # Iniciando a fusão
        new_head = None
        current1, current2 = self.head, other.head
        prev = None
        while current1 and current2:
            if current1.degree < current2.degree:
                if prev:
                    prev.sibling = current1
                else:
                    new_head = current1
                prev = current1
                current1 = current1.sibling
            elif current1.degree > current2.degree:
                if prev:
                    prev.sibling = current2
                else:
                    new_head = current2
                prev = current2
                current2 = current2.sibling
            else:
                if current1.key < current2.key:
                    if prev:
                        prev.sibling = current1
                    else:
                        new_head = current1
                    prev = current1
                    current1 = current1.sibling
                else:
                    if prev:
                        prev.sibling = current2
                    else:
                        new_head = current2
                    prev = current2
                    current2 = current2.sibling
        if current1:
            prev.sibling = current1
        if current2:
            prev.sibling = current2
        self.head = new_head

    def insert(self, key):
        new_heap = BinomialHeap()
        new_node = BinomialHeap.Node(key)
        new_heap.head = new_node
        self.merge(new_heap)

    def minimum(self):
        # Retorna o mínimo valor na heap
        if not self.head:
            return None
        min_node = self.head
        current = self.head.sibling
        while current:
            if current.key < min_node.key:
                min_node = current
            current = current.sibling
        return min_node.key

    def extract_min(self):
        if not self.head:
            return None
        # Encontrar o nó com a chave mínima
        min_node = self.head
        prev_min = None
        current = self.head.sibling
        prev = self.head
        while current:
            if current.key < min_node.key:
                min_node = current
                prev_min = prev
            prev = current
            current = current.sibling
        if prev_min:
            prev_min.sibling = min_node.sibling
        else:
            self.head = min_node.sibling
        # Criar uma nova heap com os filhos do nó mínimo
        new_heap = BinomialHeap()
        child = min_node.child
        while child:
            next_child = child.sibling
            child.sibling = new_heap.head
            new_heap.head = child
            child = next_child
        self.merge(new_heap)
        return min_node.key

# Função para ler o dataset
def read_dataset(file_name):
    with open(file_name, 'r') as f:
        return list(map(int, f.readlines()))

# Função para avaliar o desempenho
def evaluate_performance(heap, dataset):
    # Avaliando inserção
    start_time = time.time()
    for num in dataset:
        heap.insert(num)
    insertion_time = time.time() - start_time

    # Avaliando busca do mínimo
    start_time = time.time()
    min_val = heap.minimum()
    minimum_time = time.time() - start_time

    # Avaliando remoção do mínimo
    start_time = time.time()
    for _ in range(len(dataset)):
        heap.extract_min()
    extraction_time = time.time() - start_time

    return insertion_time, minimum_time, extraction_time

# Função para calcular os tempos normalizados
def normalize_times(insertion_time, minimum_time, extraction_time):
    total_time = insertion_time + minimum_time + extraction_time
    normalized_insertion = insertion_time / total_time
    normalized_minimum = minimum_time / total_time
    normalized_extraction = extraction_time / total_time
    return normalized_insertion, normalized_minimum, normalized_extraction

# Função para plotar o desempenho
def plot_performance(insertion_time, minimum_time, extraction_time):
    labels = ['Insertion', 'Minimum', 'Extraction']
    times = [insertion_time, minimum_time, extraction_time]

    plt.figure(figsize=(10, 5))
    plt.bar(labels, times, color=['blue', 'green', 'red'])
    plt.xlabel('Operations')
    plt.ylabel('Time (seconds)')
    plt.title('Binomial Heap Performance')
    plt.show()

# Função para plotar o desempenho normalizado
def plot_normalized_performance(normalized_insertion, normalized_minimum, normalized_extraction):
    labels = ['Insertion', 'Minimum', 'Extraction']
    times = [normalized_insertion, normalized_minimum, normalized_extraction]

    plt.figure(figsize=(10, 5))
    plt.bar(labels, times, color=['blue', 'green', 'red'])
    plt.xlabel('Operations')
    plt.ylabel('Normalized Time')
    plt.title('Normalized Binomial Heap Performance')
    plt.show()

# Main
if __name__ == "__main__":
    # Leitura do dataset
    dataset = read_dataset("dataset_100000_numbers.txt")

    # Criando a heap binomial
    binomial_heap = BinomialHeap()

    # Avaliando o desempenho
    insertion_time, minimum_time, extraction_time = evaluate_performance(binomial_heap, dataset)

    # Exibindo o desempenho
    print(f"Insertion Time: {insertion_time:.4f} seconds")
    print(f"Minimum Search Time: {minimum_time:.4f} seconds")
    print(f"Extraction Time: {extraction_time:.4f} seconds")

    # Calculando os tempos normalizados
    normalized_insertion, normalized_minimum, normalized_extraction = normalize_times(insertion_time, minimum_time, extraction_time)

    # Plotando o gráfico de desempenho
    plot_performance(insertion_time, minimum_time, extraction_time)

    # Plotando o gráfico de desempenho normalizado
    plot_normalized_performance(normalized_insertion, normalized_minimum, normalized_extraction)
