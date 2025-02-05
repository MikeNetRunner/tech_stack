import os
import random

# Path to the destination folder
folder_path = "/home/linux/tech_stack/python/algorithms/algorithms_part1/ex3"

# File sizes (thousands of items)
file_sizes = [2, 4, 6, 8, 10, 20, 40, 60, 80, 100, 200, 400, 600, 800, 1000]

# Create dir if doesn't exist
os.makedirs(folder_path, exist_ok=True)

# Gen and save files
for size in file_sizes:
    # Number of elements in files
    num_elements = size * 1000
    
    # Gen random numbers
    random_numbers = [random.randint(0, 1000000) for _ in range(num_elements)]
    
    # Create and save files for different orders
    if size >= 100:  # For files with more than 100k elements, generate only random files
        order = "random"
        random.shuffle(random_numbers)  # Shuffle the list randomly
        
        # Create file name with order included
        file_name = f"{size}k_{order}.txt"
        file_path = os.path.join(folder_path, file_name)
        
        # Save data to file
        with open(file_path, "w") as f:
            f.write("\n".join(map(str, random_numbers)))
        
        print(f"File saved: {file_path}")
    
    else:
        # For files with size <= 100k, generate all three versions: ascending, descending, and random
        for order in ["ascending", "descending", "random"]:
            # Sort list according to the order
            if order == "ascending":
                random_numbers.sort()  # Sort in ascending order
            elif order == "descending":
                random_numbers.sort(reverse=True)  # Sort in descending order
            else:
                random.shuffle(random_numbers)  # Shuffle the list randomly
            
            # Create file name with order included
            file_name = f"{size}k_{order}.txt"
            file_path = os.path.join(folder_path, file_name)
            
            # Save data to file
            with open(file_path, "w") as f:
                f.write("\n".join(map(str, random_numbers)))
            
            print(f"File saved: {file_path}")
