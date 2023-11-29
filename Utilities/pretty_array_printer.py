def print_checkpoints(array, level_name: str):
    print("-------------------------------")
    print(f"Checkpoints for level: {level_name}")
    # Replace -1 with empty strings
    array = [['' if cell == -1 else cell for cell in row] for row in array]

    # Calculate the maximum width of the elements in each column
    col_widths = [max(len(str(cell)) for cell in column) for column in zip(*array)]

    for row in array:
        print(" ".join(f"{str(cell).rjust(width)}" for cell, width in zip(row, col_widths)))
    print("-------------------------------")