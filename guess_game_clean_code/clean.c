#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

static const int NUM_ROUNDS = 10;       /**< Number of rounds to play */
static const int MIN_NUM = 1;           /**< Minimum number to guess */
static const int MAX_NUM = 10;          /**< Maximum number to guess */
static const int GUESS_TRIES = 3;       /**< Number of allowed tries per round */


/**
 * Prints a tip for the user based on the guess.
 *
 * @param number_to_guess Random number to guess
 * @param guess User guess
 */
void print_user_tip(int number_to_guess, int guess)
{
    int distance = abs(number_to_guess - guess);

    if (distance == 1)
    {
        printf("    hot\n");
    }
    else if (distance == 2)
    {
        printf("    warm\n");
    }
    else
    {
        printf("    cold\n");
    }
}


/**
 * Reads in the user guess and checks it.
 *
 * @return User guess as integer
 */
int user_guess(void)
{
//    int user_input = 0;
//    int ret;
//
//    ret = scanf("%u", &user_input);
//    while (ret != 1)
//    {
//        printf("Please enter a number\n");
//        ret = scanf("%u", &user_input);
//    }
//
//    printf("user_input: %d   ret: %d\n", user_input, ret);
//
//    return user_input;

    /* TODO: Fix this input stuff (sorry, wasn't in the mood for bug searching) */
    return 5;
}


/**
 * Completes a round including multiple guesses and tips to the user.
 *
 * @note This function uses following constants: MIN_NUM, MAX_NUM, GUESS_TRIES
 *
 * @param round_num Round number to display to the user
 * @return Boolean if the user won this round
 */
bool start_round(int round_num)
{
    int number_to_guess = rand() % MAX_NUM;   // TODO: limit num
    int guess;

    printf("Round %d... Good Luck!\n", round_num);

    for (int i = 0; i < GUESS_TRIES; i++)
    {
        guess = user_guess();
        if (guess == number_to_guess)
        {
            printf("Correct!\n");
            return true;
        }
        else
        {
            print_user_tip(number_to_guess, guess);
        }
    }

    printf("You lost! The right answer was %d\n", number_to_guess);
    return false;
}


/**
 * Prints the end game message to the user.
 *
 * @note This function uses following constants: NUM_ROUNDS
 *
 * @param rounds_won Number of rounds won
 */
void print_end_game_stat(int rounds_won)
{
    float percent_won = ((float) rounds_won / (float) NUM_ROUNDS);

    printf("\n");
    printf("%d of %d games won\n", rounds_won, NUM_ROUNDS);

    if (percent_won >= 1.0)
    {
        printf("You... are... a...\n");
        printf("    ...HACKER!\n");
    }
    else if (percent_won >= 0.9)
    {
        printf("You... are... a...\n");
        printf("    ...PROFESSIONAL!\n");
    }
    else if (percent_won >= 0.8)
    {
        printf("You... are...\n");
        printf("    ...ADVANCED!\n");
    }
    else
    {
        printf("You... are... an...\n");
        printf("    ...AMATEUR!\n");
    }
}


/**
 * Runs a game of NUM_ROUNDS rounds, and prints all user messages.
 *
 * @note This function uses following constants: NUM_ROUNDS
 */
int main(void)
{
    int rounds_won = 0;
    bool won;

    srand(time(NULL));

    for (int round_num = 0; round_num < NUM_ROUNDS; round_num++)
    {
        won = start_round(round_num);
        if (won)
        {
            rounds_won++;
        }
    }

    print_end_game_stat(rounds_won);
}
