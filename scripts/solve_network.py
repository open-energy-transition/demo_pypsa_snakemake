import os

first_directory = snakemake.input[0]
second_directory = snakemake.output[0]

if not os.path.exists(second_directory):
    os.makedirs(second_directory)

for filename in os.listdir(first_directory):
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
    new_file_path = os.path.join(second_directory, "solve"+filename)

    # Write the squared number to the new file
    with open(new_file_path, 'w') as new_file:
        new_file.write(str(squared_number))

