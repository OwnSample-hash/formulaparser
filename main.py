#!/bin/env python3
from parser.evaler import Evaler
from parser.parser import Parser
from utils import *

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


if __name__ == '__main__':
    help()
    size = get_size()
    ev = Evaler(size)
    parser = Parser("A")
    last_evaled_prompt = ''
    while 1:
        try:
            ogp = input('>')
        except EOFError:
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
            save(last_evaled_prompt, fn, size, ev.table)
            print('Done!')
            continue

        if prompt.startswith('W'):
            if not last_evaled_prompt:
                print('Nothing has been evaluated')
                continue
            fn = ogp.split(' ')[1]
            print(f'Saving to {fn}')
            save(last_evaled_prompt, fn, size, ev.table)
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

        for i in range(size):
            print(ascii_uppercase[i], end=' ')
        prompt = dedupwc(prompt)
        print(f'{check_dm(prompt)}')
        parsed = parser.parse(prompt)
        for evc in ev(parsed):
                print(evc)
        last_evaled_prompt = prompt
