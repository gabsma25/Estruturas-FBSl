import random
import sys

# Configurações para a Skip List
MAX_LEVEL = 6
P = 0.5  # Probabilidade de promoção de nível


class Node:
    def __init__(self, key, level):
        self.key = key
        self.forward = [None] * (level + 1)


class SkipList:
    def __init__(self):
        self.level = 0
        self.header = Node(-sys.maxsize, MAX_LEVEL)  # Cabeçalho com chave -∞

    def random_level(self):
        level = 0
        while random.random() < P and level < MAX_LEVEL:
            level += 1
        return level

    def insert(self, key):
        update = [None] * (MAX_LEVEL + 1)
        current = self.header

        # Encontrar os pontos de inserção
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        # Se a chave não está presente, insere-a
        if not current or current.key != key:
            new_level = self.random_level()
            if new_level > self.level:
                for i in range(self.level + 1, new_level + 1):
                    update[i] = self.header
                self.level = new_level

            # Criar novo nó
            new_node = Node(key, new_level)
            for i in range(new_level + 1):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node

    def delete(self, key):
        update = [None] * (MAX_LEVEL + 1)
        current = self.header

        # Encontrar o nó a ser removido
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        # Se a chave está presente, remove-a
        if current and current.key == key:
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]

            # Ajusta o nível da Skip List
            while self.level > 0 and not self.header.forward[self.level]:
                self.level -= 1

    def find_min(self):
        if self.header.forward[0]:
            return self.header.forward[0].key
        return -sys.maxsize  # Retorna -∞ se a lista estiver vazia

    def display(self):
        print("Skip List:")
        for i in range(self.level, -1, -1):
            current = self.header.forward[i]
            print(f"Level {i}: ", end="")
            while current:
                print(current.key, end=" ")
                current = current.forward[i]
            print()


# Teste da Skip List
if __name__ == "__main__":
    random.seed()

    skip_list = SkipList()
    skip_list.insert(10)
    skip_list.insert(20)
    skip_list.insert(5)
    skip_list.insert(1)

    skip_list.display()

    print(f"Mínimo: {skip_list.find_min()}")

    skip_list.delete(5)
    print("Após remover 5:")
    skip_list.display()

    print(f"Mínimo após remoção: {skip_list.find_min()}")
