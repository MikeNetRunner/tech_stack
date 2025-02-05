import os
import pandas as pd
import time


from rich.console import Console
from rich.table import Table
from typing import List, Callable, Tuple


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


# === Sorting Shell ===
def shell_sort(arr: List[int], gap_sequence: Callable[[int], List[int]]) -> None:
    """
    Sort shell with any sequence.
    """
    n = len(arr)
    gaps = gap_sequence(n)
    for gap in gaps:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp


# === Function for shell sorts ===
def shell_sequence(n: int) -> List[int]:
    """Shell: n // 2, n // 4, ..., 1"""
    gaps = []
    gap = n // 2
    while gap > 0:
        gaps.append(gap)
        gap //= 2
    return gaps


def knuth_sequence(n: int) -> List[int]:
    """Knuth: 1, 4, 13, 40, ..."""
    gaps = []
    gap = 1
    while gap < n:
        gaps.append(gap)
        gap = gap * 3 + 1
    return gaps[::-1]


def hibbard_sequence(n: int) -> List[int]:
    """Hibbard: 1, 3, 7, 15, ..., 2^k - 1"""
    gaps = []
    k = 1
    while (gap := 2**k - 1) < n:
        gaps.append(gap)
        k += 1
    return gaps[::-1]


def sedgewick_sequence(n: int) -> List[int]:
    """Sedgewick: 1, 5, 19, 41, ..."""
    gaps = []
    k = 0
    while True:
        if k % 2 == 0:
            gap = 9 * (2**k - 2**(k//2)) + 1
        else:
            gap = 8 * 2**k - 6 * 2**((k + 1)//2) + 1
        if gap >= n:
            break
        gaps.append(gap)
        k += 1
    return gaps[::-1]


# === load data ===
def load_data_from_files(directory: str) -> List[Tuple[str, List[int]]]:
    """
    Load files from directory.
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


# Create console
console = Console()


# === Time measuring ===
if __name__ == "__main__":
    directory = "/home/linux/tech_stack/python/algorithms/algorithms_part1/kfiles"
    excel_folder = os.path.join(os.getcwd(), "excel")
    os.makedirs(excel_folder, exist_ok=True)
    datasets = load_data_from_files(directory)
    sequences = {
        "Shell Sequence": shell_sequence,
        "Knuth Sequence": knuth_sequence,
        "Hibbard Sequence": hibbard_sequence,
        "Sedgewick Sequence": sedgewick_sequence,
    }

    # Store results for later Excel export
    results_10_repeats = []
    results_1_repeat = []

    for filename, data in datasets:
        # Determine number of repetitions based on file name (10 for certain files, 1 for others)
        repeat_count = 1 if "WL" in filename or "WP1R" in filename or "WK1R" in filename else 10
        console.print(f"\n[bold yellow]=== Processing file: {filename} ===[/bold yellow]")
        
        # Initialize the table
        table = Table(title=f"Shell Sort Times for {filename}", title_style="bold blue")
        table.add_column("Gap Sequence", style="cyan", justify="left")
        table.add_column("Avg Time (seconds)", style="magenta", justify="right")
        table.add_column("Std Dev (seconds)", style="magenta", justify="right")

        # Track times for each gap sequence
        times = {name: [] for name in sequences}

        for name, gap_func in sequences.items():
            time_taken_list = []
            for _ in range(repeat_count):
                time_taken, _ = measure_sort_time(lambda d: shell_sort(d, gap_func), data)
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
    df_10_repeats = pd.DataFrame(results_10_repeats, columns=["Filename", "Gap Sequence", "Avg Time (s)", "Std Dev (s)"])
    df_10_repeats_pivoted = df_10_repeats.pivot(index="Filename", columns="Gap Sequence", values="Avg Time (s)")
    df_10_repeats_pivoted.to_excel("shell_sort_results_10_repeats.xlsx", index=True, engine="openpyxl")
    console.print("\n[bold green]Results for 10 repeats have been saved to 'shell_sort_results_10_repeats.xlsx'[/bold green]")

    # Export for 1 repeat
    df_1_repeat = pd.DataFrame(results_1_repeat, columns=["Filename", "Gap Sequence", "Avg Time (s)", "Std Dev (s)"])
    df_1_repeat_pivoted = df_1_repeat.pivot(index="Filename", columns="Gap Sequence", values="Avg Time (s)")
    df_1_repeat_pivoted.to_excel("shell_sort_results_1_repeat.xlsx", index=True, engine="openpyxl")
    console.print("\n[bold green]Results for 1 repeat have been saved to 'shell_sort_results_1_repeat.xlsx'[/bold green]")
