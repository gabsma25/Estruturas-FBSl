import time
import matplotlib.pyplot as plt
import numpy as np

# Implementação da classe Node e FibonacciHeap (já fornecida acima)
class Node:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = None
        self.child = None
        self.mark = False
        self.next = self
        self.prev = self

class FibonacciHeap:
    
    def __init__(self):
        self.min_node = None
        self.total_nodes = 0

    def insert(self, key):
        new_node = Node(key)
        if not self.min_node:
            self.min_node = new_node
        else:
            self._add_to_root_list(new_node)
            if new_node.key < self.min_node.key:
                self.min_node = new_node
        self.total_nodes += 1
        return new_node

    def find_min(self):
        if not self.min_node:
            return None
        return self.min_node.key

    def extract_min(self):
        z = self.min_node
        if z:
            if z.child:
                children = [x for x in self._iterate(z.child)]
                for child in children:
                    self._add_to_root_list(child)
                    child.parent = None
            self._remove_from_root_list(z)
            if z == z.next:  # Foi o único nó
                self.min_node = None
            else:
                self.min_node = z.next
                self._consolidate()
            self.total_nodes -= 1
        return z.key if z else None

    def delete(self, node):
        self.decrease_key(node, float('-inf'))
        self.extract_min()

    def decrease_key(self, node, new_key):
        if new_key > node.key:
            raise ValueError("Novo valor é maior que a chave atual.")
        node.key = new_key
        parent = node.parent
        if parent and node.key < parent.key:
            self._cut(node, parent)
            self._cascading_cut(parent)
        if node.key < self.min_node.key:
            self.min_node = node

    def _cut(self, node, parent):
        self._remove_from_child_list(parent, node)
        parent.degree -= 1
        self._add_to_root_list(node)
        node.parent = None
        node.mark = False

    def _cascading_cut(self, node):
        parent = node.parent
        if parent:
            if not node.mark:
                node.mark = True
            else:
                self._cut(node, parent)
                self._cascading_cut(parent)

    def _consolidate(self):
        max_degree = int(self.total_nodes**0.5) + 1
        aux = [None] * max_degree

        for node in self._iterate(self.min_node):
            x = node
            d = x.degree
            while aux[d]:
                y = aux[d]
                if x.key > y.key:
                    x, y = y, x
                self._link(y, x)
                aux[d] = None
                d += 1
            aux[d] = x

        self.min_node = None
        for node in aux:
            if node:
                if not self.min_node or node.key < self.min_node.key:
                    self.min_node = node

    def _link(self, y, x):
        self._remove_from_root_list(y)
        if not x.child:
            x.child = y
        else:
            self._add_to_child_list(x, y)
        y.parent = x
        x.degree += 1
        y.mark = False

    def _add_to_root_list(self, node):
        if not self.min_node:
            self.min_node = node
        else:
            node.prev = self.min_node
            node.next = self.min_node.next
            self.min_node.next.prev = node
            self.min_node.next = node

    def _remove_from_root_list(self, node):
        if node.next == node:  # Único nó
            self.min_node = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev

    def _add_to_child_list(self, parent, node):
        if not parent.child:
            parent.child = node
            node.next = node.prev = node
        else:
            child = parent.child
            node.prev = child
            node.next = child.next
            child.next.prev = node
            child.next = node

    def _remove_from_child_list(self, parent, node):
        if parent.child == node:
            if node.next == node:  # Único filho
                parent.child = None
            else:
                parent.child = node.next
        node.prev.next = node.next
        node.next.prev = node.prev

    def _iterate(self, head):
        if not head:
            return
        node = head
        while True:
            yield node
            node = node.next
            if node == head:
                break

    def __init__(self):
        self.min_node = None
        self.total_nodes = 0

    def insert(self, key):
        new_node = Node(key)
        if not self.min_node:
            self.min_node = new_node
        else:
            self._add_to_root_list(new_node)
            if new_node.key < self.min_node.key:
                self.min_node = new_node
        self.total_nodes += 1
        return new_node

    def find_min(self):
        if not self.min_node:
            return None
        return self.min_node.key

    def extract_min(self):
        z = self.min_node
        if z:
            if z.child:
                children = [x for x in self._iterate(z.child)]
                for child in children:
                    self._add_to_root_list(child)
                    child.parent = None
            self._remove_from_root_list(z)
            if z == z.next:  # Foi o único nó
                self.min_node = None
            else:
                self.min_node = z.next
                self._consolidate()
            self.total_nodes -= 1
        return z.key if z else None


# análise de desempenho
def analyze_fibonacci_heap(dataset):
    fib_heap = FibonacciHeap()
    times = {}

    # Medir tempo de inserção
    start = time.time()
    nodes = [fib_heap.insert(num) for num in dataset]
    times["Inserção"] = time.time() - start

    # Medir tempo para encontrar o mínimo
    start = time.time()
    min_value = fib_heap.find_min()
    times["Busca Mínimo"] = time.time() - start

    # Medir tempo para extração do mínimo
    start = time.time()
    for _ in range(len(dataset)):
        fib_heap.extract_min()
    times["Extração Mínimo"] = time.time() - start

    return times

# Carregar dataset
dataset_path = "dataset_100000_numbers.txt"
dataset = np.loadtxt(dataset_path, dtype=int)

# Executar análise
performance = analyze_fibonacci_heap(dataset)

# Gerar gráficos
plt.figure(figsize=(10, 6))
plt.bar(performance.keys(), performance.values(), color=['blue', 'orange', 'green'])
plt.title("Desempenho da Heap de Fibonacci")
plt.ylabel("Tempo (segundos)")
plt.xlabel("Operação")
plt.show()
