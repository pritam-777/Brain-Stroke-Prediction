from pydantic import BaseModel
from typing import Optional, List


class Health(BaseModel):
    gender:Optional[str]=None
    Age:Optional[int]=None
    hypertension:Optional[str]=None
    heart:Optional[str]=None
    married:Optional[str]=None
    work:Optional[str]=None
    res:Optional[str]=None
    glu: Optional[float] = None
    bmi: Optional[float] = None
