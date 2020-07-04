from fastapi import APIRouter
from rest_api.controller import search

router = APIRouter()
router.include_router(search.router, tags=["search"])

