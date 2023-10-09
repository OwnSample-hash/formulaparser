from typing import List


class EXPR:
    id: str
    name: str
    expr_raw: str
    expr_par: str
    res: List[int]

    def __init__(
        self, id: str, name: str, expr_raw: str, expr_par: str, res: List[int]
    ):
        self.id = id
        self.name = name
        self.expr_raw = expr_raw
        self.expr_par = expr_par
        self.res = res
