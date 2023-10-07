#!/bin/env python3
from string import ascii_uppercase
from typing import List
from parser.evaler import Evaler
from parser.parser import Parser
from utils import *
from models import *
import sys


def do(prompt: str):
    prompt = parser.parse(prompt)
    for i in range(size):
        print(ascii_uppercase[i], end=' ')
    for expr in expr_list:
        print(expr.name, end=' ')
    prompt = dedupwc(prompt)
    print(f'| {prompt}')
    for evc in ev(prompt, expr_list):
        print(evc)


def do_eval(expr: EXPR):
    out = []
    for evc in ev(expr.expr_par, expr_list, True):
        out.append(evc)
    expr.res = out


if __name__ == '__main__':
    usage()
    size = get_size()
    ev = Evaler(size)
    parser = Parser('')
    last_evaled_prompt = ''
    expr_list: List[EXPR] = []
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
            usage()
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

        if prompt == 'M':
            ev.more_info = not ev.more_info
            print('Enabled' if ev.more_info else 'Disabled', 'more info')
            continue

        if prompt.startswith('LET'):
            payload = ogp.split(' ')
            if len(payload) != 3:
                print('Usage: let <Expr. name> <Expr.>')
                continue
            abort_ = False
            for expr in expr_list:
                if expr.name == payload[1]:
                    print(f'{expr.name} is already a register expr!')
                    abort_ = True
            if abort_:
                continue
            expr_list.append(
                EXPR(
                    id=payload[1],
                    name=payload[1].upper(),
                    expr_raw=payload[2],
                    expr_par=parser.parse(payload[2]),
                    res=[0 for _ in range(2**size)],
                )
            )
            continue

        if prompt.startswith('DEL'):
            try:
                item = ogp.split(' ')[1]
            except:
                print('Try again')
                continue
            [expr_list.remove(expr) for expr in expr_list if expr.id == item]
            continue

        if prompt.startswith('LIST'):
            for expr in expr_list:
                print(
                    f'{expr.name}:\t{expr.expr_raw if prompt[-1:] == "R" else expr.expr_par}'
                )
            continue

        if prompt == 'EVAL':
            for expr in expr_list:
                do_eval(expr)
            for i in range(size):
                print(ascii_uppercase[i], end=' ')
            print('| ', end='')
            for expr in expr_list:
                print(expr.name, end=' | ')
            print()
            for i in range(2**ev.size):
                for num in ev.table[i]:
                    print(num, end=' ')
                print('| ', end='')
                for expr in expr_list:
                    print(expr.res[i], end=' | ')   # pyright: ignore
                print()
            continue

        if not prompt:
            print('Empty prompt try again!')
            continue

        do(prompt)
        last_evaled_prompt = prompt
