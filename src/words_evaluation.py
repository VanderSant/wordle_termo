#!/usr/bin/env python3
#coding=utf-8

import numpy as np

WORDLE_POSSIBLE_WORDS_PATH = "docs/wordle/all_possibles_words.txt"
WORDLE_ALL_WORDS_PATH = "docs/wordle/all_words.txt"
WORD_SIZE = 5

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

    eval_w = evaluate_step(possi_words[0],all_words)
    evaluate_words = np.array([(possi_words[0],eval_w)],dtype=[('name', 'U10'), ('value', 'i4')])
    eval_w = evaluate_step(possi_words[1],all_words)
    evaluate_words = np.append(evaluate_words,[(possi_words[1],eval_w)])
    
    print(evaluate_words)
    #for word in possi_words:
        #word_evaluate = evaluate_step(word,all_words)

    print(possi_words)
    print(all_words)

if __name__ == "__main__":
    try:
        evaluate()
    except KeyboardInterrupt:
        print("\nBetter luck next time")