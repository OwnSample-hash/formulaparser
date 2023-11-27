import logging
from typing import Dict, List
from .lexer import Token, Lexer


class ParserExcepction(Exception):
    pass


class InvalidSyntax(ParserExcepction):
    pass


class Parser:
    def __init__(self, lexer, vals):
        self.lexer: Lexer = lexer
        self.prev_vars: List[Token] = []
        self.vals: Dict[str, bool] = vals
        self.current_token = self.lexer.get_next_token()

    def eat(self, expected_type):
        if self.current_token.type == expected_type:
            self.current_token = self.lexer.get_next_token()
            logging.debug(f'token:{self.current_token}')
        else:
            raise InvalidSyntax(
                f"Excepted '{expected_type}', got '{self.current_token.type}'"
            )

    def factor(self):
        token = self.current_token
        if token.type == 'VAR':
            self.eat('VAR')
            self.prev_vars.append(token)

        elif token.type == 'OR':
            self.eat('OR')

        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            result = self.expr()
            self.eat('RPAREN')
            return result

        elif token.type == 'NOT':
            self.eat('NOT')
            try:
                self.factor()
                return not self.vals[self.prev_vars[-1].value]
            except InvalidSyntax as e:
                print(str(e))
                return self.eat('LPAREN')
            # self.factor()
        else:
            raise ParserExcepction(f'Not implemented: {token}')

    def term(self):
        res = False
        do_not_reset = False
        local_vals: Dict[str, bool] = self.vals

        while self.current_token.type in ('OR', 'AND', 'VAR', 'NOT', 'LPAREN'):
            token = self.current_token
            if do_not_reset:
                do_not_reset = False
            else:
                local_vals = self.vals

            if token.type == 'OR':
                x = local_vals[self.prev_vars[-1].value]
                self.eat('OR')
                tmp = self.factor()
                if tmp == None:
                    y = self.vals[self.prev_vars[-1].value]
                else:
                    y = tmp
                # print(f"or x:{x} y:{y}", end=" ")
                if x == True:
                    res = True
                    continue
                elif y == True:
                    res = True
                    continue
                else:
                    res = False

            if token.type == 'AND':
                x = local_vals[self.prev_vars[-1].value]
                self.eat('AND')
                tmp = self.factor()
                if tmp == None:
                    y = self.vals[self.prev_vars[-1].value]
                else:
                    y = tmp
                if x == False:
                    res = False
                    continue
                elif y == False:
                    res = False
                    continue
                else:
                    res = True

            if token.type == 'VAR':
                if not len(self.prev_vars):
                    self.factor()
                    continue
                x = local_vals[self.prev_vars[-1].value]
                tmp = self.factor()
                if tmp == None:
                    y = self.vals[self.prev_vars[-1].value]
                else:
                    y = tmp
                if x == False:
                    res = False
                    continue
                elif y == False:
                    res = False
                    continue
                else:
                    res = True

            if token.type == 'LPAREN':
                res = res or self.factor()

            if token.type == 'NOT':
                self.eat('NOT')
                tmp = self.factor()
                if tmp == None:
                    local_vals[self.prev_vars[-1].value] = not self.vals[
                        self.prev_vars[-1].value
                    ]
                    res = local_vals[self.prev_vars[-1].value]
                    do_not_reset = True
                else:
                    res = not tmp

        return res

    def expr(self):
        return self.term()
