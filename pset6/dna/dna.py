import csv
import sys


def main():
    # TODO: Check for command-line usage
    # Ensure correct usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py FILENAME.csv FILENAME.txt")

    # TODO: Read database file into a variable
    # Reading the str database file into the headers[] list and data{} dict
    with open(sys.argv[1], "r") as file_csv:
        reader = csv.DictReader(file_csv)
        headers = list(reader.fieldnames)
        data = list(reader)

    # TODO: Read DNA sequence file into a variable
    # Reading the sequence file with the .read() method and storing into the sequence variable
    with open(sys.argv[2], "r") as file_txt:
        sequence = file_txt.read()

    # TODO: Find longest match of each STR in DNA sequence
    # Generating the count of every str with the longest_match function into the results[] list
    results = []
    for str in headers:
        results.append(longest_match(sequence, str))

    # TODO: Check database for matching profiles
    # Iterating over every row in the data and then iterating over every cell in the row to
    # see if it matches the results[] list. If all cells match set output to this person.
    output = "No match"
    for row in data:
        count = 0
        for i in range(1, len(row)):
            if int(row[headers[i]]) == results[i]:
                count += 1
            if count == len(row) - 1:
                output = row[headers[0]]

    # Create output
    print(output)
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
