from cs50 import get_string


def main():

    # Get user input
    text = get_string("Text: ")

    # Counting
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # Calculating index
    index = calculate_index(letters, words, sentences)

    # Creating output
    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


def count_letters(text):
    letters = 0
    # iterate over every char in text
    for letter in text:
        # if unicode char is in a-z of ascii table, count it as a letter
        if ord(letter.lower()) in range(97, 123):
            letters += 1
    return letters


def count_words(text):
    words = 1
    # iterate over every char in text
    for letter in text:
        # if letter is a space, count it as a word
        if letter == " ":
            words += 1
    return words


def count_sentences(text):
    sentences = 0
    # iterate over every char in text
    for letter in text:
        # if letter is .!? count it as sentence
        if letter in (".", "!", "?"):
            sentences += 1
    return sentences


def calculate_index(letters, words, sentences):
    # index = 0.0588 * L - 0.296 * S - 15.8
    L = letters / words * 100
    S = sentences / words * 100
    index = (0.0588 * L) - (0.296 * S) - 15.8
    return round(index)


main()
