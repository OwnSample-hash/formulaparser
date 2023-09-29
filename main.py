#!/bin/env python3
from string import ascii_uppercase
from utils import *
#!(A&B) == !A|!B
#! negate
#| or
#& and

def help():
    print('q to quit;re to resize table;? to help')

if __name__ == "__main__":
    help()
    size = int(input("How many elements?> "))
    table = make_table(size)
    while 1:
        prompt = input(">").upper()
        if prompt == "Q":
            print('Bye')
            break
        if prompt == "RE":
            size = int(input("How many elements?> "))
            table = make_table(size)
            print("Resized table to ",size)
            continue
        if prompt == '?':
            help()
            continue
        if not prompt:
            print("Empty prompt try again!")
            continue
        prompt = prompt            \
            .replace('!', ' not ') \
            .replace('&', ' and ') \
            .replace('|', ' or ')  \
            .strip()

        for i in range(size):
            print(ascii_uppercase[i], end=" ")
        prompt = dedupchar(prompt)
        print(f"{check_dm(prompt)}")
        for it in table:
            for i in range(size):
                exec(f"{ascii_uppercase[i]} = int(it[{i}])")
                exec(f"print({ascii_uppercase[i]}, end=\" \")")
            print("|", eval(prompt))
