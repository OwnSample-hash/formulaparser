from string import whitespace


def dedupwc(ins: str) -> str:
    out = ''
    for ch in ins:
        if not (out[-1:] == ch and ch in whitespace):
            out += ch
    return out
