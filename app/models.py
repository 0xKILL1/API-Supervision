from typing import Optional
from sqlmodel import SQLModel, Field

class Equipement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hostname: str
    ip: str
