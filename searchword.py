#!/usr/bin/python3
# -*- coding: utf-8 -*-

#

import string
import re
import random as r
import pickle as pk

#https://fr.wikipedia.org/wiki/Fr%C3%A9quence_d%27apparition_des_lettres
freq = {'e': 12.10, 'a': 7.11, 'i': 6.59, 's': 6.51, 'n': 6.39, 'r': 6.07,
        't': 5.92, 'o': 5.02, 'l': 4.96, 'u': 4.49, 'd': 3.67, 'c': 3.18,
        'm': 2.62, 'p': 2.49, 'g': 1.23, 'b': 1.14, 'v': 1.11, 'h': 1.11,
        'f': 1.11, 'q': 0.65, 'y': 0.46, 'x': 0.38, 'j': 0.34, 'k': 0.29,
        'w': 0.17, 'z': 0.15}



with open('lexique.txt', 'r') as lexique:
    RAW_LEXIQUE = lexique.read()
    LEXIQUE = RAW_LEXIQUE.split()

def load_words():
    global splited
    try:
        with open("sw_save.pk", "rb") as save:
            mypick = pk.Unpickler(save)
            splited = mypick.load()
    except FileNotFoundError:
        splited = dict()
        for i in LEXIQUE:
            try:
                splited[len(i)].append(i)
            except:
                splited[len(i)] = [i]
        for k, v in splited.items():
            splited[k] = sort_full_score(splited[k])
        with open("sw_save.pk", "wb") as save:
            mypick = pk.Pickler(save)
            mypick.dump(splited)


def score(word):
    """Return the score of the word"""
    if len(word) == 0:
        return 0
    # "e"=26 points "z"=1 point
    s = sum([freq[i] for i in word])
    return s/len(word)

def is_full(word):
    """Check wether the word contains unique letters or not"""
    return len(word) == len(set(word))

def sort_full_score(iterable):
    """"""
    iterable.sort(key=score, reverse=True)
    full = [i for i in iterable if is_full(i)]
    full.sort(key=score, reverse=True)
    for i in full:
        iterable.remove(i)
    # also return iterable in case the full is empty
    return full + iterable

def get_random(length, count=5):
    i = 0
    res = []
    while is_full(splited[length][i]):
        i += 1
        res.append(splited[length][i])
    try:
        return [r.choice(res) for _ in range(count)]
    except IndexError:
        return splited[length][0]

def search(guesses, excluded):
    """
    * = to ignore
    lowercase = good spot
    uppercase = wrong spot
    """
    length = len(guesses[0])
    pattern = r'\b([^'+excluded+r'\n]{'+str(length)+r'})\b'
    # all words without the excluded letters and of length 'length'
    result = " ".join(re.findall(pattern, RAW_LEXIQUE))
    pattern2 = ['' for _ in range(length)]
    regexs = []
    for idx, g in enumerate(guesses):
        regex = r'\b'
        for i in g:
            if i == '*':
                regex += '\w'
            elif i.isupper():
                regex += '[^' + i.lower() + ']'
            elif i.islower():
                regex += i
        regex += r'\b'
        regexs.append(regex)
    for reg in regexs: # try with re.sub to avoid the " ".join ???
        result = " ".join(re.findall(reg, result))
    # check if any of the 'wrongspot' letters is indeed in the words
    # {"letter": max number of times in the guess
    needed = {}
    for g in guesses:
        for i in g:
            # result already filtered with lowercase (ie good spot)
            if not i.isupper():
                continue
            i = i.lower()
            c = g.lower().count(i) # number of appearance
            if i not in needed.keys():
                needed[i] = c
            elif needed[i] < c:
                needed[i] = c
    result = result.split(' ')
    for r in result.copy():
        match = True
        for k, v in needed.items():
            if r.count(k) < v:
                match = False
                break
        if not match:
            result.remove(r)
    return sort_full_score(result)

load_words()
if __name__ == "__main__":
    pass
    
    
