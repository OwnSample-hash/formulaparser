def dec2anys(num: int, pad: int, base: int = 2) -> str:
    outs = ''
    while num > 0:
        outs += str(num % base)
        num = int(str(num / base).split('.')[0])
    outs = outs[::-1]
    if len(outs) < pad:
        outs = '0' * (pad - len(outs)) + outs
    return outs


def anys2dec(in_: str, base: int) -> int:
    out = 0
    i = 0
    for digit in in_[::-1]:
        out += base**i * int(digit)
        i += 1
    return out


def make_table(size: int) -> list[list[str]]:
    limit = 2**size
    table = []
    for num in range(0, limit):
        tmp = dec2anys(num, size)
        row = []
        for i in range(0, size):
            row.append(tmp[i])
        table.append(row)
    return table
