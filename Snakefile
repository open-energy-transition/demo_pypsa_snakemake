rule calculate_sum:
    input:
        "input/option.txt"
    output:
        "results/network.txt"
    script:
        "sum_script.py"
