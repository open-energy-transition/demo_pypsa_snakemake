import sys

# Reading file paths from command line arguments
input_file = sys.argv[0]
output_file = sys.argv[1]

# Reading numbers and calculating sum
with open(input_file, 'r') as file:
    numbers = [int(line.strip()) for line in file.readlines()]
total = sum(numbers)

# Writing the result to output file
with open(output_file, 'w') as file:
    file.write(str(total))
