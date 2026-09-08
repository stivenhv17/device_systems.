from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routes.user_routes import router as user_router


app = FastAPI(
    title="Device Systems API",
    description="API REST para la gestión de usuarios del sistema device_systems.",
    version="1.0"
)


@app.middleware("http")
async def agregar_cabeceras(request: Request, call_next):

    response = await call_next(request)

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    return response


app.include_router(user_router)


@app.get("/")
def inicio():
    return {
        "message": "API device_systems funcionando correctamente."
    }