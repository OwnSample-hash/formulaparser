def dec2anys(num: int, pad: int, base: int = 2) -> str:
    outs = ''
    while 1:
        outs += str(num % base)
        num = int(str(num / base).split('.')[0].split(',')[0])
        if num == 0:
            break
    outs = outs[::-1]
    if len(outs) < pad:
        diff = pad - len(outs)
        outs = '0' * diff + outs
    # print(bins)
    return outs


def make_table(size: int):
    limit = 2**size
    table = []
    for num in range(0, limit):
        tmp = dec2anys(num, size)
        row = []
        for i in range(0, size):
            row.append(tmp[i])
        table.append(row)
    # pp(table)
    return table
