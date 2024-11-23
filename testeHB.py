class BinomialNode:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.child = None
        self.sibling = None
        self.parent = None


class BinomialHeap:
    def __init__(self):
        self.head = None

    def create_node(self, key):
        return BinomialNode(key)

    def link_trees(self, tree1, tree2):
        if tree1.key > tree2.key:
            tree1, tree2 = tree2, tree1
        tree2.parent = tree1
        tree2.sibling = tree1.child
        tree1.child = tree2
        tree1.degree += 1
        return tree1

    def merge_heaps(self, heap1, heap2):
        if heap1.head is None:
            return heap2
        if heap2.head is None:
            return heap1

        new_head = None
        h1 = heap1.head
        h2 = heap2.head

        if h1.degree <= h2.degree:
            new_head = h1
            h1 = h1.sibling
        else:
            new_head = h2
            h2 = h2.sibling

        current = new_head

        while h1 and h2:
            if h1.degree <= h2.degree:
                current.sibling = h1
                h1 = h1.sibling
            else:
                current.sibling = h2
                h2 = h2.sibling
            current = current.sibling

        current.sibling = h1 if h1 else h2

        merged_heap = BinomialHeap()
        merged_heap.head = new_head
        return merged_heap

    def union_heaps(self, heap1, heap2):
        merged_heap = self.merge_heaps(heap1, heap2)
        if not merged_heap.head:
            return merged_heap

        prev = None
        curr = merged_heap.head
        next = curr.sibling

        while next:
            if (curr.degree != next.degree) or (
                next.sibling and next.sibling.degree == curr.degree
            ):
                prev = curr
                curr = next
            else:
                if curr.key <= next.key:
                    curr.sibling = next.sibling
                    curr = self.link_trees(curr, next)
                else:
                    if prev:
                        prev.sibling = next
                    else:
                        merged_heap.head = next
                    next = self.link_trees(curr, next)
                    curr = next
            next = curr.sibling

        return merged_heap

    def insert(self, key):
        new_node = self.create_node(key)
        temp_heap = BinomialHeap()
        temp_heap.head = new_node
        self.head = self.union_heaps(self, temp_heap).head

    def find_min(self):
        if not self.head:
            return None

        min_node = self.head
        curr = self.head

        while curr:
            if curr.key < min_node.key:
                min_node = curr
            curr = curr.sibling

        return min_node

    def reverse_list(self, node):
        prev = None
        curr = node

        while curr:
            next = curr.sibling
            curr.sibling = prev
            prev = curr
            curr = next

        return prev

    def extract_min(self):
        if not self.head:
            return None

        min_node = self.head
        min_prev = None
        curr = self.head
        prev = None

        while curr.sibling:
            if curr.sibling.key < min_node.key:
                min_node = curr.sibling
                min_prev = curr
            curr = curr.sibling

        if min_prev:
            min_prev.sibling = min_node.sibling
        else:
            self.head = min_node.sibling

        child = min_node.child
        if child:
            child = self.reverse_list(child)
            temp_heap = BinomialHeap()
            temp_heap.head = child
            self.head = self.union_heaps(self, temp_heap).head

        return min_node


# Teste do heap binomial
if __name__ == "__main__":
    heap = BinomialHeap()

    heap.insert(10)
    heap.insert(20)
    heap.insert(5)

    min_node = heap.find_min()
    if min_node:
        print(f"Min: {min_node.key}")

    min_node = heap.extract_min()
    if min_node:
        print(f"Extracted Min: {min_node.key}")

    min_node = heap.find_min()
    if min_node:
        print(f"Min: {min_node.key}")
