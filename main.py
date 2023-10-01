#!/bin/env python3
from utils import *

#!(A&B) == !A|!B
#! negate
# | or
# & and


def help():
    print(
        """
        q to quit\n
        re to resize table\n
        w to save the last expr.\n
        r to reevaluate last expression\n
        ? to help
        """
    )


if __name__ == '__main__':
    help()
    try:
        size = int(input('How many elements?> '))
    except EOFError:
        print('Bye')
        quit(0)
    table = make_table(size)
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
            table = make_table(size)
            print('Resized table to', size)
            continue

        if prompt.startswith('RE'):
            size = int(prompt.split(' ')[1])
            table = make_table(size)
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
            save(last_evaled_prompt, fn, size, table)
            print('Done!')
            continue

        if prompt.startswith('W'):
            if not last_evaled_prompt:
                print('Nothing has been evaluated')
                continue
            fn = ogp.split(' ')[1]
            print(f'Saving to {fn}')
            save(last_evaled_prompt, fn, size, table)
            print('Done!')
            continue

        if prompt == 'R':
            print('Reevaluating last expression!')
            prompt = last_evaled_prompt

        if not prompt:
            print('Empty prompt try again!')
            continue

        prompt = (
            prompt.replace('!', ' not ')
            .replace('&', ' and ')
            .replace('|', ' or ')
            .strip()
        )

        for i in range(size):
            print(ascii_uppercase[i], end=' ')
        prompt = dedupchar(prompt)
        print(f'{check_dm(prompt)}')
        for it in table:
            for i in range(size):
                exec(f'{ascii_uppercase[i]} = int(it[{i}])')
                exec(f'print({ascii_uppercase[i]}, end=" ")')
            try:
                print('|', eval(prompt))
                last_evaled_prompt = prompt
            except:
                print('Err')
