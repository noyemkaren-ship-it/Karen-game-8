from repository.game_repo import GameRepository
from fastapi import HTTPException

game_repo = GameRepository()

def create_game(name, link):
    if game_repo.get_by_name(name):
        raise HTTPException(status_code=400, detail="Game with this name already exists")
    result = game_repo.create(name, link)
    return result


def get_game_all():
    result = game_repo.get_all()
    return result


def delete_game(name):
    if not game_repo.get_by_name(name):
        raise HTTPException(status_code=404, detail="Game not found")
    result = game_repo.delete(name)
    return result

