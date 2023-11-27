import re
from typing import Tuple, List


TOKEN_TYPES = [
    ('VAR', r'\w\d'),
    ('VAR', r'\w'),
    ('OR', r'\+'),
    ('AND', r'\*'),
    ('NOT', r'\!'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('WHITESPACE', r'\s+'),
]


class Token:
    def __init__(self, type, value):
        self.type: str = type
        self.value: str = value

    def __str__(self):
        return f'Token({self.type}, {repr(self.value)})'


class LexerException(Exception):
    pass


class InvalidChar(LexerException):
    pass


class Lexer:
    def __init__(self, text, token_types=TOKEN_TYPES):
        self.text = text
        self.position = 0
        self.current_token = None
        self.token_types: List[Tuple[str, str]] = token_types

    def __iter__(self):
        return self

    def __next__(self):
        return self.get_next_token()

    def get_next_token(self) -> Token:
        if self.position >= len(self.text):
            return Token('EOF', None)

        for token_type, pattern in self.token_types:
            regex = re.compile(pattern)
            match = regex.match(self.text, self.position)

            if match:
                value = match.group(0)
                token = Token(token_type, value)
                self.position = match.end()
                return token

        raise InvalidChar
