import os
import random
import sys
import time
from typing import Callable, Tuple

import numpy as np
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table

sys.setrecursionlimit(1000000)

DATA_DIR = os.path.expanduser("~/tech_stack/python/algorithms/algorithms_part3")
os.makedirs(DATA_DIR, exist_ok=True)

# === Measure execution time ===
def measure_time(operation: Callable, *args) -> Tuple[float, any]:
    start_time = time.perf_counter()
    result = operation(*args)
    end_time = time.perf_counter()
    return end_time - start_time, result

# === Implementations of data structures ===

# 📌 Binary Search Tree (BST) with proper deletion
class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None
        self.insert_count = 0
        self.search_count = 0
        self.delete_count = 0

    def insert(self, key):
        self.root = self._insert(self.root, key)
        self.insert_count += 1

    def _insert(self, node, key):
        if node is None:
            return BSTNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)
        return node

    def search(self, key):
        self.search_count += 1
        return self._search(self.root, key) is not None

    def _search(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def delete(self, key):
        self.root = self._delete(self.root, key)
        self.delete_count += 1

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
            temp = self.find_min(node.right)  # Find the smallest node in the right subtree
            node.key = temp.key  # Copy the value
            node.right = self._delete(node.right, temp.key)  # Remove the smallest node
        return node

    def find_min(self, node):
        """ Finds the node with the smallest key in a subtree """
        while node.left:
            node = node.left
        return node  # Return the node, not just the value

# 📌 Stack implementation
class Stack:
    def __init__(self):
        self.stack = []
        self.insert_count = 0
        self.search_count = 0
        self.delete_count = 0

    def push(self, item):
        self.stack.append(item)
        self.insert_count += 1

    def pop(self):
        if self.stack:
            self.delete_count += 1
            return self.stack.pop()
        return None

    def search(self, item):
        self.search_count += 1
        return item in self.stack

# 📌 Queue implementation
class Queue:
    def __init__(self):
        self.queue = []
        self.insert_count = 0
        self.search_count = 0
        self.delete_count = 0

    def enqueue(self, item):
        self.queue.append(item)
        self.insert_count += 1

    def dequeue(self):
        if self.queue:
            self.delete_count += 1
            return self.queue.pop(0)
        return None

    def search(self, item):
        self.search_count += 1
        return item in self.queue

# === Generate random data ===
def generate_data(size: int):
    return [random.randint(0, 10000) for _ in range(size)]

# === Benchmarking and testing ===
def benchmark(size):
    console = Console()
    table = Table(title=f"Operation Times for {size} Elements")
    table.add_column("Structure", justify="left", style="cyan", no_wrap=True)
    table.add_column("Insert (s)", justify="right", style="magenta")
    table.add_column("Search (s)", justify="right", style="green")
    table.add_column("Delete (s)", justify="right", style="yellow")

    numbers = generate_data(size)
    
    results = {}

    # 📌 List
    lst = []
    insert_time, _ = measure_time(lambda: [lst.append(x) for x in numbers])
    search_time, _ = measure_time(lambda: [x in lst for x in numbers])
    delete_time, _ = measure_time(lambda: [lst.remove(x) for x in numbers if x in lst])
    table.add_row("List", f"{insert_time:.6f}", f"{search_time:.6f}", f"{delete_time:.6f}")
    results["List"] = (insert_time, search_time, delete_time)

    # 📌 Dictionary (Hash Map)
    hash_map = {}
    insert_time, _ = measure_time(lambda: [hash_map.update({x: True}) for x in numbers])
    search_time, _ = measure_time(lambda: [x in hash_map for x in numbers])
    delete_time, _ = measure_time(lambda: [hash_map.pop(x, None) for x in numbers])
    table.add_row("Dict", f"{insert_time:.6f}", f"{search_time:.6f}", f"{delete_time:.6f}")
    results["Dict"] = (insert_time, search_time, delete_time)

    # 📌 BST - Binary Search Tree
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

    # === Display operation counts ===
    console.print("\n[bold]Operation Counts:[/bold]")
    counts_table = Table(title="Operation Counts")
    counts_table.add_column("Structure", justify="left", style="cyan", no_wrap=True)
    counts_table.add_column("Inserted", justify="right", style="magenta")
    counts_table.add_column("Searched", justify="right", style="green")
    counts_table.add_column("Deleted", justify="right", style="yellow")

    counts_table.add_row("List", str(size), str(size), str(size))
    counts_table.add_row("Dict", str(size), str(size), str(size))
    counts_table.add_row("BST", str(bst.insert_count), str(bst.search_count), str(bst.delete_count))
    counts_table.add_row("Stack", str(stack.insert_count), str(stack.search_count), str(stack.delete_count))
    counts_table.add_row("Queue", str(queue.insert_count), str(queue.search_count), str(queue.delete_count))

    console.print(counts_table)

    # === Plot results ===
    structures = list(results.keys())
    insert_times = [results[struct][0] for struct in structures]
    search_times = [results[struct][1] for struct in structures]
    delete_times = [results[struct][2] for struct in structures]

    # Set up the positions for each group of bars
    x = np.arange(len(structures))  # the label locations
    width = 0.25  # the width of the bars

    # Create the plot
    plt.figure(figsize=(12, 7))  # Increase the figure size for more space

    # Plot the bars for each operation
    plt.bar(x - width, insert_times, width, color='magenta', label='Insert')
    plt.bar(x, search_times, width, color='green', label='Search')
    plt.bar(x + width, delete_times, width, color='yellow', label='Delete')

    # Adding labels, title, and legend
    plt.xlabel("Data Structure", fontsize=12)
    plt.ylabel("Time (s)", fontsize=12)
    plt.title(f"Comparison of Operation Times for {size} Elements", fontsize=14)
    plt.xticks(x, structures, rotation=45, ha='right', fontsize=10)  # Rotate labels and adjust alignment
    plt.legend()
    plt.grid(True, axis='y')

    # Make sure layout is tight to avoid cutting off labels
    plt.tight_layout()

    # Show the plot
    plt.show()

if __name__ == "__main__":
    sizes = [10, 100, 1000, 10000, 100000]
    for size in sizes:
        benchmark(size)