from typing import Optional
from sqlmodel import SQLModel, Field

class Equipement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hostname: str
    ip: Optional[str] = None
    type: str = "Equipement"
    username: str
    password: Optional[str] = None
    key_filename: Optional[str] = None
    ram: Optional[str] = "8gb"
    disk: Optional[str] = "C:\\"
    

    nb_interface: Optional[int] = 1
    interface: Optional[str] = ""
