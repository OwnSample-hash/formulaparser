def str2bin(num:int,pad:int):
    bins = ""
    do  = True
    while do:
        bins += str(num % 2)
        num = int(str(num / 2).split('.')[0].split(',')[0])
        if num == 0:
            do = False
    bins = bins[::-1]
    if len(bins) < pad:
        diff = pad - len(bins)
        bins = "0"*diff+bins
    # print(bins)
    return bins

def make_table(size:int):
    limit = 2**size
    table = []
    for num in range(0,limit):
        tmp = str2bin(num,size)
        row = []
        for i in range(0, size):
            row.append(tmp[i])
        table.append(row)
    # pp(table)
    return table
