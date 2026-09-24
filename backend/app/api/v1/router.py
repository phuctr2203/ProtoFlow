from fastapi import APIRouter

from app.api.v1 import dev, health, meetings, projects, webhooks

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(projects.router)
api_router.include_router(meetings.router)
api_router.include_router(webhooks.router)
api_router.include_router(dev.router)
