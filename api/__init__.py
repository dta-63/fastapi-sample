from fastapi import APIRouter, Depends

from .items import items as items_router
from .others import others as others_router
from tools.security import Auth

router = APIRouter()

router.include_router(items_router, prefix="/items", tags=["items"], dependencies=[Depends(Auth())])
router.include_router(others_router, prefix="/others", tags=["others"])
