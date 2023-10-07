from pydantic import BaseModel
from typing import List


class EXPR_RES(BaseModel):
    name: str
    values: List[int]


class EXPR(BaseModel):
    # id: int
    name: str
    expr_raw: str
    expr_par: str
    res: EXPR_RES | None = None
