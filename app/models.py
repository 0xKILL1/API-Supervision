from typing import Optional, List, Dict, Any
from sqlmodel import SQLModel, Field, Column, JSON
from pydantic import BaseModel, ConfigDict 


class SharedFields(BaseModel):
    model_config = ConfigDict(extra='ignore') 
    hostname: str
    ip: str
    is_up: bool = False
    username: str
    password: str

class OrdinateurCreate(SharedFields):
    ram: Optional[str] = None
    disk: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    
class OrdinateurRead(OrdinateurCreate):
    id: int

class Ordinateur(SharedFields, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    hostname: str
    ip: str
    is_up: bool = False

    ram: Optional[str] = None
    disk: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, 
        sa_column=Column(JSON)
    ) 

class RouteurCreate(SharedFields):
    nb_interface: Optional[int] = None
    interfaces_ip: Optional[List[Dict[str, Any]]] = Field(default_factory=list)

class RouteurRead(RouteurCreate):
    id: int

class Routeur(SharedFields, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    hostname: str
    ip: str
    is_up: bool = False

    nb_interface: Optional[int] = None
    interfaces_ip: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, 
        sa_column=Column(JSON)
    )

class User(BaseModel,SQLModel,table=True):
    id: Optional[int]=Field(default=None,primary_key=True)
    nom: str
    HashPsswd: str
    email: Optional[str]=""
    adresse: Optional[str]=""




