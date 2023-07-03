import binascii

def read_csv(file_path):
    data = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip().split(',')
            data[line[0]] = line[1]
    return data

def read_file_as_hex(file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
        hex_data = binascii.hexlify(file_data).decode('utf-8')
    return hex_data

def file_carving(csv_file_path, uncarved_file_path):
    csv_data = read_csv(csv_file_path)
    hex_data = read_file_as_hex(uncarved_file_path)
    file_number = 0

    fragment_start = 0
    while fragment_start < len(hex_data):
        found_header = False
        found_extension = ""
        header_length=0
        for header, extension in csv_data.items():
            header_length = len(header)
            if hex_data.startswith(header, fragment_start):
                found_header = True
                found_extension = extension
                break
        
        if found_header:
            file_number += 1
            fragment = hex_data[fragment_start:]
            if len(fragment) % 2 != 0:
                fragment_temp = "0" + fragment
            else: 
                fragment_temp = fragment
                
            extracted_bytes = binascii.unhexlify(fragment_temp)
            # Save extracted bytes to a file
            filename = f"extracted_file_{file_number}.{found_extension}"
            with open(filename, 'wb') as extracted_file:
                extracted_file.write(extracted_bytes)
            fragment_start = fragment_start+ header_length 
        else:
            fragment_start += 1
# test
csv_file_path = 'HeadersCSV.csv'
uncarved_file_path = 'fileCarving2'
file_carving(csv_file_path, uncarved_file_path)