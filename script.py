import csv
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Union, Tuple

from formatter import FormatterType1
from formatter import FormatterType2
from formatter import FormatterType3


formatter_type = {
    'TYPE_1': FormatterType1,
    'TYPE_2': FormatterType2,
    'TYPE_3': FormatterType3,
}

def start_parser() -> argparse.Namespace:
    """
    Parse arguments for the script
    usage: script.py [-h] [-o OUTPUT_FILE] input_files [input_files ...]
    """
    parser = argparse.ArgumentParser() 
    
    parser.add_argument("input_files", nargs="+", type=str)
    parser.add_argument("-o", "--output_file", type=str, default="merged.csv", help='Filename for storing unified data')
     
    args = parser.parse_args()     
    return args

def read_format(format_file: str) -> dict:
    """
    Reads the various types of data formats from json file
    """    
    with open(format_file) as json_file:
        return json.load(json_file)

def read_csv(file_name: str) -> Tuple[set, List[dict]]:
    """
    Reads the csv file to extract column names and row data
    """
    with open(file_name) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        field_keys, row_list = '', []        
        
        for row in csv_reader:
            if line_count == 0:
                field_keys = set(row.keys())
                line_count += 1
                    
            row_list.append(row)
        
        return field_keys, row_list

def identify_file_format(format_type, input_formats: dict) -> Union[str, None]:
    """
    Identifies the format of the input file
    """
    for key, value in input_formats.items():
        if set(value['fields'].keys()) == format_type:
            return key
    
    return None
    
def convert_to_output_format(data: List[dict], format: str) -> List[dict]:
    """
    Converts the data to the expected output format
    """
    formatter = formatter_type[format]
    output_list = []

    for item in data:
        output_list.append(formatter(item).output)

    return output_list

def sort_output(output_list: List[dict]) -> List[dict]:
    """ 
    Sorts the rows on the date field in ascending order
    """
    output_list.sort(key=lambda item: datetime.strptime(item['date'], '%d-%m-%Y'))
    return output_list

def write_output_csv(merge_file_name: str, rows: List[dict]) -> None:
    """
    Writes the rows to the output file 
    """
    with open(merge_file_name, mode='w') as merge_file:
        writer = csv.DictWriter(merge_file, fieldnames=rows[0].keys())
        writer.writeheader()

        for row in rows:
            writer.writerow(row)

        print(f'Unified output written to file {merge_file_name}')
    

def main() -> None:
    """
    Entry point to the script
    """
    args = start_parser()

    available_input_formats = read_format('input_format.json')

    unified_output = []

    for file_name in args.input_files:        
        if Path(file_name).is_file():
            format_type, row_list = read_csv(file_name)
            format_key = identify_file_format(format_type, available_input_formats)

            if format_key:
                output = convert_to_output_format(row_list, format_key)
                unified_output.extend(output)
            else:
                print(f'Error: Could not identify type for {file_name}')   
                 
        else:
            print(f'Error: File {file_name} does not exists')

    sorted_output = sort_output(unified_output)

    write_output_csv(args.output_file, sorted_output)

if __name__ == '__main__':
    main()

