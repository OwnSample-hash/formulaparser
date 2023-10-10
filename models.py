from typing import List


class EXPR:
    id: str
    name: str
    expr_raw: str
    expr_par: str
    res: List[int]
    hidden: bool

    def __init__(
        self,
        id: str,
        name: str,
        expr_raw: str,
        expr_par: str,
        res: List[int],
        hidden: bool,
    ):
        self.id = id
        self.name = name
        self.expr_raw = expr_raw
        self.expr_par = expr_par
        self.res = res
        self.hidden = hidden

    def t_hidden(
        self,
    ):
        self.hidden = not self.hidden
        return f'{self.name} has been {"" if self.hidden else "un"}hid'
