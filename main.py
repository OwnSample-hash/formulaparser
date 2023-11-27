#!/bin/env python3
from string import ascii_uppercase
from typing import Dict, List
from logic import lexer
from logic.parser import Parser as Parser
from logic.lexer import Lexer
from utils import *
from models import *
import sys


def do(prompt: str):
    for i in range(size):
        print(ascii_uppercase[i], end=' ')
    for expr in expr_list:
        print(expr.name, end=' ')
    print(f'| {prompt}')
    vals: List[Dict[str, bool]] = []
    for row in make_table(size):
        tmp: Dict[str, bool] = {}
        i = 0
        for c in row:
            tmp[ascii_uppercase[i]] = bool(int(c))
            i += 1
        vals.append(tmp)
    for cur in vals:
        for v in cur.values():
            print(int(v),end=" ") # pyright: ignore
        try:
            print(int(Parser(Lexer(prompt), cur).expr())) # pyright: ignore
        except lexer.LexerException as e:
            print(str(e))
        


def do_eval(expr: EXPR):
    out = [] 
    vals: List[Dict[str, bool]] = []
    for row in make_table(size):
        tmp: Dict[str, bool] = {}
        i = 0
        for c in row:
            tmp[ascii_uppercase[i]] = bool(int(c))
            i += 1
        vals.append(tmp)

    for cur in vals:
        out.append(int(Parser(Lexer(prompt), cur).expr())) # pyright: ignore
    expr.res = out


def resize_expr_l():
    for expr in expr_list:
        [expr.res.append(0) for _ in range(2**size - len(expr.res))]


if __name__ == '__main__':
    usage()
    size = get_size()
    # ev = Evaler(size)
    # parser = Parser('')
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
        if not prompt:
            print('Empty prompt try again!')
            continue
        if prompt == 'Q':
            print('Bye')
            break

        if prompt == 'RE':
            size = int(input('How many elements?> '))
            resize_expr_l()
            for expr in expr_list:
                do_eval(expr)
            print('Resized table to', size, 'and reevaluated expressions')
            continue

        if prompt.startswith('RE'):
            size = int(prompt.split(' ')[1])
            resize_expr_l()
            for expr in expr_list:
                do_eval(expr)
            print('Resized table to', size, 'and reevaluated expressions')
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
            for it in make_table(size):
                for i in range(size):
                    exec(f'{ascii_uppercase[i]} = int(it[{i}])')
                    exec(f'print({ascii_uppercase[i]}, end=" ")')
                print()
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
                    expr_par="NOT USED",
                    res=[0 for _ in range(2**size)],
                    hidden=False,
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
                    f'{expr.name}:\t{expr.expr_raw if prompt[-1:] == "R" else expr.expr_par}\t{"hidden" if expr.hidden else ""}'
                )
            continue

        if prompt == 'EVAL':
            for expr in expr_list:
                do_eval(expr)
            for i in range(size):
                print(ascii_uppercase[i], end=' ')
            print('| ', end='')
            for expr in expr_list:
                if expr.hidden:
                    continue
                print(expr.name, end=' | ')
            print()
            for i in range(2**size):
                for num in make_table(size)[i]:
                    print(num, end=' ')
                print('| ', end='')
                for expr in expr_list:
                    if expr.hidden:
                        continue
                    print(expr.res[i], end=' | ')   # pyright: ignore
                print()
            continue

        if prompt.startswith('HIDE'):
            try:
                item = ogp.split(' ')[1]
            except:
                print('Try again')
                continue
            for res in [
                expr.t_hidden() for expr in expr_list if expr.id == item
            ]:
                print(res)
            continue

        do(prompt)
