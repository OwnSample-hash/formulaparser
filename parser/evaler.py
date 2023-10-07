from string import ascii_uppercase   # pyright: ignore
from typing import List
from utils.mktbl import make_table


class Evaler:
    def __init__(self, size: int) -> None:
        self.size = size
        self.table: List[List[str]] = make_table(self.size)
        self.more_info: bool = False

    def re_size(self, new_size):
        self.size = new_size
        self.table: List[List[str]] = make_table(self.size)
        self.prompt: str = ''

    def __iter__(self):
        abort_ = False
        for it in self.table:   # pyright: ignore
            for i in range(self.size):
                exec(f'{ascii_uppercase[i]} = int(it[{i}])')
                exec(f'print({ascii_uppercase[i]}, end=" ")')
            try:
                # print(self.prompt)
                yield '| {0}{1}'.format(int(eval(self.prompt)) ,(
                    '\t' + self.prompt
                ) if self.more_info else '')
            except:
                print(
                    '\nErr happend in evaluation of the expression\nAborting...'
                )
                abort_ = True
                break
            if abort_:
                break
        return

    def __call__(self, prompt: str):
        self.prompt = prompt
        return self
