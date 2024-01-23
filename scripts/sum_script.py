import sys
import subprocess
import os

input_file = snakemake.input[0]
output_file = snakemake.output[0]

with open(input_file, 'r') as file:
    numbers = [int(line.strip()) for line in file.readlines()]
total = sum(numbers)

with open(output_file, 'w') as file:
    file.write(str(total))
    
# for _ in range(100):
#         print("doing")
#         time.sleep(1)

subprocess.run(["echo","bbbcjebc"])
subprocess.run(["ls"])
subprocess.run(["pwd"])

current_directory = os.getcwd()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f"{current_directory}/key.json"

subprocess.run(["printenv"])


