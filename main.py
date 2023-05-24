# main.py

import sys
import pandas as pd
from anytree import Node, RenderTree
from dataclasses import dataclass


# Get SLR parse table
parse_table = pd.read_excel(io='SLR_table.xlsx', sheet_name='SLR_parse_table', index_col=0)

# Get production table
production_table = pd.read_excel(io='SLR_table.xlsx', sheet_name='Productions', index_col=0, usecols='A,C:E')


def main(input_file):
    # Get tokens from input file and tokenize
    with open(input_file, 'r') as f:
        contents = f.read()

    # Split contents by whitespace to get tokens
    tokens = contents.split()

    # Process tokens
    # Replace with actual processing logic
    for token in tokens:
        print(token)

    # print(parse_table)
    # Initialize stack and buffer
    stack = [0]
    buffer = tokens + ["$"]
    node_stack = []

    # Parsing
    while True:
        # Get current state and next input symbol
        current_state = stack[-1]
        next_input_symbol = buffer[0]

        # Get action from SLR parsing table
        action = parse_table.loc[current_state, next_input_symbol]

        if action == "acc":  # Accept
            print("Accept")
            for pre, _, node in RenderTree(node_stack[-1]):
                print(f'{pre}{node.name}')
            break

        action_type = action[0]
        action_number = int(action[1:])

        if action_type == 's':  # Shift
            shift_func(action_number, stack, buffer, node_stack)
        elif action_type == 'r':  # Reduce
            reduce_func(action_number, stack, node_stack)
        else:  # Error
            print("Parsing failed.")
            # print(f, "{next_input_symbol} has error.")
            break


def shift_func(action_number, stack, buffer, node_stack):
    # Append the state number to the stack
    stack.append(action_number)

    node_stack.append(Node(buffer[0]))

    # Move the spliter
    # Remove the first symbol from the buffer
    buffer.pop(0)


def reduce_func(action_number, stack, node_stack):
    # Get the production rule to be reduced
    production_RHS = production_table.loc[action_number, 'RHS']
    production_LHS = production_table.loc[action_number, 'LHS']

    # Get the production's length to pop states from stack
    production_len = len(production_RHS.split())
    if production_RHS == "''":
        production_len = 0

    parent = Node(production_LHS)

    # Remove state from the stack
    if production_len != 0:
        for _ in range(production_len):
            stack.pop()
            node_stack[-1].parent = parent
            node_stack.pop()

    node_stack.append(parent)

    next_state = parse_table.loc[stack[-1], production_LHS]
    stack.append(next_state)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <input_file>")
    else:
        main(sys.argv[1])
