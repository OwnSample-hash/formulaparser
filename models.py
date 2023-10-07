from pydantic import BaseModel
from typing import List


class EXPR(BaseModel):
    id: str
    name: str
    expr_raw: str
    expr_par: str
    res: List[int]
