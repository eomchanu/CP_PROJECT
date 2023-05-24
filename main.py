# main.py

import sys
import pandas as pd

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
    state_stack = [0]
    buffer = tokens + ["$"]

    # Parsing
    while True:
        # Get current state and next input symbol
        current_state = state_stack[-1]
        next_input_symbol = buffer[0]

        # Get action from SLR parsing table
        action = parse_table.loc[current_state, next_input_symbol]

        # If action is None or NaN
        if pd.isnull(action):
            # update bug report soon
            print(f"REJECT!! Can't look up [{current_state},{next_input_symbol}] on SLR parsing table.")
            break

        print(action)

        if action == "acc":  # Accept
            print("Accept")
            # add parse tree soon
            break

        action_type = action[0]
        action_number = int(action[1:])

        if action_type == 's':  # Shift
            shift_func(action_number, state_stack, buffer)

        elif action_type == 'r':  # Reduce
            reduce_func(action_number, state_stack)
        else:  # Error
            print("Parsing failed. Check SLR Parsing Table.")
            break


def shift_func(action_number, state_stack, buffer):
    # Append the state number to the stack
    state_stack.append(action_number)

    # Move the spliter
    # Remove the first symbol from the buffer
    buffer.pop(0)


def reduce_func(action_number, state_stack):
    # Get the production rule to be reduced
    production_LHS = production_table.loc[action_number, 'LHS']
    production_len = production_table.loc[action_number, 'n']


    # Reduce
    # Remove state from the stack
    for _ in range(production_len):
        state_stack.pop()

    # GOTO func.
    next_state = parse_table.loc[state_stack[-1], production_LHS]
    state_stack.append(next_state)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <input_file>")
    else:
        main(sys.argv[1])
