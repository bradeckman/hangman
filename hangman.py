#################################################################
# FILE : hangman.py
# WRITER : Brad Eckman , eckmanbrad , 328958244
# EXERCISE : intro2cse ex4 2020
# DESCRIPTION: A program that executes the Hangman game.
# STUDENTS I DISCUSSED THE EXERCISE WITH: Naftali Arnold
# WEB PAGES I USED: None
# NOTES: run_single_game is a bit of a long function (30 lines or so, I
#        actually refactored into smaller functions and decided to revert it
#        back to the way it was, as I realized the logic is more understandable
#        that way.
#################################################################

from hangman_helper import *

UNDERSCORE = '_'
WELCOME, INVALID_FORMAT, ALREADY_GUESSED, CORRECT_LETTER, INCORRECT_LETTER,\
INCORRECT_WORD, WON, LOST, HINTS, POINTS_LEFT, NO_POINTS_LEFT = range(1, 12)
message_dict = {
    WELCOME: "Welcome the Hangman!",
    INVALID_FORMAT: "That guess is invalid. Try again!",
    ALREADY_GUESSED: "You've already guessed that. Try again!",
    CORRECT_LETTER: "Correct guess!",
    INCORRECT_LETTER: "Incorrect guess!",
    INCORRECT_WORD: "Your guess of the word '{}' is incorrect!",
    WON: "Nice job! You won the game!",
    LOST: "You lost the game! The keyword was: '{}'",
    HINTS: "Hints unlocked! See some possible words in the list above.",
    POINTS_LEFT: "Games played: {}\t\t\tPoints left: {}\n"
                     "Would you like to play again?",
    NO_POINTS_LEFT: "Games played: {}\n"
                    "You've run out of points! Would you like to play again?"
    }


def update_word_pattern(word, pattern, letter):
    """
    Returns the updated pattern given a specific guess
    :param word: The key word that the player must guess
    :param pattern: The uncovered pattern of the word, for the current state
    :param letter: The player's guess
    :return: The updated pattern
    """
    for i in range(len(word)):
        if word[i] == letter:
            # 'Insert' the letter using string concatenation
            pattern = pattern[:i] + letter + pattern[i + 1:]

    return pattern


def game_is_over(keyword, pattern, points):
    """
    Checks if the game is over
    :param keyword: The keyword that the player must guess
    :param pattern: The uncovered pattern of the keyword, for the current state
    :param points: The amount of points currently left
    :return: Boolean value: True if game is over, else - False
    """
    if pattern == keyword or points == 0:
        return True
    else:
        return False


def guess_is_invalid(guess, pattern, wrong_guess_lst):
    """
    Checks whether a guess is invalid, and if so returns appropriate message
    :param guess: The user's guess
    :param pattern: The uncovered pattern of the keyword, for the current state
    :param wrong_guess_lst: The current list of all wrong guesses
    :return: Appropriate message for an invalid guess, else - False
    """
    if len(guess) > 1 or not guess.islower():
        return message_dict[INVALID_FORMAT]
    elif guess in pattern or guess in wrong_guess_lst:
        return message_dict[ALREADY_GUESSED]
    else:
        return False


def guess_in_keyword(guess, keyword):
    """
    Checks if a guess is in the keyword
    :param guess: The user's guess
    :param keyword: The keyword that the player must guess
    :return: Boolean value: True if guess is in keyword, else - False
    """
    if guess in keyword:
        return True
    else:
        return False


def update_points(points, keyword, guess, pattern=None):
    """
    Returns the updated amount of points, based on how many letters were
    uncovered by a specific guess
    :param points: The current amount of points
    :param keyword: The keyword that the player must guess
    :param guess: The user's guess
    :param pattern: (optional) The uncovered pattern of the keyword, for the
           current state (provided only when word is correctly guessed)
    :return: The updated amount of points
    """
    # If word was correctly guessed
    if keyword == guess:
        # Calculate n (guess_rating) based on how many letters were
        # covered before guessing correctly
        guess_rating = pattern.count(UNDERSCORE)
    # Else, letter was correctly guessed
    else:
        # n is based on how many 'guess' letters were uncovered
        guess_rating = keyword.count(guess)
    # n*(n+1)//2
    updated_points = points + (guess_rating * (guess_rating + 1) // 2)

    return updated_points


def won_or_lost(pattern, keyword):
    """
    Return the appropriate message at the end of a game
    :param pattern: The uncovered pattern of the keyword, for the current state
    :param keyword: The keyword that the player must guess
    :return: The message to display to the user
    """
    if pattern == keyword:
        return message_dict[WON]
    else:
        return message_dict[LOST].format(keyword)


def filter_words_list(words, pattern, wrong_guess_lst):
    """
    Filters updated list of words (hints for the user) that can potentially
    be the keyword
    :param words: A list of words
    :param pattern: The uncovered pattern of the keyword, for the
           current state
    :param wrong_guess_lst: The current list of all wrong guesses
    :return: An updated list of words
    """
    hint_words = []

    for word in words:
        # If word isn't the same length as pattern, it can't be the keyword
        if len(word) != len(pattern):
            continue
        # Iterate through corresponding letters of word and pattern
        for word_letter, pattern_letter in zip(word, pattern):
            # If that position has been uncovered, and the corresponding
            # letters don't match, it can't be keyword
            if pattern_letter != UNDERSCORE and word_letter != pattern_letter:
                break
            # If there is letter that is known to be wrong, it can't be keyword
            if word_letter in wrong_guess_lst:
                break
            # Filter out words that have instances of a letter that contradicts
            # our findings of a previous correct guess
            if word_letter in pattern and word_letter != pattern_letter:
                break
        # If there was no break at the end of iteration, word has passed tests
        else:
            hint_words.append(word)

    return hint_words


def handpick(hints):
    """
    Handpicks certain words out of potential hints
    :param hints: The current hint list
    :return: A select list of hints
    """
    if len(hints) > HINT_LENGTH:
        # Initialize list of length HINT_LENGTH of appropriate indexes based
        # on algorithm specified in exercise documentation
        indexes = [i * len(hints) // HINT_LENGTH for i in range(HINT_LENGTH)]
        # Access appropriate words from hints
        minimized_hints = [hints[index] for index in indexes]
        return minimized_hints

    else:
        return hints


def letter_chosen(guess, keyword, pattern, wrong_guess_lst, points):
    """
    Gameplay logic for when user has guessed a letter, updates relevant
    parameters.
    :param guess: The user's guess
    :param keyword: The keyword that the player must guess
    :param pattern: The uncovered pattern of the keyword, for the
           current state
    :param wrong_guess_lst: The current list of all wrong guesses
    :param points: The current amount of points
    :return: Updated values for msg, pattern and points
    """
    # Check if invalid char, or if already guessed letter
    if guess_is_invalid(guess, pattern, wrong_guess_lst):
        msg = guess_is_invalid(guess, pattern, wrong_guess_lst)
    # Letter is a valid guess
    else:
        points -= 1
        # If guessed a correct letter, update pattern, points and msg
        if guess_in_keyword(guess, keyword):
            points = update_points(points, keyword, guess)
            pattern = update_word_pattern(keyword, pattern, guess)
            msg = message_dict[CORRECT_LETTER]
        # Else, update msg and add guess to wrong guess list
        else:
            wrong_guess_lst.append(guess)
            msg = message_dict[INCORRECT_LETTER]

    return msg, pattern, points


def word_chosen(guess, keyword, pattern, points, msg):
    """
    Gameplay logic for when user has guessed a word, updates relevant
    parameters.
    :param guess: The user's guess
    :param keyword: The keyword that the player must guess
    :param pattern: The uncovered pattern of the keyword, for the
           current state
    :param points: The current amount of points
    :param msg: The current message to be displayed
    :return: Updated values for msg, pattern and points
    """
    points -= 1
    # If user correctly guessed the keyword, update pattern and points
    if guess == keyword:
        points = update_points(points, keyword, guess, pattern)
        pattern = keyword
    # Else, update msg and reiterate
    else:
        msg = message_dict[INCORRECT_WORD].format(guess)

    return msg, pattern, points


def hint_chosen(points, words_list, pattern, wrong_guess_lst):
    """
    Gameplay logic for when user has selected a hint, updates relevant
    parameters.
    :param points: The current amount of points
    :param words_list: A list of possible keywords
    :param pattern: The uncovered pattern of the keyword, for the
           current state
    :param wrong_guess_lst: The current list of all wrong guesses
    :return: Updated values for msg and points
    """
    points -= 1
    # Get all relevant hints, minimize if need be
    hints = handpick(filter_words_list(words_list, pattern,
                                       wrong_guess_lst))
    show_suggestions(hints)
    msg = message_dict[HINTS]

    return msg, points


def run_single_game(words_list, points):
    """
    Runs a single game of hangman
    :param words_list: A list of possible keywords
    :param points: The amount of points with which the player will start the
           current game
    :return: The updated amount of points after playing one game
    """
    # Set and initialize parameters to start off the game
    keyword = get_random_word(words_list)
    pattern = UNDERSCORE * len(keyword)
    msg = message_dict[WELCOME]
    wrong_guess_lst = []

    # Continue to iterate as long as the game is not over
    while not game_is_over(keyword, pattern, points):
        # Display current state and get input from user
        display_state(pattern, wrong_guess_lst, points, msg)
        guess_type, guess = get_input()  # unpack into descriptive variables

        # Check the type of input of the user, and continue gameplay sequence
        # by sending to the appropriate function, while updating the relevant
        # parameters
        if guess_type == LETTER:
            msg, pattern, points = letter_chosen(guess, keyword, pattern,
                                                 wrong_guess_lst, points)
        elif guess_type == WORD:
            msg, pattern, points = word_chosen(guess, keyword, pattern,
                                               points, msg)
        elif guess_type == HINT:
            msg, points = hint_chosen(points, words_list, pattern,
                                      wrong_guess_lst)

    # Update msg appropriately and display
    msg = won_or_lost(pattern, keyword)
    display_state(pattern, wrong_guess_lst, points, msg)

    return points


def main():
    """ The main function for operating the hangman program """
    # Initialize words, points and games played counter
    words_list = load_words()
    points_in_game = POINTS_INITIAL
    games_played = 0

    while True:
        # Run a single game - capture amount of points left and record 1
        # game played
        points_in_game = run_single_game(words_list, points_in_game)
        games_played += 1
        # If user has points left from last game, he can play again (his points
        # and number of games played being passed over), or opt out
        if points_in_game > 0:
            if play_again(message_dict[POINTS_LEFT].format(games_played,
                                                           points_in_game)):
                continue
            else:
                return None
        # Else, user doesn't have points left from last game, he can play again
        # (his points and number of games played being reset), or opt out
        else:
            if play_again(message_dict[NO_POINTS_LEFT].format(games_played)):
                games_played = 0
                points_in_game = POINTS_INITIAL
                continue
            else:
                return None


if __name__ == "__main__":
    main()
