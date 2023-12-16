rule calculate_sum:
    input:
        "input/option.txt"
    output:
        "results/output.txt"
    script:
        "sum_script.py"
