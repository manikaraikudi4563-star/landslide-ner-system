from fastapi import APIRouter
from app.routes.states_routes import router as states_router
from app.routes.stations_routes import router as stations_router
from app.routes.sensors_routes import router as sensors_router
from app.routes.risk_routes import router as risk_router
from app.routes.ml_routes import router as ml_router
from app.routes.weather_routes import router as weather_router
from app.routes.shelter_routes import router as shelter_router
from app.routes.infrastructure_routes import router as infrastructure_router
from app.routes.routing_routes import router as routing_router
from app.routes.alert_routes import router as alert_router
from app.routes.incident_routes import router as incident_router
from app.routes.satellite_routes import router as satellite_router
from app.routes.simulation_routes import router as simulation_router
from app.routes.communication_routes import router as communication_router
from app.routes.history_routes import router as history_router
from app.routes.authority_routes import router as authority_router

all_routers = [
    states_router,
    stations_router,
    sensors_router,
    risk_router,
    ml_router,
    weather_router,
    shelter_router,
    infrastructure_router,
    routing_router,
    alert_router,
    incident_router,
    satellite_router,
    simulation_router,
    communication_router,
    history_router,
    authority_router
]
