from cs50 import get_string

# Get user input
number = get_string("Number: ")

# Calculate number of digits
length = len(number)

# Determine first pair of digits to identify card
pair_digits = number[0] + number[1]

# Calculate Luhn’s Algorithm
sum = 0
second = False

# Iterate over digits of number
for i in range(length - 1, -1, -1):

    # Convert string into integers
    x = ord(number[i]) - ord('0')

    # Multiplication every second number
    if second == True:
        x *= 2

    # Calculate Sum
    sum += (x // 10)
    sum += (x % 10)

    # Switch first <> second character
    second = not second

valid = ""
# Check if last digit of sum is 0
if sum % 10 == 0:
    valid = True

# American Express: 15-digit, start with 34 or 37, ie: 378282246310005
if length == 15 and pair_digits in ("34", "37"):
    creditor = "AMEX"
# MasterCard: 16-digit, start with 51, 52, 53, 54, or 55, ie: 5555555555554444
elif length == 16 and pair_digits in ("51", "52", "53", "54", "55"):
    creditor = "MASTERCARD"
# Visa: 13- or 16-digit, start with 4, ie: 4003600000000014
elif (length == 13 or length == 16) and pair_digits[0] == "4":
    creditor = "VISA"
else:
    creditor = "INVALID"

# Creating output
if valid == True:
    output = creditor
else:
    output = "INVALID"

print(output)
