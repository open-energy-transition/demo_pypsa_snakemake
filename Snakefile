rule calculate_sum:
    input: "input/option.txt"
    output:
        "results/network.txt"
    script:
        "scripts/sum_script.py"

rule prepare_networks:
    input: "network_config/config.txt"
    output: "prepared_networks/done.txt"
    script:
        "scripts/prepare_network.py"

rule solve_networks:
    input: "prepared_networks/done.txt"
    output: "solved_networks/done.txt"
    script:
        "scripts/solve_network.py"

rule try_conda:
    output:
        "env-out/result.txt"
    conda:
        "env-temp-snakemake.yaml"
    script:
        "scripts/conda-use.py"