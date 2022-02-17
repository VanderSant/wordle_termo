#!/usr/bin/env python3
#coding=utf-8

import numpy as np
import pandas as pd

def evaluate():
    f = open("docs/wordle/all_possibles_words.txt", "r")
    possi_words = np.split(f,"\n")
    print(possi_words)

if __name__ == "__main__":
    try:
        evaluate()
    except KeyboardInterrupt:
        print("\nBetter luck next time")