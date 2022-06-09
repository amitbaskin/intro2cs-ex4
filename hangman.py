#############################################################
# FILE: hangman.py
# WRITER: Amit Baskin , amit.baskin , 312259013
# EXERCISE : intro2cs ex4 2016-2017
# DESCRIPTION: A program that executes the game "hangman".
#############################################################


import hangman_helper  # a python file contains a few functions for assistance


UNDER_SCORE = '_'

CHAR_A = 97

NUM_OF_LETTERS = 26


def update_word_pattern(word, pattern, letter):
    """
    the function gets a word, the current pattern and a letter as parameters
    and returns an updated pattern that contains the letter
    :param word: the word
    :param pattern: the current pattern
    :param letter: the letter
    :return: updated pattern
    """

    word_characters_lst = list(word)  # unpack the string "word" into a list that contains
    # the character that are in the string
    pattern_characters_lst = list(pattern)  # unpack the string "pattern" into a list that contains
    # the characters that are in the string
    len_lst1 = len(word_characters_lst)

    for i in range(len_lst1):
        if word_characters_lst[i] == letter:  # if the letter is in the word:
            pattern_characters_lst[i] = letter  # insert the letter into the pattern
            # exactly where it is in the word

    updated_pattern = ''.join(pattern_characters_lst)  # transform the list
    # of the characters of the pattern back into a string
    return updated_pattern


def original_pattern(word):
    """
    the function returns a blank note ("_"), multiplied by the length of the given word
    :param word: the given word
    :return: a blank note ("_"), multiplied by the length of the given word
    """

    len_word = len(word)  # the length of the given word
    orig_pattern = [UNDER_SCORE] * len_word
    orig_pattern = ''.join(orig_pattern)
    return orig_pattern


def run_single_game(words_list):
    """
    the function gets a list of words from a file and runs the game itself
    :param words_list: a list of words from a file
    :return: graphic messages in context with the game progress
    """

    error_count = 0  # the game begins with the amount of zero errors
    word = hangman_helper.get_random_word(words_list)  # pick a random
    # word from the list with the assistance of the function 'get_random_word'
    pattern = original_pattern(word)  # name 'pattern' a string of blank notes
    # by calling the function 'original_pattern'
    wrong_guess_lst = []  # the game begins with an empty list of wrong guesses
    chosen_letters = []  # the game begins with an empty list of chosen letters
    msg = hangman_helper.DEFAULT_MSG  # the game begins with a default message: ''

    while (error_count < hangman_helper.MAX_ERRORS) and (pattern != word):
        # while the amount of errors is smaller than the number of
        # maximum errors allowed and the user did not find the word,
        # hence the pattern does not equal to the word

        hangman_helper.display_state(pattern, error_count, wrong_guess_lst, msg)
        # call the function display_state which displays
        # the pattern, the amount of errors made, the list of wrong guesses,
        # and the required message

        user_input = hangman_helper.get_input()  # equals to the input given
        # by the user including the type of input and the input itself
        letter = user_input[1]  # the item in the '1' place in the tuple of the input should be the letter
        input_type = user_input[0]  # the type of the input should be
        # signified in the '0' place in the tuple of the input

        if input_type == hangman_helper.LETTER:  # if the input is a letter

            if (len(letter) != 1) or (not letter.islower()):
                # if the length of the input is different than 1 or if the input is not a letter
                msg = hangman_helper.NON_VALID_MSG
                # the msg is updated to a message that says that the input is not valid

            elif letter in chosen_letters:  # if the letter has already been chosen
                msg = hangman_helper.ALREADY_CHOSEN_MSG + letter  # the msg is updated to a message that says
                #  that the letter has already been chosen and with the letter that was chosen

            elif letter in word:  # if the letter is in the word
                chosen_letters.append(letter)  # add the letter to the list of chosen letters
                pattern = update_word_pattern(word, pattern, letter)  # the letter is to be added to the pattern
                msg = hangman_helper.DEFAULT_MSG  # the msg is updated to the default message

            else:
                chosen_letters.append(letter)  # otherwise, add the letter to the list of the chosen letters
                wrong_guess_lst.append(letter)  # add the letter to the list of wrong guesses
                error_count += 1  # the count of errors gets bigger by one
                msg = hangman_helper.DEFAULT_MSG  # the msg is updated to the default message

        elif input_type == hangman_helper.HINT:  # if the type of the input is a hint
            filtered_words_list = filter_words_list(words_list, pattern, wrong_guess_lst)
            # then the words_list will be filtered

            hint_letter = choose_letter(filtered_words_list, pattern)  # the hint letter will be chosen with the
            # assistance of the function choose_letter, and it will pick from the list 'filtered_words_list'

            msg = hangman_helper.HINT_MSG + hint_letter  # the msg is updated to the hint message plus the letter
            # that was chosen

    if pattern == word:  # if the pattern equals to the word, hence the word was found
        msg = hangman_helper.WIN_MSG  # the msg is updated to the 'winning message'

    else:
        msg = hangman_helper.LOSS_MSG + word  # the msg is updated to the 'loosing message'
        # + the word that was not discovered

    hangman_helper.display_state(pattern, error_count, wrong_guess_lst, msg, ask_play=True)
    # the current state is given and the question whether another game shall be played or not


def run_multiple_games(words_list):
    """
    the function ensures that the game will not be exited while another game shall be played
    :param words_list: a list of words
    :return: a beginning of another game or not if the user chooses not to
    """


    run_game = True

    while run_game:
        run_single_game(words_list)

        user_input = hangman_helper.get_input()

        if user_input[1]:
            run_game = True

        if not user_input[1]:
            run_game = False


def character_in_word(word, pattern):
    """
    the function checks whether or not every letter that in the pattern is in the word exactly in the same place
    :param word: the word to be guessed
    :param pattern: the pattern to be shown
    :return: True if the check is positive and False if negative
    """

    for i in range(len(word)):
        if word[i] != pattern[i] and pattern[i] != UNDER_SCORE:
            return True
    return False


def letter_in_guess_list(word, wrong_guess_list):
    """
    the function checks whether the chosen letter is in the wrong guesses list
    :param word: the word to be guessed
    :param wrong_guess_list: a list of previous wrong guesses
    :return: True if the check is positive and False if negative
    """

    for letter in word:
        if letter in wrong_guess_list:
            return True

    return False


def filter_words_list(words, pattern, wrong_guess_lst):
    """
    the function filters the list of words according to a few conditions
    :param words: the words to be filtered
    :param pattern: the given pattern
    :param wrong_guess_lst: the list of previous wrong guesses
    :return: the filtered list of words
    """

    returned_words_list = []
    for word in words:
        if len(word) != len(pattern):
            continue

        elif character_in_word(word, pattern):
            continue

        elif letter_in_guess_list(word, wrong_guess_lst):
            continue

        else:
            returned_words_list.append(word)

    return returned_words_list


def max_char_count(words, pattern):
    """
    the functions tells which is the most popular letter
    :param words: the given words
    :param pattern: the given pattern
    :return: the most popular letter
    """

    counters = [0] * NUM_OF_LETTERS


    def letter_to_index(letter):
        """
        the function returns the index of the given letter in an alphabet list
        :param letter: the letter to be checked
        :return: the index of the given letter in an alphabet list
        """
        return ord(letter.lower()) - CHAR_A


    def index_to_letter(index):
        """
        thee function returns the letter corresponding to the given index
        :param index: the given index
        :return: the letter corresponding to the given index
        """
        return chr(index + CHAR_A)

    for word in words:
        for letter in word:
            if letter in pattern:
                continue
            counters[letter_to_index(letter)] += 1

    return index_to_letter(counters.index(max(counters)))


def choose_letter(words, pattern):
    """
    the function chooses the letter according to a few conditions
    :param words: a list of words
    :param pattern: the given pattern
    :return: the chosen letter
    """
    letters_in_words = ''.join(words)
    most_popular_letter = max_char_count(letters_in_words, pattern)
    return most_popular_letter


def main():
    """
    the function runs the game itself
    :return: the game running
    """

    words_list = hangman_helper.load_words(file='words.txt')
    run_multiple_games(words_list)


if __name__ == "__main__":  # responsible to start the game
    hangman_helper.start_gui_and_call_main(main)
    hangman_helper.close_gui()
