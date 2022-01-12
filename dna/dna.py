import csv
import sys


def main():

    # TODO: Check for command-line usage
    # Ensure correct usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py FILENAME.csv FILENAME.txt")

    # TODO: Read database file into a variable
    with open(sys.argv[1], "r") as file_csv:
        database = csv.DictReader(file_csv)
        str_db = list(database.fieldnames)
        str_db.remove("name")
        #
        reader = csv.reader(file_csv)
        # headers = next(reader)
        data = list(reader)
    # print(data)

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as file_txt:
        sequence = file_txt.read()

    # TODO: Find longest match of each STR in DNA sequence
    results = []  # {}
    for str in str_db:
        results.append(longest_match(sequence, str))
        #results[str] = longest_match(sequence, str)
    # print(results)

    # TODO: Check database for matching profiles
    for row in data:
        count = 0
        for i in range(1, len(row)):
            if int(row[i]) == results[i-1]:
                count += 1
            if count == len(row) - 1:
                print(row[0])
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
