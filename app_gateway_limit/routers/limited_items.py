from fastapi import APIRouter


router = APIRouter(prefix="/limited_items", tags=["Limited Items"])


@router.get("/")
def get_items():
    return {"message": "OK - passed rate limit"}
