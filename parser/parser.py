from string import whitespace, ascii_uppercase


class Parser:
    def __init__(
        self,
        input: str,
    ):
        self.input_str = input

    def __iter__(self):
        iter_in = iter(self.input_str.upper())
        prev_c = ''
        for char in iter_in:
            # print("prev_c:",prev_c)
            if char in whitespace:
                continue
            out = char
            if (
                char in ascii_uppercase
                and prev_c[-1:] in ascii_uppercase
                and prev_c
            ):
                out = f' and {char}'
            if char == '!':
                if prev_c == '(' or prev_c[-1:] == ' ':
                    out = f'not {next(iter_in)}'
                elif prev_c[-1:] in ascii_uppercase and prev_c:
                    out = f' and not {next(iter_in)}'
                else:
                    out = f' not {next(iter_in)}'
            if char == '+':
                out = ' or '
            prev_c = out
            yield out
        # print("parsed:",self.input_str, "=V",)
        return

    def parse(self, input_: str) -> str:
        parsed = ''
        self.input_str = input_
        for parser in self:
            parsed += parser
        return parsed

    def set(self, input: str):
        self.input_str = input


if __name__ == '__main__':
    p = Parser('!a')
    parsed = ''
    for pc in p.parse('!a!b'):
        parsed += pc
    print(parsed)
    parsed = ''
    for pc in p.parse('(!a!B)+(!A+!BC)'):
        parsed += pc
    print(parsed)
    parsed = ''
    for pc in p.parse('ABC+!AB'):
        parsed += pc
    print(parsed)
