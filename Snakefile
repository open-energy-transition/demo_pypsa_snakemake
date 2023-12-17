rule calculate_sum:
    input:
        "input/option.txt"
    output:
        "results/network.txt"
    script:
        "sum_script.py"


rule prepare_networks:
    input:
        "network_config/config.txt"
    output:
        directory("prepared_networks/")
    script:
        "prepare_network.py"

rule solve_networks:
    input:
        rules.prepare_networks.output
    output:
        directory("solved_networks/")
    script:
        "solve_network.py"



