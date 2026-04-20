TILE_SIZE = 65
GAP = 5
STEP = TILE_SIZE + GAP   
COLS = 10  # 0 и 9 - боковые панели, 1-8 - доска
ROWS = 8
WIDTH = COLS * STEP - GAP
HEIGHT = ROWS * STEP - GAP
FPS = 30


COLOR_BG = (40, 40, 40)              
COLOR_WHITE = (240, 217, 181)
COLOR_BLACK = (181, 136, 99)
COLOR_SIDEBAR_WHITE = (200, 200, 200)
COLOR_SIDEBAR_BLACK = (50, 50, 50)
COLOR_HIGHLIGHT = (100, 200, 100, 150) 
COLOR_CHECK = (200, 50, 50, 150)
COLOR_DESYNC = (255, 150, 0, 150)


PIECES_UNICODE = {
    "white": {1: "♙", 2: "♘", 3: "♗", 4: "♖", 5: "♕", 6: "♔"},
    "black": {1: "♟", 2: "♞", 3: "♝", 4: "♜", 5: "♛", 6: "♚"}
}

BASE_URL = "http://127.0.0.1:8001"
STORAGE_NAME = "storage3"
CV_URL = "http://127.0.0.1:8080/data"