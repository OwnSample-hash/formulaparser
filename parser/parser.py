from string import whitespace, ascii_uppercase


class Parser:
    def __init__(
        self,
        input: str,
    ):
        self.input_str = input

    def __iter__(self):
        self.ogp = self.input_str
        iter_in = iter(self.ogp.upper())
        prev_c = ''
        for char in iter_in:
            if char in whitespace:
                continue
            out = char
            if char in ascii_uppercase and prev_c[-1:] in ascii_uppercase:
                out = f' and {char}'
            if char == '!':
                if prev_c == '(':
                    out = f'not {next(iter_in)}'
                else:
                    out = f' not {next(iter_in)}'
            if char == '+':
                out = ' or '
            prev_c = out
            yield out
        return

    def parse(self, input_:str)->str:
        parsed = ""
        self.input_str = input_
        for parser in self:
           parsed += parser
        return parsed

    def set(self, input: str):
        self.input_str = input


if __name__ == '__main__':
    parsed = ""
    for pc in Parser('!a!B'):
        parsed += pc
    print(parsed)
