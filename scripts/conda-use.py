import arrow
import phonenumbers

output_file = snakemake.output[0]

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
        file.write(f"Current Time: {current_time.format('YYYY-MM-DD HH:mm:ss')}")
        
main()
