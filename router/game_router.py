# router/game_router.py
from serveces.game_services import create_game, get_game_all, delete_game
from fastapi import APIRouter, HTTPException
from schemas.game import Game

router = APIRouter(prefix="/game", tags=["game"])

@router.post("/create")
async def create_game_endpoint(game: Game):
    result = create_game(game.name, game.link)
    return {"message": "Game created successfully", "game": result} 

@router.get("/all")
async def get_game_all_endpoint():
    result = get_game_all()
    return {"games": result}

@router.delete("/delete/{name}")
async def delete_game_endpoint(name: str):
    result = delete_game(name)
    if result:
        return {"message": "Game deleted successfully"}
    raise HTTPException(status_code=404, detail="Game not found")