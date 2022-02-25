#!/usr/bin/env python3
#coding=utf-8

#includes
import numpy as np
import pandas as pd

WORDLE_TERMO_GREEN_COLOR_SIMBOL = '2'
WORDLE_TERMO_YELLOW_COLOR_SIMBOL = '1'

def evaluate_step(word,solutions):
    green_color_num,yellow_color_num = 0,0
    good_word_prob = 0
    for solution in solutions:
        has_green_color,has_yellow_color = False,False
        solution_list = list(solution)
        word_list = list(word)
        for (i,_) in enumerate(word_list):
            if(word_list[i] == solution_list[i]):
                green_color_num += 1
                has_green_color = True
                solution_list[i] = WORDLE_TERMO_GREEN_COLOR_SIMBOL
                word_list[i] = WORDLE_TERMO_GREEN_COLOR_SIMBOL

        for (i,word_char) in enumerate(word_list):
            if((word_char == WORDLE_TERMO_GREEN_COLOR_SIMBOL) or (word_list[i] == WORDLE_TERMO_YELLOW_COLOR_SIMBOL)):
                continue
            elif(word_char in solution_list):
                yellow_color_num += 1
                has_yellow_color = True
                pos_char_sol = solution_list.index(word_char)
                pos_char_word = word_list.index(word_char)
                solution_list[pos_char_sol] = WORDLE_TERMO_YELLOW_COLOR_SIMBOL
                word_list[pos_char_word] = WORDLE_TERMO_YELLOW_COLOR_SIMBOL

        good_word = (1 if(has_green_color or has_yellow_color) else 0)
        good_word_prob += good_word

    good_word_prob = good_word_prob/len(solutions)
    return green_color_num,yellow_color_num,good_word_prob

def evaluate(possi_words,all_words):
    rank_words = pd.DataFrame(columns=['word','green_color_num','yellow_color_num','good_word_prob'])

    for word in all_words:
        eright_pos,eyellow_color_num,egood_word_prob = evaluate_step(word,possi_words)
        rank_words = rank_words.append({'word':word,'green_color_num':eright_pos,'yellow_color_num':eyellow_color_num,'good_word_prob':egood_word_prob}, ignore_index=True)

    return rank_words

def remove_wrong_words(guess,colors,possible_solutions,all_words):
    letter_in_solution = np.array(["_"])
    for pos,_ in enumerate(colors):
        if ((colors[pos] == 2) or (colors[pos] == 1)):
            letter_in_solution = np.append(letter_in_solution,guess[pos])
    for pos,color_i in enumerate(colors):
        letter = guess[pos]
        if(color_i == 0):
            for solution in possible_solutions:
                if(letter in solution):
                    if(letter not in letter_in_solution):
                        possible_solutions = np.delete(possible_solutions,np.where(possible_solutions == solution))
                    else:
                        possible_solutions = np.delete(possible_solutions,np.where(possible_solutions[pos] == solution[pos]))
            for word in all_words:
                if(letter in word):
                    if(letter not in letter_in_solution):
                        all_words = np.delete(all_words,np.where(all_words == word))
                    else:
                        all_words = np.delete(all_words,np.where(all_words[pos] == word[pos]))
        elif(color_i == 1):
            for solution in possible_solutions:
                if((letter not in solution)or(letter == solution[pos])):
                    possible_solutions = np.delete(possible_solutions,np.where(possible_solutions == solution))
            for word in all_words:
                if((letter not in word)or(letter == word[pos])):
                    all_words = np.delete(all_words,np.where(all_words == word))
        elif(color_i == 2):
            for solution in possible_solutions:
                if(letter != solution[pos]):
                    possible_solutions = np.delete(possible_solutions,np.where(possible_solutions == solution))
            for word in all_words:
                if(letter != word[pos]):
                    all_words = np.delete(all_words,np.where(all_words == word))
    return possible_solutions,all_words

def greedy_action(possible_solutions, rank_words):
    for rank_word in rank_words:
        if(rank_word in possible_solutions):
            return rank_word
    return "something_bad_happened"