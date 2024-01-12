# from snakemake.remote.GS import RemoteProvider as GSRemoteProvider
# GS = GSRemoteProvider()

rule calculate_sum:
    input: "input/option.txt"
    # input: GS.remote("remotesnake/options.txt")
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

rule calculate_sum_cloud:
    input:
        "input/option.txt"
    output:
        "results/network.txt"
    shell: "bash vm_stuff/runner.sh {input} {output} calculate_sum"

rule prepare_networks_cloud:
    input: "network_config/config.txt"
    output: "prepared_networks/done.txt"
    shell: "bash runner.sh {input} {output} prepare_networks"

rule solve_networks_cloud:
    input: "prepared_networks/done.txt"
    output: "solved_networks/done.txt"
    shell: "bash runner.sh {input} {output} solve_networks"