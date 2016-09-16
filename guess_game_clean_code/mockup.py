#!/usr/bin/env python3


# http://web.cs.iastate.edu/~honavar/JavaNotes/Notes/chap20/progExercises20.html
#
# Write a program that implements a guessing game:
# 
# The program picks a random number from 1 to 10. Now the user gets three
# guesses. As soon as the user enters the correct number the program writes
# a winning message and exits. If the user fails to enter the correct number
# in three guesses, the program writes a failure message and exits. 
#
# Write a more complicated guessing game, similar to the one in Exercise 3. 
# Now the program is to write "cold" when the guess is 3 or more away from the
# correct answer, "warm" when the guess is 2 away, and "hot" when the guess is 
# 1 away.
#
# Write an even more complicated guessing game. In this version, the full game
# consists of 10 "rounds," where each round is a game like exercise 4. After
# the 10 rounds, the program prints out how many of the 10 rounds were won and
# how many were lost.
#    players who win 7 or fewer rounds are rated as "amateurs,"
#    players who win 8 rounds are rated as "advanced,"
#    players who win 9 rounds are rated as "professionals," and
#    players who win all 10 rounds are rated as "hackers." 


import random


NUM_ROUNDS = 10     # Number of rounds to play
MIN_NUM = 1         # Minimum number to guess
MAX_NUM = 10        # Maximum number to guess
GUESS_TRIES = 3     # Number of allowed tries per round


def print_user_tip(number_to_guess, guess):
    """
    Prints a tip for the user based on the guess.
    
    :param number_to_guess: Random number to guess
    :param guess: User guess
    """

    distance = abs(number_to_guess - guess)

    if distance == 1:
        print('    hot')
    elif distance == 2:
        print('    warm')
    else:
        print('    cold')


def user_guess():
    """
    Reads in the user guess and checks it.
    
    :return: User guess as integer
    :raise ValueError: Raised if user input is invalid
    """
    
    user_input = input('  Enter your guess: ')

    # invalid user input throws ValueError through cast    
    user_input = int(user_input)

    return user_input


def start_round(round_num):
    """
    Completes a round including multiple guesses and tips to the user.
    
    This function uses following constants: MIN_NUM, MAX_NUM, GUESS_TRIES
    
    :param round_num: Round number to display to the user
    :return: Boolean if the user won this round
    """
    
    print('Round {}... Good Luck!'.format(round_num))
    
    number_to_guess = random.randint(MIN_NUM, MAX_NUM)

    valid_tries = 0
    while valid_tries < GUESS_TRIES:
        try:
            guess = user_guess()
            
            if guess == number_to_guess:
                print('Correct')
                return True
            else:
                print_user_tip(number_to_guess, guess)
                
            valid_tries += 1
        except ValueError:
            print('Please enter a number')
    
    print('You lost! The right answer was {}'.format(number_to_guess))
    return False


def print_end_game_stat(rounds_won):
    """
    Prints the end game message to the user.

    This function uses following constants: NUM_ROUNDS
    
    :param rounds_won: Number of rounds won
    """
    
    ranking_prefix_str = None
    ranking_str = None
    percent_won = (rounds_won / NUM_ROUNDS)
    if percent_won >= 1.0:
        ranking_prefix_str = 'a...'
        ranking_str = '...HACKER'
    elif percent_won >= 0.9:
        ranking_prefix_str = 'a...'
        ranking_str = '...PROFESSIONAL'
    elif percent_won >= 0.8:
        ranking_prefix_str = ''
        ranking_str = '...ADVANCED'
    else:
        ranking_prefix_str = 'an...'
        ranking_str = '...AMATEUR'
    
    print('')
    print('{} of {} games won'.format(rounds_won, NUM_ROUNDS))
    print('You... are... {}'.format(ranking_prefix_str))
    print('    {}!'.format(ranking_str))


def start_game():
    """
    Runs a game of NUM_ROUNDS rounds, and prints all user messages.
    
    This function uses following constants: NUM_ROUNDS 
    """
    
    rounds_won = 0
    for round_num in range(NUM_ROUNDS):
        won = start_round(round_num)
        if won:
            rounds_won += 1
    print_end_game_stat(rounds_won)


if __name__ == '__main__':
    start_game()
