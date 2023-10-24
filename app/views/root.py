from fastapi import APIRouter

router = APIRouter(
    tags=['root']
)

@router.get('/')
async def home():
    return {'message': 'Welcome home 💀'}