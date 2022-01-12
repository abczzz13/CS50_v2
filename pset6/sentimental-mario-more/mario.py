from cs50 import get_int

# Get user input
height = 0
while height not in range(1, 9):
    height = get_int("Height: ")

for line in range(1, height + 1):
    print(((height - line) * " ") + (line * "#") +
          "  " + (line * "#"))
