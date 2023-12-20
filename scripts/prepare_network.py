input_file = snakemake.input[0]
output_file = snakemake.output[0]

import os

with open(input_file, 'r') as file:
    n = int(file.read().strip())

output_dir = os.path.dirname(output_file)

os.makedirs(output_dir, exist_ok=True)


for i in range(n):
    with open(f"{output_dir}/n{i}.txt", 'w') as out_file:
        out_file.write(str(i+1))

with open(output_file,'w') as done_file:
    done_file.write("done")