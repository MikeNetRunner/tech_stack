import os
import pandas as pd
import random
import sys
import time


from rich.console import Console
from rich.table import Table
from rich.text import Text
from typing import List, Callable, Tuple


# === Set limit recursion ===
sys.setrecursionlimit(1000000)


# === Measure time ===
def measure_sort_time(sort_function: Callable[[List[int]], None], data: List[int]) -> Tuple[float, List[int]]:
    """
    Measure time for operation.
    """
    data_copy = data[:]  # Create a copy of the data to sort independently
    start_time = time.perf_counter() # Start timer
    sort_function(data_copy) # Call sorting algorithm
    end_time = time.perf_counter() # End timer
    return end_time - start_time, data_copy


# === Common partition logic for QuickSort ===
def partition(arr: List[int], low: int, high: int, pivot_strategy: Callable[[List[int], int, int], int]) -> int:
    """
    Partition with dynamic pivot.
    """
    pivot_index = pivot_strategy(arr, low, high)
    arr[low], arr[pivot_index] = arr[pivot_index], arr[low]  # Move pivot on start
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
    Uni implementation QuickSort.
    """
    def quicksort(low, high):
        if low < high:
            pivot_index = partition(arr, low, high, pivot_strategy)
            quicksort(low, pivot_index - 1)
            quicksort(pivot_index + 1, high)

    quicksort(0, len(arr) - 1)


# === Pivot position ===
def first_pivot_strategy(arr: List[int], low: int, high: int) -> int:
    return low


def last_pivot_strategy(arr: List[int], low: int, high: int) -> int:
    return high


def middle_pivot_strategy(arr: List[int], low: int, high: int) -> int:
    return (low + high) // 2


def random_pivot_strategy(arr: List[int], low: int, high: int) -> int:
    return random.randint(low, high)


def median_of_three_pivot_strategy(arr: List[int], low: int, high: int) -> int:
    mid = (low + high) // 2
    trio = [(arr[low], low), (arr[mid], mid), (arr[high], high)]
    trio.sort(key=lambda x: x[0])
    return trio[1][1]


# === Load data ===
def load_data_from_files(directory: str) -> List[Tuple[str, List[int]]]:
    """
    Load files from the directory.
    """
    all_data = []
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".txt"):  # Read only .txt
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                try:
                    with open(filepath, "r") as file:
                        data = list(map(int, file.read().split()))
                        all_data.append((filename, data))
                except ValueError as e:
                    print(f"Error reading file {filename}: {e}")
    return all_data


# Tworzenie konsoli Rich
console = Console()


# === Test with measuring time ===
if __name__ == "__main__":
    directory = "/home/linux/tech_stack/python/algorithms/algorithms_part1/ex3"
    excel_folder = os.path.join(os.getcwd(), "excel")
    os.makedirs(excel_folder, exist_ok=True)
    datasets = load_data_from_files(directory)
    sort_variants = {
        "First Pivot": lambda data: quicksort_generic(data, first_pivot_strategy),
        "Last Pivot": lambda data: quicksort_generic(data, last_pivot_strategy),
        "Middle Pivot": lambda data: quicksort_generic(data, middle_pivot_strategy),
        "Random Pivot": lambda data: quicksort_generic(data, random_pivot_strategy),
        "Median of Three Pivot": lambda data: quicksort_generic(data, median_of_three_pivot_strategy),
    }

    # Store results for later Excel export
    results_10_repeats = []
    results_1_repeat = []

    for filename, data in datasets:
        # Determine number of repetitions based on file name (10 for certain files, 1 for others)
        repeat_count = 1 if "WL" in filename or "WP1R" in filename or "WK1R" in filename else 10
        console.print(f"\n[bold yellow]=== Processing file: {filename} ===[/bold yellow]")
        
        # Initialize the table
        table = Table(title=f"Sorting Times for {filename}", title_style="bold blue")
        table.add_column("Algorithm QuickSort", style="cyan", justify="left")
        table.add_column("Avg Time (seconds)", style="magenta", justify="right")
        table.add_column("Std Dev (seconds)", style="magenta", justify="right")

        # Track times for each sort variant
        times = {name: [] for name in sort_variants}

        for name, sort_func in sort_variants.items():
            time_taken_list = []
            for _ in range(repeat_count):
                time_taken, _ = measure_sort_time(sort_func, data)
                time_taken_list.append(time_taken)

            # Calculate AVERAGE & STANDARD DEVIATION
            avg_time = sum(time_taken_list) / repeat_count
            std_dev = (sum((t - avg_time) ** 2 for t in time_taken_list) / repeat_count) ** 0.5

            # Store the results in the appropriate list based on the number of repetitions
            result_entry = (name, avg_time, std_dev)
            if repeat_count == 10:
                results_10_repeats.append((filename, *result_entry))
            else:
                results_1_repeat.append((filename, *result_entry))

            # Add row to table
            table.add_row(name, f"{avg_time:.6f}", f"{std_dev:.6f}")

        console.print(table)

    # === Export results to separate Excel files ===
    # Export for 10 repeats
    df_10_repeats = pd.DataFrame(results_10_repeats, columns=["Filename", "Algorithm", "Avg Time (s)", "Std Dev (s)"])
    df_10_repeats_pivoted = df_10_repeats.pivot(index="Filename", columns="Algorithm", values="Avg Time (s)")
    df_10_repeats_pivoted.to_excel("sorting_results_10_repeats.xlsx", index=True, engine="openpyxl")
    console.print("\n[bold green]Results for 10 repeats have been saved to 'sorting_results_10_repeats.xlsx'[/bold green]")

    # Export for 1 repeat
    df_1_repeat = pd.DataFrame(results_1_repeat, columns=["Filename", "Algorithm", "Avg Time (s)", "Std Dev (s)"])
    df_1_repeat_pivoted = df_1_repeat.pivot(index="Filename", columns="Algorithm", values="Avg Time (s)")
    df_1_repeat_pivoted.to_excel("sorting_results_1_repeat.xlsx", index=True, engine="openpyxl")
    console.print("\n[bold green]Results for 1 repeat have been saved to 'sorting_results_1_repeat.xlsx'[/bold green]")
