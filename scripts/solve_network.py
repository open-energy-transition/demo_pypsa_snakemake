import os

first_file = snakemake.input[0]
second_file = snakemake.output[0]

first_directory = os.path.dirname(first_file)
second_directory = os.path.dirname(second_file)

if not os.path.exists(second_directory):
    os.makedirs(second_directory)

for filename in os.listdir(first_directory):
    if filename == "done.txt":
        continue
    
    file_path = os.path.join(first_directory, filename)

    # Read the number from the file
    with open(file_path, 'r') as file:
        try:
            number = int(file.read().strip())
            squared_number = number ** 2
        except ValueError:
            print(f"Error reading number from {filename}")
            continue

    # Create a path for the new file in the second directory
    new_file_path = os.path.join(second_directory, "solved"+filename)

    # Write the squared number to the new file
    with open(new_file_path, 'w') as new_file:
        new_file.write(str(squared_number))

with open(second_file,'w') as done_file:
    done_file.write("done")