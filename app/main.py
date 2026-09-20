from fastapi import FastAPI, Request

from app.database.connection import Base, engine
from app.models import user_model
from app.routes.user_routes import router as user_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="device_systems API",
    description="API REST para la gestión de usuarios del sistema device_systems.",
    version="2.0.0",
    contact={
        "name": "Stiven Hurtado Valencia"
    }
)


@app.middleware("http")
async def agregar_cabeceras(request: Request, call_next):

    response = await call_next(request)

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0.0"

    return response


app.include_router(user_router)


@app.get(
    "/",
    summary="Verificar funcionamiento de la API",
    description="Comprueba que la API device_systems se encuentre funcionando correctamente."
)
def inicio():
    return {
        "message": "API device_systems funcionando correctamente."
    }