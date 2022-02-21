#!/usr/bin/env python3
#coding=utf-8

import numpy as np
import pandas as pd

WORDLE_POSSIBLE_WORDS_PATH = "docs/wordle/all_possibles_words.txt"
WORDLE_ALL_WORDS_PATH = "docs/wordle/all_words.txt"

WORDLE_GREEN_COLOR_SIMBOL = '2'
WORDLE_YELLOW_COLOR_SIMBOL = '1'

def evaluate_step(word,solutions):
    right_pos,in_word = 0,0

    for solution in solutions:
        is_in_right_pos,is_char_in_word = 0,0
        solution_list = list(solution) 
        for (i,char_word) in enumerate(word):
            if(char_word == solution_list[i]):
                is_in_right_pos = 1
                solution_list[i] = WORDLE_GREEN_COLOR_SIMBOL
            elif(char_word in solution_list):
                is_char_in_word = 1
                pos_char_word = solution_list.index(char_word)
                solution_list[pos_char_word] = WORDLE_YELLOW_COLOR_SIMBOL
            print(word)
            print(solution_list)
        right_pos += is_in_right_pos
        in_word += is_char_in_word
    exist_right_in_word = right_pos + in_word 
    return right_pos,in_word,exist_right_in_word

def evaluate():
    with open(WORDLE_POSSIBLE_WORDS_PATH) as f:
        possi_words_list = [line.rstrip('\n') for line in f]
    possi_words = np.array(possi_words_list)

    with open(WORDLE_ALL_WORDS_PATH) as f:
        all_words_list = [line.rstrip('\n') for line in f]
    all_words = np.array(all_words_list)

    rank_words = pd.DataFrame(columns=['word','right_pos','exist_in_word','exist_right_in_word'])

    for word in all_words:
        eright_pos,ein_word,has_color = evaluate_step(word,possi_words)
        rank_words = rank_words.append({'word':word,'right_pos':eright_pos,'exist_in_word':ein_word,'exist_right_in_word':has_color}, ignore_index=True)

    # tranform dataframe to csv file
    rank_words = rank_words.sort_values(by=['exist_right_in_word'],ascending=False)
    rank_words.to_csv('rank_wordle_words.csv',index=False)

if __name__ == "__main__":
    try:
        evaluate()
    except KeyboardInterrupt:
        print("\nBetter luck next time")