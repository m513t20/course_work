import json
import chess

ID_TO_FIGURE = { 1 : chess.PAWN, 2 : chess.KNIGHT, 3 : chess.BISHOP, 4 : chess.ROOK, 5 : chess.QUEEN, 6 : chess.KING, 9 : chess.ROOK}

class ChessBoard:

    def __init__(self, data_string: dict):
        board_data = data_string
        
        self.matrix = [[0] * board_data["cols"] for _ in range(board_data["rows"])]

        for square_data in board_data["matrix"]:
            col, row = square_data["cords"][0], square_data["cords"][1]
            self.matrix[row][col] = ID_TO_FIGURE[square_data["id"]]
        
    def __str__(self):
        result = ""
        for row in self.matrix:
            result += f'{row}\n'
        
        return result