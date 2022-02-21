# %%
#!/usr/bin/env python3
#coding=utf-8

#includes
import numpy as np
import pandas as pd

# %%
# constants

WORDLE_POSSIBLE_WORDS_PATH = "docs/wordle/all_possibles_words.txt"
WORDLE_ALL_WORDS_PATH = "docs/wordle/all_words.txt"
WORDLE_INITIAL_SOLUTION_PATH = "results/wordle/initial_rank_wordle_words.csv"

WORDLE_GREEN_COLOR_SIMBOL = '2'
WORDLE_YELLOW_COLOR_SIMBOL = '1'

# %%
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
                solution_list[i] = WORDLE_GREEN_COLOR_SIMBOL
                word_list[i] = WORDLE_GREEN_COLOR_SIMBOL

        for (i,word_char) in enumerate(word_list):
            if((word_char == WORDLE_GREEN_COLOR_SIMBOL) or (word_list[i] == WORDLE_YELLOW_COLOR_SIMBOL)):
                continue
            elif(word_char in solution_list):
                yellow_color_num += 1
                has_yellow_color = True
                pos_char_sol = solution_list.index(word_char)
                pos_char_word = word_list.index(word_char)
                solution_list[pos_char_sol] = WORDLE_YELLOW_COLOR_SIMBOL
                word_list[pos_char_word] = WORDLE_YELLOW_COLOR_SIMBOL

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

def generate_initial_evaluate_list():
    with open(WORDLE_POSSIBLE_WORDS_PATH) as f:
        possi_words_list = [line.rstrip('\n') for line in f]
    possi_words = np.array(possi_words_list)

    with open(WORDLE_ALL_WORDS_PATH) as f:
        all_words_list = [line.rstrip('\n') for line in f]
    all_words = np.array(all_words_list)
    all_words = np.append(all_words,possi_words)

    # tranform dataframe to csv file#
    rank_words = evaluate(possi_words,all_words)
    rank_words = rank_words.sort_values(by=['good_word_prob'],ascending=False) #sort values
    rank_words.to_csv(WORDLE_INITIAL_SOLUTION_PATH,index=False)
    print(rank_words) 


# %%
def remove_wrong_words(guess,colors,possible_solutions,all_words):
    for pos,color_i in enumerate(colors):
        letter = guess[pos]
        if(color_i == 0):
            for solution in possible_solutions:
                if(letter in solution):
                    possible_solutions = np.delete(possible_solutions,np.where(possible_solutions == solution))
            for word in all_words:
                if(letter in word):
                    all_words = np.delete(all_words,np.where(all_words == word))
        elif(color_i == 1):
            for solution in possible_solutions:
                if(letter not in solution):
                    possible_solutions = np.delete(possible_solutions,np.where(possible_solutions == solution))
            for word in all_words:
                if(letter not in word):
                    all_words = np.delete(all_words,np.where(all_words == word))
        elif(color_i == 2):
            for solution in possible_solutions:
                if(letter != solution[pos]):
                    possible_solutions = np.delete(possible_solutions,np.where(possible_solutions == solution))
            for word in all_words:
                if(letter != word[pos]):
                    all_words = np.delete(all_words,np.where(all_words == word))
    return possible_solutions,all_words

# %%
def greedy_action(possible_solutions, rank_words):
    for rank_word in rank_words:
        if(rank_word in possible_solutions):
            return rank_word
    return "something_bad_happened"

def main():
    with open(WORDLE_POSSIBLE_WORDS_PATH) as f:
        possible_solutions_list = [line.rstrip('\n') for line in f]
    possible_solutions = np.array(possible_solutions_list)

    with open(WORDLE_ALL_WORDS_PATH) as f:
        all_words_list = [line.rstrip('\n') for line in f]
    all_words = np.array(all_words_list)
    all_words = np.append(all_words,possible_solutions)

    rank_words = pd.read_csv(WORDLE_INITIAL_SOLUTION_PATH)['word']
    colors = [0]*5

    guess = rank_words[0]
    while(colors != [2]*5):
        print("guess: ",guess)
        print("feedback:")
        feedback = input("result:")
        colors = [int(letter_feedback) for letter_feedback in feedback]

        possible_solutions,all_words = remove_wrong_words(guess,colors,possible_solutions,all_words)
        rank_words = evaluate(possible_solutions,all_words).sort_values(by=['good_word_prob'],ascending=False)['word']
        guess = greedy_action(possible_solutions, rank_words)
    print("easy peasy")

# %%
if __name__ == "__main__":
    try:
        # test_evaluate
        #takes almost 3 minutes
        #generate_initial_evaluate_list()

        main()
    except KeyboardInterrupt:
        print("\nBetter luck next time")


