# main.py

import sys
import pandas as pd
from dataclasses import dataclass

def main(input_file):
    # Get tokens from input file and tokenize
    with open(input_file, 'r') as f:
        contents = f.read()

    # Split contents by whitespace to get tokens
    tokens = contents.split()

    # # Process tokens
    # for token in tokens:
    #     print(token)  # Replace with actual processing logic

    # Get production table
    production_table = pd.read_excel(io='SLR_table.xlsx', sheet_name='Productions', index_col=0, usecols='A,C:E')

    # Get SLR parse table
    parse_table = pd.read_excel(io='SLR_table.xlsx', sheet_name='SLR_parse_table', index_col=0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
    else:
        main(sys.argv[1])
