# main.py

import sys
import pandas as pd
from anytree import Node, RenderTree

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

    # Initialize state stack and buffer
    state_stack = [0]
    buffer = tokens + ["$"]

    # Initialize node stack
    node_stack = []

    # Count number of input token
    cnt = 1

    # Parsing
    while True:
        # Get current state and next input symbol
        current_state = state_stack[-1]
        next_input_symbol = buffer[0]

        # Get action from SLR parsing table
        action = parse_table.loc[current_state, next_input_symbol]

        # If action is None or NaN
        if pd.isnull(action):
            print(f"REJECT!! Error detected at token{cnt} : {next_input_symbol}")
            break

        if action == "acc":  # Accept
            print("ACCEPT!!")
            print("--------------[Parse Tree]--------------")
            # Print Parse Tree
            for pre, _, node in RenderTree(node_stack[-1]):
                print(f'{pre}{node.name}')
            break

        action_type = action[0]
        action_number = int(action[1:])

        if action_type == 's':  # Shift
            shift_func(action_number, state_stack, buffer, node_stack)
            cnt += 1
        elif action_type == 'r':  # Reduce
            reduce_func(action_number, state_stack, node_stack)
        else:  # Error
            print("Parsing failed. Check SLR Parsing Table.")
            break


def shift_func(action_number, state_stack, buffer, node_stack):
    # Append the state number to the stack
    state_stack.append(action_number)

    # Append the current node to the stack
    node_stack.append(Node(buffer[0]))

    # Move the spliter
    # Remove the first symbol from the buffer
    buffer.pop(0)


def reduce_func(action_number, state_stack, node_stack):
    # Get the production rule to be reduced
    production_RHS = production_table.loc[action_number, 'RHS']
    production_LHS = production_table.loc[action_number, 'LHS']
    production_len = production_table.loc[action_number, 'n']

    # Create a new parent node
    parent = Node(production_LHS)

    # Add epsilon node if RHS is ''
    if production_RHS == "''":
        Node("ε", parent=parent)

    # Remove state from the state_stack and link child nodes with parent node
    for _ in range(production_len):
        if state_stack or node_stack:  # Check if the stack is not empty
            state_stack.pop()
            node_stack[-1].parent = parent
            node_stack.pop()
        else:
            print("Error: Trying to pop from an empty stack!", file = sys.stderr)
            return

    # Append current parent node to the stack (current parent node also can be child node)
    node_stack.append(parent)

    if not state_stack:  # Check if the stack is empty
        print("Error: Trying to pop from an empty stack!", file=sys.stderr)
        return

    # GOTO Action
    next_state = parse_table.loc[state_stack[-1], production_LHS]
    state_stack.append(next_state)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <input_file>")
    else:
        main(sys.argv[1])
