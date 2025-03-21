from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import get_settings
from endpoints.api import api_router

app = FastAPI(
    title=get_settings().PROJECT_NAME,
    openapi_url=f"{get_settings().API_V1_STR}/openapi.json",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in get_settings().ALLOWED_HOSTS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=get_settings().API_V1_STR)


@app.get("/")
def root():
    return {"message": "Welcome to the Geolocation API. Go to /docs for documentation."}
