from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination
from redis.asyncio import Redis
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from src.db import redis
from src.services import rabbitmq
from src.api.v1.users import router as users_router
from src.api.v1.auth import router as auth_router
from src.api.v1.admin import router as admin_router
from src.api.v1.google_oauth import router as oauth_router
from src.core.config import settings
from src.utils.tracer_config import configure_tracer


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis.redis = Redis(
        host=settings.service_settings.redis_host,
        port=settings.service_settings.redis_port
    )
    rabbitmq.setup_rabbitmq()
    # await db_helper.create_database()
    yield
    # await db_helper.purge_database()
    await redis.redis.close()
    # rabbitmq.rabbitmq_connection.close()


if settings.service_settings.jaeger_configure_tracer:
    configure_tracer()


app = FastAPI(
    lifespan=lifespan,
    title="Authentication Service",
    docs_url='/auth/openapi',
    openapi_url='/auth/openapi.json',
)
app.add_middleware(SessionMiddleware, secret_key='some secret text')

add_pagination(app)


app.include_router(
    router=admin_router,
    prefix='/auth/roles',
    tags=['Roles: Role Management']
)
app.include_router(
    router=auth_router,
    prefix='/auth/auth',
    tags=['Auth: Login, Logout and Refresh tokens']
)
app.include_router(
    router=users_router,
    prefix='/auth/users',
    tags=['Users: User Management']
)
app.include_router(
    router=oauth_router,
    prefix='/auth/oauth',
    tags=['OAuth2']
)

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

if settings.service_settings.jaeger_configure_tracer:

    FastAPIInstrumentor.instrument_app(app)

    @app.middleware('http')
    async def before_request(request: Request, call_next):
        response = await call_next(request)
        request_id = request.headers.get('X-Request-Id')
        if not request_id:
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={'detail': 'X-Request-Id is required'}
            )
        return response
