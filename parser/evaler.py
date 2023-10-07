from string import ascii_uppercase   # pyright: ignore
from typing import Iterator, List
from utils.mktbl import make_table


class Evaler:
    def __init__(self, size: int) -> None:
        self.size: int = size
        self.table: List[List[str]] = make_table(self.size)
        self.more_info: bool = False

    def re_size(self, new_size: int) -> None:
        self.size: int = new_size
        self.table: List[List[str]] = make_table(self.size)
        self.prompt: str = ''

    def __iter__(self) -> Iterator[str | int]:
        abort_ = False
        for it in self.table:   # pyright: ignore
            for i in range(self.size):
                exec(f'{ascii_uppercase[i]} = int(it[{i}])')
                exec(f'print({ascii_uppercase[i]}, end=" ")')
            try:
                # print(self.prompt)
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
        return

    def __call__(self, prompt: str, raw: bool = False):
        self.prompt = prompt
        self.raw = raw
        return self
