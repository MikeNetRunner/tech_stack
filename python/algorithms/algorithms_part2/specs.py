from rich.console import Console
from rich.table import Table

# Tworzenie konsoli Rich
console = Console()

# Tworzenie tabeli
table = Table(title="\nInformacje o środowisku eksperymentalnym")

# Dodawanie kolumn
table.add_column("Kategoria", style="cyan", justify="right")
table.add_column("Dane", style="magenta", justify="left")

# Dodawanie wierszy
table.add_row("Język programowania", "Python 3.12.7")
table.add_row("Kompilator", "Visual Studio Code")
table.add_row("System operacyjny", "WSL Kali Linux (na Windows 10 Pro)")
table.add_row("Procesy w tle", "Podstawowe procesy dla WSL i systemu Windows")
table.add_row("Procesor", "Intel Core i5 14th 14600KF, 3.5 GHz")
table.add_row("RAM", "32 GB, 4800 MHz")
table.add_row("Dysk", "SSD, prędkość odczytu i zapisu: 7000 MB/s")

# Wyświetlenie tabeli
console.print(table)
