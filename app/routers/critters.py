from fastapi import APIRouter, Depends, status
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from ..dependencies import PermissionsValidator, validate_token

class Species(BaseModel):
    id: int
    name: str

class Critter(BaseModel):
    name: str
    nickname: str
    species: Species
    is_freak: bool

# TODO
# PUT IN SQLITE or something so that multiple threads
# can share this same list
cat = Species(id=9685, name="Felis catus Linnaeus")
human = Species(id=9606, name="Homo sapiens")
critter_store = [
    Critter(name='Bruce Wayne', nickname='BW', is_freak=True, species=cat),
    Critter(name='Lu-Lu Fishpaw', nickname='LuLu', is_freak=True, species=cat),
    Critter(name='Stuart Smiley', nickname='Stu', is_freak=False, species=human),
    Critter(name='Jennifer Lentz', nickname='Doc', is_freak=False, species=human)
]

router = APIRouter()

@router.get('/critters', dependencies=[Depends(PermissionsValidator(['read:critters']))])
def read_critters(skip: int = 0, limit: int = 10):
    return critter_store[skip: skip + limit]

@router.get('/critters/{tax_id}', dependencies=[Depends(PermissionsValidator(["read:critters"]))])
def critters_by_tax_id(tax_id: int):
    return [critter for critter in critter_store if critter.species.id == tax_id]

@router.get('/nicknamed/{tax_id}', response_model=list[Critter])
def critter_by_tax_id_and_nickname(tax_id: int, nickname: str):
    return [critter for critter in critter_store
            if critter.species.id == tax_id and critter.nickname == nickname]

@router.post('/critter', response_model=Critter, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(PermissionsValidator(["write:critters"]))])
async def add_critter(critter: Critter):
    if critter.nickname == 'dude':
        raise RuntimeError('dude does not abide')
    for existing in critter_store:
        if existing.nickname == critter.nickname:
            raise RequestValidationError(f'{existing.nickname} nickname is already in use.')
    critter_store.append(critter)
    return critter

