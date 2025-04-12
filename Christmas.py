def christmas_tree(ornament, leaf, height):
    for i in range(height):
        leaves = i * 2 + 1

        row = ""
        for j in range(leaves):
            if j % 2 == 0:
                row += leaf
            else:
                row += ornament

        spaces = height - i - 1
        print(" " * spaces + row)

christmas_tree("0", "*", 3)