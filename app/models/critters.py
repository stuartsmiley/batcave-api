from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class Species(SQLModel, table=True):
    __tablename__ = 'species'
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(index=True)
    critters: List['Critter'] = Relationship(back_populates="species")

class Critter(SQLModel, table=True):
    __tablename__ = 'critters'
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    nickname: str = Field(index=True, unique=True)
    is_freak: bool
    species_id: int = Field(foreign_key="species.id", index=True)
    species: Optional[Species] = Relationship(back_populates="critters")