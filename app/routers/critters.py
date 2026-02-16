from fastapi import APIRouter, Depends, status
from fastapi.exceptions import RequestValidationError
from sqlmodel import SQLModel, Session, select

from app.db import get_db
from app.dependencies import PermissionsValidator
from app.models.critters import Critter


class CritterCreate(SQLModel):
    name: str
    nickname: str
    is_freak: bool
    species_id: int

class CritterRead(SQLModel):
    id: int
    name: str
    nickname: str
    is_freak: bool
    species_id: int


router = APIRouter()

@router.get('/api/critters', response_model=list[CritterRead],
            dependencies=[Depends(PermissionsValidator(['read:critters']))])
def read_critters(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    stmt = select(Critter).offset(skip).limit(limit)
    return db.exec(stmt).all()

@router.get('/api/critters/{tax_id}', response_model=list[CritterRead],
            dependencies=[Depends(PermissionsValidator(["read:critters"]))])
def critters_by_tax_id(tax_id: int, db: Session = Depends(get_db)):
    stmt = select(Critter).where(Critter.species_id == tax_id)
    return db.exec(stmt).all()


@router.get('/api/nicknamed/{tax_id}', response_model=list[CritterRead])
def critter_by_tax_id_and_nickname(tax_id: int, nickname: str, db: Session = Depends(get_db)):
    stmt = select(Critter).where((Critter.species_id == tax_id) & (Critter.nickname == nickname))
    return db.exec(stmt).all()

@router.post('/api/critter', response_model=CritterRead, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(PermissionsValidator(["write:critters"]))])
async def add_critter(critter: CritterCreate, db: Session = Depends(get_db)):
    if critter.nickname == 'dude':
        raise RuntimeError('dude does not abide')
    exists = db.exec(select(Critter).where(Critter.nickname == critter.nickname)).first()
    if exists:
        raise RequestValidationError([{
        'loc': ['body', 'nickname'],
        'msg': f'{critter.nickname} nickname is already in use.',
        'type': 'value_error.duplicate'
    }])
    db_obj = Critter(**critter.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

