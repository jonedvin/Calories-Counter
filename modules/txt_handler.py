import os

def get_file_lines(filename: str) -> list:
    if not os.path.exists(filename):
        print(f"File not recognised: {filename}")
        return []
    
    with open(filename) as file:
        return file.readlines()
    

def write_lines_to_file(filename: str, lines: list):
    if not os.path.exists(filename):
        print(f"File not recognised: {filename}")
        return 
    
    with open(filename, "w") as file:
        for line in lines:
            file.write(line)


def remove_meal_from_file(filename: str, meal_string: str):
    if not os.path.exists(filename):
        print(f"File not recognised: {filename}")
        return 
    
    lines = get_file_lines(filename)
    for line in lines:
        if line.strip() == meal_string:
            lines.remove(line)
            break
    
    write_lines_to_file(filename, lines)


def add_meal_to_file(filename: str, meal_string: str):
    if not os.path.exists(filename):
        print(f"File not recognised: {filename}")
        return 
    
    with open(filename, "a") as file:
        file.write("\n"+meal_string)
