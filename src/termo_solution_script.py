#!/usr/bin/env python3
#coding=utf-8

#includes
import numpy as np
import pandas as pd
from evaluation import evaluate,remove_wrong_words,greedy_action

# constants
TERMO_POSSIBLE_WORDS_PATH = "docs/termo/all_possibles_words.txt"
TERMO_ALL_WORDS_PATH = "docs/termo/all_words.txt"
TERMO_INITIAL_SOLUTION_PATH = "results/termo/initial_rank_termo_words.csv"

def generate_initial_evaluate_list():
    with open(TERMO_POSSIBLE_WORDS_PATH) as f:
        possi_words_list = [line.rstrip('\n') for line in f]
    possi_words = np.array(possi_words_list)

    with open(TERMO_ALL_WORDS_PATH) as f:
        all_words_list = [line.rstrip('\n') for line in f]
    all_words = np.array(all_words_list)
    all_words = np.append(all_words,possi_words)

    # tranform dataframe to csv file#
    rank_words = evaluate(possi_words,all_words)
    rank_words = rank_words.sort_values(by=['good_word_prob'],ascending=False) #sort values
    rank_words.to_csv(TERMO_INITIAL_SOLUTION_PATH,index=False)
    print(rank_words) 

def main():
    with open(TERMO_POSSIBLE_WORDS_PATH) as f:
        possible_solutions_list = [line.rstrip('\n') for line in f]
    possible_solutions = np.array(possible_solutions_list)

    with open(TERMO_ALL_WORDS_PATH) as f:
        all_words_list = [line.rstrip('\n') for line in f]
    all_words = np.array(all_words_list)
    all_words = np.append(all_words,possible_solutions)
    
    rank_words = pd.read_csv(TERMO_INITIAL_SOLUTION_PATH)['word']
    colors = [0]*5

    guess = rank_words[0]
    while(colors != [2]*5):
        print("guess: ",guess)
        feedback = input("result(0 -> black | 1 -> yellow | 2 -> green):")
        colors = [int(letter_feedback) for letter_feedback in feedback]

        possible_solutions,all_words = remove_wrong_words(guess,colors,possible_solutions,all_words)
        rank_words = evaluate(possible_solutions,all_words).sort_values(by=['good_word_prob'],ascending=False)['word']
        guess = greedy_action(possible_solutions, rank_words)
    print("easy peasy")

if __name__ == "__main__":
    try:
        #test_evaluate
        #takes almost 3 minutes
        #generate_initial_evaluate_list()

        main()
    except KeyboardInterrupt:
        print("\nBetter luck next time")