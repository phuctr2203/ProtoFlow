from fastapi import APIRouter

from app.api.v1 import approvals, dev, health, intelligence, meetings, mvp, projects, webhooks

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(projects.router)
api_router.include_router(meetings.router)
api_router.include_router(intelligence.router)
api_router.include_router(mvp.router)
api_router.include_router(approvals.router)
api_router.include_router(webhooks.router)
api_router.include_router(dev.router)
