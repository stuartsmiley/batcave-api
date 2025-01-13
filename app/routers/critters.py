from fastapi import APIRouter, status
from pydantic import BaseModel

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

@router.get('/critters')
def read_critters(skip: int = 0, limit: int = 10):
    return critter_store[skip: skip + limit]

@router.get('/critters/{tax_id}')
def critters_by_tax_id(tax_id: int):
    return [critter for critter in critter_store if critter.species.id == tax_id]

@router.get('/nicknamed/{tax_id}', response_model=list[Critter])
def critter_by_tax_id_and_nickname(tax_id: int, nickname: str):
    return [critter for critter in critter_store
            if critter.species.id == tax_id and critter.nickname == nickname]

@router.post('/critter', response_model=Critter, status_code=status.HTTP_201_CREATED)
async def add_critter(critter: Critter):
    critter_store.append(critter)
    return critter

