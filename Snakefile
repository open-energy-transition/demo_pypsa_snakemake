rule calculate_sum:
    input:
        "input/option.txt"
    output:
        "results/network.txt"
    script:
        "scripts/sum_script.py"


rule prepare_networks:
    input:
        "network_config/config.txt"
    output:
        directory("prepared_networks/")
    script:
        "scripts/prepare_network.py"

rule solve_networks:
    input:
        rules.prepare_networks.output
    output:
        directory("solved_networks/")
    script:
        "scripts/solve_network.py"



