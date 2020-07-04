from fastapi import APIRouter
from controller import search

router = APIRouter()
router.include_router(search.router, tags=["search"])

