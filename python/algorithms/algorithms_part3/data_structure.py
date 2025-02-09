import sys
import time
import random
import os
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table
from typing import Callable, Tuple

sys.setrecursionlimit(1000000)

DATA_DIR = os.path.expanduser("~/tech_stack/python/algorithms/algorithms_part3")
os.makedirs(DATA_DIR, exist_ok=True)

# === Measure time ===
def measure_time(operation: Callable, *args) -> Tuple[float, any]:
    start_time = time.perf_counter()
    result = operation(*args)
    end_time = time.perf_counter()
    return end_time - start_time, result

# === Implementacje struktur ===

# 📌 Drzewo BST z poprawnym usuwaniem
class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return BSTNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)
        return node

    def search(self, key):
        return self._search(self.root, key) is not None

    def _search(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return node
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self.find_min(node.right)  # Znajdujemy najmniejszy węzeł z prawego poddrzewa
            node.key = temp.key  # Kopiujemy wartość
            node.right = self._delete(node.right, temp.key)  # Usuwamy najmniejszy węzeł
        return node

    def find_min(self, node):
        """ Znajduje węzeł o najmniejszym kluczu w poddrzewie """
        while node.left:
            node = node.left
        return node  # Zwracamy węzeł, nie wartość

# 📌 Implementacja stosu
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop() if self.stack else None

    def search(self, item):
        return item in self.stack

# 📌 Implementacja kolejki
class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        return self.queue.pop(0) if self.queue else None

    def search(self, item):
        return item in self.queue

# === Generowanie danych ===
def generate_data(size: int):
    return [random.randint(0, 10000) for _ in range(size)]

# === Testowanie i benchmark ===
def benchmark(size=100000):
    console = Console()
    table = Table(title="Czasy operacji")
    table.add_column("Struktura", justify="left", style="cyan", no_wrap=True)
    table.add_column("Insert (s)", justify="right", style="magenta")
    table.add_column("Search (s)", justify="right", style="green")
    table.add_column("Delete (s)", justify="right", style="yellow")

    numbers = generate_data(size)
    
    results = {}

    # 📌 Lista
    lst = []
    insert_time, _ = measure_time(lambda: [lst.append(x) for x in numbers])
    search_time, _ = measure_time(lambda: [x in lst for x in numbers])
    delete_time, _ = measure_time(lambda: [lst.remove(x) for x in numbers if x in lst])
    table.add_row("List", f"{insert_time:.6f}", f"{search_time:.6f}", f"{delete_time:.6f}")
    results["List"] = (insert_time, search_time, delete_time)

    # 📌 Dict
    hash_map = {}
    insert_time, _ = measure_time(lambda: [hash_map.update({x: True}) for x in numbers])
    search_time, _ = measure_time(lambda: [x in hash_map for x in numbers])
    delete_time, _ = measure_time(lambda: [hash_map.pop(x, None) for x in numbers])
    table.add_row("Dict", f"{insert_time:.6f}", f"{search_time:.6f}", f"{delete_time:.6f}")
    results["Dict"] = (insert_time, search_time, delete_time)

    # 📌 BST - drzewo wyszukiwań binarnych
    bst = BST()
    insert_time, _ = measure_time(lambda: [bst.insert(x) for x in numbers])
    search_time, _ = measure_time(lambda: [bst.search(x) for x in numbers])
    delete_time, _ = measure_time(lambda: [bst.delete(x) for x in numbers])
    table.add_row("BST", f"{insert_time:.6f}", f"{search_time:.6f}", f"{delete_time:.6f}")
    results["BST"] = (insert_time, search_time, delete_time)

    # 📌 Stack
    stack = Stack()
    insert_time, _ = measure_time(lambda: [stack.push(x) for x in numbers])
    search_time, _ = measure_time(lambda: [stack.search(x) for x in numbers])
    delete_time, _ = measure_time(lambda: [stack.pop() for _ in range(size)])
    table.add_row("Stack", f"{insert_time:.6f}", f"{search_time:.6f}", f"{delete_time:.6f}")
    results["Stack"] = (insert_time, search_time, delete_time)

    # 📌 Queue
    queue = Queue()
    insert_time, _ = measure_time(lambda: [queue.enqueue(x) for x in numbers])
    search_time, _ = measure_time(lambda: [queue.search(x) for x in numbers])
    delete_time, _ = measure_time(lambda: [queue.dequeue() for _ in range(size)])
    table.add_row("Queue", f"{insert_time:.6f}", f"{search_time:.6f}", f"{delete_time:.6f}")
    results["Queue"] = (insert_time, search_time, delete_time)

    console.print(table)

    # === Wykresy ===
    structures = list(results.keys())
    insert_times = [results[struct][0] for struct in structures]
    search_times = [results[struct][1] for struct in structures]
    delete_times = [results[struct][2] for struct in structures]

    plt.figure(figsize=(10, 5))
    plt.bar(structures, insert_times, color='magenta', label='Insert')
    plt.bar(structures, search_times, color='green', label='Search', bottom=insert_times)
    plt.bar(structures, delete_times, color='yellow', label='Delete', bottom=[i+s for i, s in zip(insert_times, search_times)])
    plt.xlabel("Struktura danych")
    plt.ylabel("Czas (s)")
    plt.title("Porównanie czasów operacji")
    plt.legend()
    plt.xticks(rotation=30)
    plt.show()

if __name__ == "__main__":
    benchmark()
