from fastapi import APIRouter
from app.data.ner_geospatial import NER_STATES

router = APIRouter(tags=["States"])

@router.get("/api/states")
async def get_states_info():
    return NER_STATES
