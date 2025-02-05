import os
import time
import pandas as pd
from typing import List, Callable, Tuple
from rich.console import Console
from rich.table import Table


# === Measure time ===
def measure_sort_time(sort_function: Callable[[List[int]], None], data: List[int]) -> Tuple[float, List[int]]:
    """
    Measure time for operation.
    """
    data_copy = data[:]  # Create a copy of the data to sort independently
    start_time = time.perf_counter()
    sort_function(data_copy)
    end_time = time.perf_counter()
    return end_time - start_time, data_copy


# === Quicksort with middle pivot ===
def partition(arr: List[int], low: int, high: int, pivot_strategy: Callable[[List[int], int, int], int]) -> int:
    """
    Partition with middle pivot.
    """
    pivot_index = pivot_strategy(arr, low, high)  # Use pivot strategy
    arr[low], arr[pivot_index] = arr[pivot_index], arr[low]  # Move pivot to start
    pivot = arr[low]
    i = low + 1
    for j in range(low + 1, high + 1):
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[low], arr[i - 1] = arr[i - 1], arr[low]
    return i - 1


def quicksort_generic(arr: List[int], pivot_strategy: Callable[[List[int], int, int], int]) -> None:
    """
    Generic implementation of QuickSort with a dynamic pivot strategy.
    """
    def quicksort(low, high):
        if low < high:
            pivot_index = partition(arr, low, high, pivot_strategy)
            quicksort(low, pivot_index - 1)
            quicksort(pivot_index + 1, high)

    quicksort(0, len(arr) - 1)


# === Pivot strategy for middle element ===
def middle_pivot_strategy(arr: List[int], low: int, high: int) -> int:
    return (low + high) // 2  # Middle element as pivot


# === Shell sort seq. Knuth ===
def knuth_sequence(n: int) -> List[int]:
    """Knuth: 1, 4, 13, 40, ..."""
    gaps = []
    gap = 1
    while gap < n:
        gaps.append(gap)
        gap = gap * 3 + 1
    return gaps[::-1]


def shell_sort(arr: List[int]) -> None:
    n = len(arr)
    gaps = knuth_sequence(n)
    for gap in gaps:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp


# === Mergesort ===
def merge_sort(arr: List[int]) -> None:
    if len(arr) > 1:
        mid = len(arr) // 2
        L, R = arr[:mid], arr[mid:]
        merge_sort(L)
        merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


# === InsertionSort ===
def insertion_sort(arr: List[int]) -> None:
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


# === SelectionSort ===
def selection_sort(arr: List[int]) -> None:
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]


# === HeapSort ===
def heapify(arr: List[int], n: int, i: int) -> None:
    largest = i
    l, r = 2 * i + 1, 2 * i + 2
    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr: List[int]) -> None:
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)


# === CountingSort ===
def counting_sort(arr: List[int]) -> None:
    max_val, min_val = max(arr), min(arr)
    range_of_elements = max_val - min_val + 1
    count = [0] * range_of_elements
    for num in arr:
        count[num - min_val] += 1
    arr_idx = 0
    for i in range(range_of_elements):
        while count[i] > 0:
            arr[arr_idx] = i + min_val
            arr_idx += 1
            count[i] -= 1


# === Load data ===
def load_data_from_files(directory: str) -> List[Tuple[str, List[int]]]:
    all_data = []
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r") as file:
                data = list(map(int, file.read().split()))
                all_data.append((filename, data))
    return all_data


# === Create console ===
console = Console()


# === Time measuring ===
if __name__ == "__main__":
    directory = "/home/linux/tech_stack/python/algorithms/algorithms_part1/kfiles"
    excel_folder = "excel"
    os.makedirs(excel_folder, exist_ok=True)
    datasets = load_data_from_files(directory)
    sort_variants = {
        "QuickSort (Middle Pivot)": lambda data: quicksort_generic(data, middle_pivot_strategy),
        "ShellSort (Knuth)": shell_sort,
        "MergeSort": merge_sort,
        "InsertionSort": insertion_sort,
        "SelectionSort": selection_sort,
        "HeapSort": heap_sort,
        "CountingSort": counting_sort,
    }

    results = []

    for filename, data in datasets:
        repeat_count = 1 if any(prefix in filename for prefix in ["WL", "WP1R", "WK1R"]) else 10
        row = {"Filename": filename}
        console.print(f"\n[bold yellow]=== Processing file: {filename} ===[/bold yellow]")
        
        # Initialize the table
        table = Table(title=f"Sorting Times for {filename}", title_style="bold blue")
        table.add_column("Algorithm", style="cyan", justify="left")
        table.add_column("Avg Time (seconds)", style="magenta", justify="right")

        for name, sort_func in sort_variants.items():
            time_taken_list = []
            for _ in range(repeat_count):
                time_taken, _ = measure_sort_time(sort_func, data)
                time_taken_list.append(time_taken)

            # Calculate AVERAGE
            avg_time = sum(time_taken_list) / repeat_count
            row[name] = avg_time

            # Add to Rich table
            table.add_row(name, f"{avg_time:.6f}")

        # Print the table for the current file
        console.print(table)

        # Append row to results
        results.append(row)

    # === Save results to Excel ===
    df = pd.DataFrame(results)
    df.to_excel(os.path.join(excel_folder, "sorting_results.xlsx"), index=False, engine="openpyxl")
    console.print(f"[bold green]Results saved to {os.path.join(excel_folder, 'sorting_results.xlsx')}[/bold green]")