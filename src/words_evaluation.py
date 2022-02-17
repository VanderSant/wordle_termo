#!/usr/bin/env python3
#coding=utf-8

import numpy as np
import pandas as pd

WORDLE_POSSIBLE_WORDS_PATH = "docs/wordle/all_possibles_words.txt"
WORDLE_ALL_WORDS_PATH = "docs/wordle/all_words.txt"

def evaluate_step(word,all_words):
    value = 0
    for word_i in all_words:
        for (i,char_word) in enumerate(word):
            if(char_word == word_i[i]):
                value += 2
            elif(char_word in word_i):
                value += 1
    return value

def evaluate():
    with open(WORDLE_POSSIBLE_WORDS_PATH) as f:
        possi_words_list = [line.rstrip('\n') for line in f]
    possi_words = np.array(possi_words_list)

    with open(WORDLE_ALL_WORDS_PATH) as f:
        all_words_list = [line.rstrip('\n') for line in f]
    all_words = np.array(all_words_list)

    rank_words = pd.DataFrame(columns=['word','evaluate'])

    for word in possi_words:
        eval_w = evaluate_step(word,all_words)
        rank_words = rank_words.append({'word':word,'evaluate': eval_w}, ignore_index=True)

    # tranform dataframe to csv file
    rank_words = rank_words.sort_values(by=['evaluate'],ascending=False)
    rank_words.to_csv('rank_wordle_words.csv',index=False)

if __name__ == "__main__":
    try:
        evaluate()
    except KeyboardInterrupt:
        print("\nBetter luck next time")