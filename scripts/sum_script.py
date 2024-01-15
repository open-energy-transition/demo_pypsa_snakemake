import sys

input_file = snakemake.input[0]
output_file = snakemake.output[0]

with open(input_file, 'r') as file:
    numbers = [int(line.strip()) for line in file.readlines()]
total = sum(numbers)

with open(output_file, 'w') as file:
    file.write(str(total))
    

import arrow
import phonenumbers

def main():
    # Using Arrow to get the current time
    current_time = arrow.now()
    print(f"Current Time: {current_time.format('YYYY-MM-DD HH:mm:ss')}")

    # Using Phonenumbers to parse and format a phone number
    sample_phone = "+1-202-555-0173"
    parsed_phone = phonenumbers.parse(sample_phone)
    formatted_phone = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    print(f"Formatted Phone Number: {formatted_phone}")
    with open(output_file, 'w') as file:
        file.write(str(formatted_phone))


main()