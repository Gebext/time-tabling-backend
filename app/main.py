from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router

from app.config import get_settings

from app.core.exceptions import EXCEPTION_HANDLERS

from app.core.logging import setup_logging, get_logger

logger = get_logger(__name__)

@asynccontextmanager

async def lifespan(app: FastAPI):

    settings = get_settings()

    setup_logging(debug=settings.DEBUG)

    logger.info("🚀 %s v%s starting …", settings.APP_NAME, settings.APP_VERSION)

    yield

    logger.info("👋 %s shutting down …", settings.APP_NAME)

def create_app() -> FastAPI:

    settings = get_settings()

    app = FastAPI(

        title=settings.APP_NAME,

        version=settings.APP_VERSION,

        description=settings.APP_DESCRIPTION,

        docs_url="/docs",

        redoc_url="/redoc",

        lifespan=lifespan,

    )

    app.add_middleware(

        CORSMiddleware,

        allow_origins=settings.CORS_ORIGINS,

        allow_credentials=True,

        allow_methods=["*"],

        allow_headers=["*"],

    )

    for exc_class, handler in EXCEPTION_HANDLERS.items():

        app.add_exception_handler(exc_class, handler)

    app.include_router(api_router)

    @app.get("/health", tags=["Health"])

    async def health_check():

        return {"status": "healthy", "version": settings.APP_VERSION}

    return app

app = create_app()
