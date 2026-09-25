import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.auth.auth_routes import router as auth_router
from app.middlewares.request_middleware import RequestMiddleware, limiter
from app.routes.device_routes import router as device_router
from app.routes.user_routes import router as user_router
from app.routes.loan_routes import history_router as loan_history_router
from app.routes.loan_routes import router as loan_router

logging.basicConfig(level=logging.INFO)


app = FastAPI(
    title="device_systems API",
    description=(
        "API REST segura para gestión de usuarios, dispositivos y "
        "préstamos"
    ),
    version="3.0.0",
    contact={
        "name": "Stiven Hurtado Valencia"
    },
    openapi_tags=[
        {
            "name": "Auth",
            "description": "Registro, login y consulta del usuario autenticado."
        },
        {
            "name": "Users",
            "description": "Gestión de usuarios."
        },
        {
            "name": "Devices",
            "description": "Gestión de dispositivos."
        },
        {
            "name": "Loans",
            "description": "Gestión de préstamos y consultas relacionadas."
        },
        {
            "name": "Security",
            "description": (
                "Controles de seguridad: CORS, middleware de trazabilidad, "
                "autenticación JWT, autorización por rol y rate limiting."
            )
        }
    ]
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(RequestMiddleware)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)
app.include_router(loan_history_router)


@app.get(
    "/",
    include_in_schema=False
)
def inicio():
    return {
        "message": "API device_systems funcionando correctamente."
    }
