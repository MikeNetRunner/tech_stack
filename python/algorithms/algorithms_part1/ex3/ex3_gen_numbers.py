import random

def save_to_file(file_name, numbers):
    with open(file_name, 'w') as file:
        for number in numbers:
            file.write(f"{number}\n")

# 1. WL1 do WL30 od 1 do liczby elementów pliku bez powtórzeń
for i in range(1, 31):
    random.seed(i)
    numbers = random.sample(range(1, i + 21), i + 20)
    save_to_file(f"WL{i}.txt", numbers)

# 2. WL31 do WL60 od 1 do połowy liczby elementów pliku
for i in range(31, 61):
    random.seed(i)
    n = i + 20
    numbers = [random.randint(1, n // 2) for _ in range(n)]
    save_to_file(f"WL{i}.txt", numbers)

# 3. WR od 1 do liczby elementów pliku w porządku rosnącym
numbers_wr = list(range(1, 51))
save_to_file("WR.txt", numbers_wr)

# 4. WM od 1 do liczby elementów pliku w porządku malejącym
numbers_wm = list(range(1, 51))[::-1]
save_to_file("WM.txt", numbers_wm)

# 5. WP1R1 do WP1R30  losowa liczba na początku, reszta posortowana rosnąco
for i in range(1, 31):
    numbers = list(range(1, i + 20))
    random.seed(i)
    first_number = random.choice(numbers)
    numbers.remove(first_number)
    numbers.sort()
    numbers.insert(0, first_number)
    save_to_file(f"WP1R{i}.txt", numbers)

# 6. WK1R1 do WK1R30 losowa liczba na końcu, reszta posortowana rosnąco
for i in range(1, 31):
    numbers = list(range(1, i + 20))
    random.seed(i)
    last_number = random.choice(numbers)
    numbers.remove(last_number)
    numbers.sort()
    numbers.append(last_number)
    save_to_file(f"WK1R{i}.txt", numbers)

# 7. Sortowanie nieparzystych(odd) i parzystych(even)
n = 50  # 50 elementow w pliku

# WNRPR – odd rosnąco, potem even rosnąco
numbers = list(range(1, n + 1))
odd = sorted([x for x in numbers if x % 2 != 0])
even = sorted([x for x in numbers if x % 2 == 0])
save_to_file("WNRPR.txt", odd + even)

# WPRNR – even rosnąco, potem odd rosnąco | odwrotnie do WNRPR
save_to_file("WPRNR.txt", even + odd)

# WNRPM – odd rosnąco, potem even malejąco
even = sorted([x for x in numbers if x % 2 == 0], reverse=True)
save_to_file("WNRPM.txt", odd + even)

# WPRPM – even rosnąco, potem odd malejąco
odd = sorted([x for x in numbers if x % 2 != 0], reverse=True)
save_to_file("WPRPM.txt", even + odd)

# WNMPR – odd malejąco, potem even rosnąco
odd = sorted([x for x in numbers if x % 2 != 0], reverse=True)
even = sorted([x for x in numbers if x % 2 == 0])
save_to_file("WNMPR.txt", odd + even)

# WPRNM – even rosnąco, potem odd malejąco
save_to_file("WPRNM.txt", even + odd)

# WNMPM – odd i even malejąco
odd = sorted([x for x in numbers if x % 2 != 0], reverse=True)
even = sorted([x for x in numbers if x % 2 == 0], reverse=True)
save_to_file("WNMPM.txt", odd + even)

# WPMNM – even i odd malejąco
save_to_file("WPMNM.txt", even + odd)

# 8. WXM – wzor z zadania (1, 10, 2, 9, 3, 8, 4, 7, 5, 6)
numbers_wxm = []
for i in range(1, (n // 2) + 1):
    numbers_wxm.extend([i, n + 1 - i])
if n % 2 != 0:
    numbers_wxm.append((n // 2) + 1)
save_to_file("WXM.txt", numbers_wxm)

# 9. WXU – wzor z zadania (1, 5, 2, 4, 3, 5, 1, 4, 2, 3) dla elementow / 2
n = 50  # 50 elementow w pliku
half = n // 2
numbers_wxu = []
for i in range(1, half // 2 + 1):
    numbers_wxu.extend([i, half - i + 1])
save_to_file("WXU.txt", numbers_wxu)
