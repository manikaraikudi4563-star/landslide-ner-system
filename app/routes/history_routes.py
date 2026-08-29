from fastapi import APIRouter
from app.data.ner_geospatial import HISTORICAL_LANDSLIDES

router = APIRouter(tags=["Historical Landslides"])

@router.get("/api/historical-landslides")
@router.get("/api/history/landslides")
async def get_historical_landslides():
    return HISTORICAL_LANDSLIDES
