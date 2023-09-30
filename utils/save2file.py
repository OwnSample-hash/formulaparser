from string import ascii_uppercase
from utils import check_dm, dedupchar
from typing import List


def save(expr: str, fn: str, size: int, table: List):
    with open(fn, 'w') as f:
        for i in range(size):
            f.write(f'{ascii_uppercase[i]} ')
        expr = dedupchar(expr)
        f.write(f'{check_dm(expr)}\n')
        for it in table:   # pyright: ignore
            for i in range(size):
                exec(f'{ascii_uppercase[i]} = int(it[{i}])')
                exec(f'f.write(f"{ascii_uppercase[i]} ")')
            try:
                f.write(f'| {eval(expr)}\n')
            except:
                f.write('Err')
        f.write('\n')
