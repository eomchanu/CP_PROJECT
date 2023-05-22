# main.py

import sys


def main(input_file):
    with open(input_file, 'r') as f:
        contents = f.read()

    # Split contents by whitespace to get tokens
    tokens = contents.split()

    # Process tokens
    for token in tokens:
        print(token)  # Replace with actual processing logic


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
    else:
        main(sys.argv[1])
