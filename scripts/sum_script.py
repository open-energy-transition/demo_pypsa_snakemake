import sys

input_file = snakemake.input[0]
output_file = snakemake.output[0]

with open(input_file, 'r') as file:
    numbers = [int(line.strip()) for line in file.readlines()]
total = sum(numbers)

with open(output_file, 'w') as file:
    file.write(str(total))
    


