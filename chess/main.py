# Файл: logic_server.py
from fastapi import FastAPI, HTTPException
import httpx
import json
import chess
from pydantic import BaseModel

from src.Data.board import ChessBoard
from src.logic import ChessLogic
from Config import *

class GameState(BaseModel):
    formation: str | None = None
    single_board: bool = False

app = FastAPI(title="Chess Engine API")
logic = ChessLogic()

async def fetch_from_storage(is_first_storgate) -> dict:
    """Асинхронный запрос для получения данных"""
    storage_name = FIRST_PLAYER if is_first_storgate else SECOND_PLAYER
    url = f"{URL}{storage_name}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=5.0)
            response.raise_for_status()
            return response.json() # Сразу возвращаем как словарь
        except httpx.RequestError as e:
            # Если хранилище упало, логика честно об этом скажет
            raise HTTPException(status_code=503, detail=f"Ошибка связи с Storage API: {e}")


@app.get("/step")
async def process_step():
    """Заставить логику сделать логический шаг (подятнуть данные и применить их на логику)"""
    data = await fetch_from_storage(logic.is_white_turn if not logic.use_signle_board else True)

    if not data:
        return {"error": "Storage is empty, waiting for first move"}

    if isinstance(data, str):
        data = json.loads(data)
    board = ChessBoard(data)
    logic.parse_board(board)

    return logic.get_data()

@app.get("/data")
async def get_current_data():
    """Просто возвращает текущее состояние логики"""
    return logic.get_data()

@app.post("/reset")
async def reset_game(state: GameState):
    """Сбрасывает состояние логики, получает на вход json с позицией в uci и играет ли 1 устройство"""
    global logic
    logic = ChessLogic(use_signle_board = state.single_board)
    if state.formation:
        logic.board = chess.Board(state.formation)
        logic.is_white_turn = logic.board.turn == chess.WHITE
    return {"status": "ok", "message": "Logic reset successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
