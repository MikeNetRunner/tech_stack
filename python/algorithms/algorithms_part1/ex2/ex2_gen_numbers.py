import random

def save_to_file(file_name, numbers):
    with open(file_name, 'w') as file:
        for number in numbers:
            file.write(f"{number}\n")

# a. od 1 do 20
numbers_a = random.sample(range(1, 21), 20)
save_to_file("20_Malecki_a.txt", numbers_a)

# b. od 1 do 5
numbers_b = [random.randint(1, 5) for _ in range(20)]
save_to_file("20_Malecki_b.txt", numbers_b)

# c. od 1 do 10
numbers_c = [random.randint(1, 10) for _ in range(20)]
save_to_file("20_Malecki_c.txt", numbers_c)

# d. od 1 do 500
numbers_d = [random.randint(1, 500) for _ in range(20)]
save_to_file("20_Malecki_d.txt", numbers_d)

# e. od -9 do 10
numbers_e = random.sample(range(-9, 11), 20)
save_to_file("20_Malecki_e.txt", numbers_e)
