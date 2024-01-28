import sys
import subprocess
import os
# import snakemake
# import debugpy
# debugpy.listen(("localhost", 5678))

# debugpy.wait_for_client() 
# debugpy.breakpoint()

input_file = snakemake.input[0]
output_file = snakemake.output[0]

with open(input_file, 'r') as file:
    numbers = [int(line.strip()) for line in file.readlines()]
total = sum(numbers)

with open(output_file, 'w') as file:
    file.write(str(total))


# breakpoint()

subprocess.run(["echo","see in logs"])
subprocess.run(["ls"])
subprocess.run(["pwd"])

current_directory = os.getcwd()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f"{current_directory}/key.json"

subprocess.run(["printenv"])


