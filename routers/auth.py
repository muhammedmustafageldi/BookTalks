from fastapi import APIRouter

router = APIRouter(tags=["Auth"])

@router.get("/auth/")
async def get_auth():
    return {'user: ': 'authenticated'}