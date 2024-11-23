class BinomialNode:
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.child = None
        self.sibling = None
        self.degree = 0  # Número de filhos

class BinomialHeap:
    def __init__(self):
        self.head = None

    def insert(self, key):
        new_heap = BinomialHeap()
        new_heap.head = BinomialNode(key)
        self.head = self._union(self.head, new_heap.head)

    def find_min(self):
        if not self.head:
            return None
        current = self.head
        min_node = current
        while current:
            if current.key < min_node.key:
                min_node = current
            current = current.sibling
        return min_node.key

    def extract_min(self):
        if not self.head:
            return None
        # Encontrar o nó mínimo e seu pai
        min_node = self.head
        min_node_prev = None
        prev = None
        current = self.head
        while current:
            if current.key < min_node.key:
                min_node = current
                min_node_prev = prev
            prev = current
            current = current.sibling

        # Remover o nó mínimo da lista de raízes
        if min_node_prev:
            min_node_prev.sibling = min_node.sibling
        else:
            self.head = min_node.sibling

        # Reverter a lista de filhos do nó mínimo
        child = min_node.child
        new_head = None
        while child:
            next_child = child.sibling
            child.sibling = new_head
            new_head = child
            child.parent = None
            child = next_child

        # Unir a lista de filhos do mínimo ao heap atual
        self.head = self._union(self.head, new_head)
        return min_node.key

    def delete(self, node):
        # Diminuir a chave do nó para -∞ e extrair o mínimo
        self.decrease_key(node, float('-inf'))
        self.extract_min()

    def decrease_key(self, node, new_key):
        if new_key > node.key:
            raise ValueError("A nova chave deve ser menor que a chave atual.")
        node.key = new_key
        while node.parent and node.key < node.parent.key:
            # Trocar a chave com o pai
            node.key, node.parent.key = node.parent.key, node.key
            node = node.parent

    def _union(self, heap1, heap2):
        merged = self._merge(heap1, heap2)
        if not merged:
            return None

        prev = None
        current = merged
        next_node = current.sibling

        while next_node:
            if current.degree != next_node.degree or (next_node.sibling and next_node.sibling.degree == current.degree):
                prev = current
                current = next_node
            else:
                if current.key <= next_node.key:
                    current.sibling = next_node.sibling
                    self._link(next_node, current)
                else:
                    if prev:
                        prev.sibling = next_node
                    else:
                        merged = next_node
                    self._link(current, next_node)
                    current = next_node
            next_node = current.sibling

        return merged

    def _merge(self, heap1, heap2):
        if not heap1:
            return heap2
        if not heap2:
            return heap1

        if heap1.degree <= heap2.degree:
            head = heap1
            heap1 = heap1.sibling
        else:
            head = heap2
            heap2 = heap2.sibling

        current = head
        while heap1 and heap2:
            if heap1.degree <= heap2.degree:
                current.sibling = heap1
                heap1 = heap1.sibling
            else:
                current.sibling = heap2
                heap2 = heap2.sibling
            current = current.sibling

        current.sibling = heap1 if heap1 else heap2
        return head

    def _link(self, y, z):
        # y torna-se o filho de z
        y.parent = z
        y.sibling = z.child
        z.child = y
        z.degree += 1
