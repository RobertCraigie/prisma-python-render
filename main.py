"""Basic FastAPI app for CRUD operations on users and posts using Prisma Client Python"""
from typing import Optional, List

from fastapi import FastAPI
from prisma import Prisma
from prisma.models import User
from prisma.partials import UserWithoutRelations


app = FastAPI()
prisma = Prisma(auto_register=True)


@app.on_event('startup')  # type: ignore
async def startup() -> None:
    await prisma.connect()


@app.on_event('shutdown')  # type: ignore
async def shutdown() -> None:
    if prisma.is_connected():
        await prisma.disconnect()


@app.get(
    '/users',
    response_model=List[UserWithoutRelations],
)
async def list_users(take: int = 10) -> List[User]:
    return await User.prisma().find_many(take=take)


@app.post(
    '/users',
    response_model=UserWithoutRelations,
)
async def create_user(name: str, email: Optional[str] = None) -> User:
    return await User.prisma().create({'name': name, 'email': email})

