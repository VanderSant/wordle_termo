#!/usr/bin/env python3
#coding=utf-8

import numpy as np
import pandas as pd

WORDLE_POSSIBLE_WORDS_PATH = "docs/wordle/all_possibles_words.txt"
WORDLE_ALL_WORDS_PATH = "docs/wordle/all_words.txt"

def evaluate_step(word,all_words):
    right_pos,in_word = 0,0
    for word_i in all_words:
        is_in_right_pos,is_char_in_word = 0,0
        for (i,char_word) in enumerate(word):
            if(char_word == word_i[i]):
                is_in_right_pos = 1
            elif(char_word in word_i):
                is_char_in_word = 1
        right_pos += is_in_right_pos
        in_word += is_char_in_word
    good_option = right_pos + in_word 
    return right_pos,in_word,good_option

def evaluate():
    with open(WORDLE_POSSIBLE_WORDS_PATH) as f:
        possi_words_list = [line.rstrip('\n') for line in f]
    possi_words = np.array(possi_words_list)

    with open(WORDLE_ALL_WORDS_PATH) as f:
        all_words_list = [line.rstrip('\n') for line in f]
    all_words = np.array(all_words_list)

    rank_words = pd.DataFrame(columns=['word','right_pos','has_in','good_option'])

    for word in all_words:
        eright_pos,ein_word,has_color = evaluate_step(word,possi_words)
        rank_words = rank_words.append({'word':word,'right_pos':eright_pos,'has_in':ein_word,'good_option':has_color}, ignore_index=True)

    # tranform dataframe to csv file
    rank_words = rank_words.sort_values(by=['good_option'],ascending=False)
    rank_words.to_csv('rank_wordle_words.csv',index=False)

if __name__ == "__main__":
    try:
        evaluate()
    except KeyboardInterrupt:
        print("\nBetter luck next time")