input_file = snakemake.input[0]
output_dir = snakemake.output[0]
print(output_dir)

import os

with open(input_file, 'r') as file:
    n = int(file.read().strip())

os.makedirs(output_dir, exist_ok=True)


for i in range(n):
    with open(f"{output_dir}/n{i}.txt", 'w') as out_file:
        out_file.write(str(i+1))
