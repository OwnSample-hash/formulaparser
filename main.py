#!/bin/env python3
from string import ascii_uppercase
from parser.evaler import Evaler
from parser.parser import Parser
from utils import *
import sys


def help():
    print(
        """q to quit
re to resize table
w to save the last expr.
r to reevaluate last expression
p to print out the table
q or eof to quit
? to help"""
    )


def do(prompt: str):
    prompt = parser.parse(prompt)
    for i in range(size):
        print(ascii_uppercase[i], end=' ')
    prompt = dedupwc(prompt)
    print(f'{prompt}')
    for evc in ev(prompt):
        print(evc)


if __name__ == '__main__':
    help()
    size = get_size()
    ev = Evaler(size)
    parser = Parser('')
    last_evaled_prompt = ''
    while 1:
        try:
            ogp = input('>')
        except EOFError:
            print('Bye')
            quit(0)
        except KeyboardInterrupt:
            print('Bye')
            quit(0)
        prompt = ogp.upper()
        if prompt == 'Q':
            print('Bye')
            break

        if prompt == 'RE':
            size = int(input('How many elements?> '))
            print('Resized table to', size)
            ev.re_size(size)
            continue

        if prompt.startswith('RE'):
            size = int(prompt.split(' ')[1])
            print('Resized table to', size)
            ev.re_size(size)
            continue

        if prompt == '?':
            help()
            continue

        if prompt == 'W':
            if not last_evaled_prompt:
                print('Nothing has been evaluated')
                continue
            fn = input('Filename>')
            print(f'Saving to {fn}')
            with open(fn, 'a') as o:
                osout = sys.stdout
                sys.stdout = o
                do(last_evaled_prompt)
                sys.stdout = osout
            print('Done!')
            continue

        if prompt.startswith('W'):
            if not last_evaled_prompt:
                print('Nothing has been evaluated')
                continue
            fn = ogp.split(' ')[1]
            print(f'Saving to {fn}')
            with open(fn, 'a') as o:
                osout = sys.stdout
                sys.stdout = o
                do(last_evaled_prompt)
                sys.stdout = osout
            print('Done!')
            continue

        if prompt == 'R':
            print('Reevaluating last expression!')
            prompt = last_evaled_prompt

        if prompt == 'P':
            print('Printing table')
            for i in range(size):
                print(ascii_uppercase[i], end=' ')
            print()
            for it in ev.table:
                for i in range(size):
                    exec(f'{ascii_uppercase[i]} = int(it[{i}])')
                    exec(f'print({ascii_uppercase[i]}, end=" ")')
                print()
            continue

        if not prompt:
            print('Empty prompt try again!')
            continue

        do(prompt)
        last_evaled_prompt = prompt
