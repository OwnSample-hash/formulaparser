from string import ascii_uppercase, whitespace
from sys import exc_info   # pyright: ignore
from typing import Iterator, List
from models import EXPR
from utils.dedupchar import dedupwc
from utils.mktbl import make_table


class Evaler:
    def __init__(self, size: int) -> None:
        self.size: int = size
        self.table: List[List[str]] = make_table(self.size)
        self.more_info: bool = False
        self.expr_list: List[EXPR]

    def re_size(self, new_size: int) -> None:
        self.size: int = new_size
        self.table: List[List[str]] = make_table(self.size)
        self.prompt: str = ''

    def __iter__(self) -> Iterator[str | int]:
        abort_ = False
        j = 0
        for it in self.table:   # pyright: ignore
            for i in range(self.size):
                exec(f'{ascii_uppercase[i]} = int(it[{i}])')
                if not self.raw:
                    exec(f'print({ascii_uppercase[i]}, end=" ")')
            for i in range(len(self.expr_list)):
                if self.expr_list[i].hidden:
                    continue
                exec(f'{self.expr_list[i].name}={self.expr_list[i].res[j]}')
                if not self.raw:
                    exec(f'print({self.expr_list[i].name}, end=" ")')
            try:
                vars = dedupwc(
                    self.prompt.replace('and', '')
                    .replace('or', '')
                    .replace('not', '')
                )
                for char in vars:
                    if char in whitespace:
                        continue
                    if char not in list(locals().keys()):
                        for expr in self.expr_list:
                            if char == expr.name:
                                print(f'{char} was hidden use "hide {char}" to unhide it.')                        
                                abort_ = True
                                break
                        if not abort_:
                            print(f'\n{char} was not defined in this eval ctx!')
                        abort_ = True
                        break
                if not self.raw:
                    yield '| {0}{1}'.format(
                        int(eval(self.prompt)),
                        ('\t' + self.prompt) if self.more_info else '',
                    )
                else:
                    yield int(eval(self.prompt))
            except NameError:
                print('\n\nUse re "<num>" to set variable size')
                abort_ = True
                break
            except:
                print(
                    '\nErr happend in evaluation of the expression\nAborting...'
                )
                abort_ = True
                break
            if abort_:
                break
            j += 1
        return

    def __call__(self, prompt: str, expr_list: List[EXPR], raw: bool = False):
        self.prompt = prompt
        self.raw = raw
        self.expr_list = expr_list
        return self
