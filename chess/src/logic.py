import chess
from dataclasses import asdict
from typing import List, Tuple, Dict

from src.Data import *
from src.Models import *

X = 'abcdefgh'
Y = [x for x in range(1,9)]

class ChessLogic:

    def __init__(self, min_col = 1, min_row = 0, max_col = 8, max_row = 7, use_signle_board = False):
        self._abscent_square = None
        self._abscent_figure = None

        self.matrix_min_col = min_col
        self.matrix_min_row = min_row
        self.matrix_max_col = max_col
        self.matrix_max_row = max_row

        self.status = []
        self.promotion = False
        self.is_white_turn = True
        self.board = chess.Board()

        self.use_signle_board = use_signle_board
        
        # Отвратительный костыль но без него игра на 1 доске невозможна
        self._patience = 3
        self._current_waiting = 0
        self._same_type_capture_move = None

    def _get_available_moves(self, start_square: chess.Square)->List[chess.Move]:
        """Получить доступные ходы
        
        Args: 
            start_square (chess.Square): стартовая клетка

        Returns:
            List[chess.Move]: доступные ходы
        """
        moves = [move for move in self.board.generate_pseudo_legal_moves() if move.from_square == start_square]
        return moves

    def _validate_move(self, move: chess.Move, start_square: chess.Square) -> bool:
        """Валидация ходов
        
        Args: 
            move (chess.Move): шаг для проверки
            start_square (chess.Square): стартовая клетка

        Returns:
            bool: если ход верный
        """
        is_available = move in self._get_available_moves(start_square)
        return is_available
    
    def _update_game_status(self):
        """Обновить статусы на доске"""
        if self._abscent_figure is not None and self._abscent_square is not None:
            moves = self._get_available_moves(self._abscent_square)
            for move in moves:
                self.status.append(AvailableMovesStatus((move.to_square % 8, move.to_square // 8)))

        if self.board.is_check():
            for square in self.board.checkers():
                self.status.append(CheckStatus((square % 8, square // 8)))

        if self.board.is_checkmate():
            for square in self.board.checkers():
                self.status.append(MateStatus((square % 8, square // 8)))

        if self.board.is_stalemate():
            self.status.append(StaleMateStatus())

    def _make_move(self, move: chess.Move):
        """Делает шаг на доске
        
        Args: 
            move (chess.Move): Ход который нужно сделать
        """
        self.board.push(move)
        self._abscent_square = None
        self._abscent_figure = None
        self.is_white_turn = not self.is_white_turn   

    def find_changes(self, board: ChessBoard)->List[Tuple[chess.Square, chess.Piece, int]]:
        """Найти изменения между внешними данными и внутренней логикой
        
        Args: 
            board (ChessBoard): внешняя доска

        Returns:
            List[Tuple[chess.Square, chess.Piece, int]]: Список изменений [клекта, фигура, фигура на стенде]

        """
        changes = []
        
        for index_x, x in enumerate(X):
            for index_y, y in enumerate(Y):
                board_square = chess.parse_square(f'{x}{y}')
                board_data = self.board.piece_at(board_square)
                matrix_data = board.matrix[index_x + self.matrix_min_row][index_y + self.matrix_min_col]
                
                # если поднята фигура
                # проверить если квадрат пустой - то скипаем
                # если нет - отмена выбора
                if self._abscent_square is not None and board_square == self._abscent_square:
                    if matrix_data == self._abscent_figure:
                        self._abscent_figure = None
                        self._abscent_square = None
                    else:
                        continue

                target_color = chess.WHITE if self.is_white_turn else chess.BLACK

                if board_data is not None and (target_color != board_data.color and not self.use_signle_board) and matrix_data == 0:
                    continue

                if (board_data is None and matrix_data != 0) \
                    or (board_data is not None and matrix_data != board_data.piece_type) \
                    or (board_data is not None and (target_color != board_data.color and not self.use_signle_board)):
                    changes.append((board_square, board_data, matrix_data))

        return changes

    def parse_board(self, board: ChessBoard):
        """Парсит доску и применяет доску к внутреннему состоянию
        
        Args: 
            board: доска
        """
        self.status = []

        changes = self.find_changes(board)
        changes_made = len(changes)
        
        if changes_made == 0:
            self._update_game_status()

            if self.use_signle_board:
                self._current_waiting += 1
                if self._current_waiting > self._patience and self._same_type_capture_move:
                    self._make_move(self._same_type_capture_move)
                    self._current_waiting = 0
                    self._same_type_capture_move = None
                return
            else: 
                return

        if changes_made > 1:
            for change in changes:
                self.status.append(DesyncStatus((change[0] % 8, change[0] // 8), change[1].piece_type if change[1] is not None else change[2]))
            self._abscent_figure = None
            self._abscent_square = None
            return

        target_square, target_board_data, target_matrix_data = changes[0]
        
        if self._abscent_figure is None and self._abscent_square is None:
            if (target_board_data is None and target_matrix_data != 0) or (target_board_data is not None and target_matrix_data != target_board_data.piece_type):
                self._abscent_square = target_square
                self._abscent_figure = target_board_data.piece_type

                # костыль на сруб одной доской
                if self.use_signle_board:
                    self._current_waiting = 0
                    moves = self._get_available_moves(target_square)
                    for move in moves:
                        if self.board.is_capture(move) \
                        and self.board.piece_at(move.to_square).piece_type == target_board_data.piece_type:
                            self._same_type_capture_move = move

        else: 
            move = chess.Move(self._abscent_square, target_square) if target_matrix_data == self._abscent_figure else chess.Move(self._abscent_square, target_square, target_matrix_data) 
            
            if self._validate_move(move, self._abscent_square):
                self._make_move(move)
            else:
                self.status.append(
                    WrongMoveStatus(
                        initial_square = (self._abscent_square % 8, self._abscent_square // 8), 
                        wrong_square = (target_square % 8, target_square // 8)
                    )
                )
        
        self._update_game_status()

    def get_data(self) -> Dict:
        """Возвращает данные в json формате
        
        Returns:
            состояние логики
        """
        result = {}

        result["is_white_turn"] = self.is_white_turn

        board_matrix = [[{} for _ in range(8)] for _ in range(8)]
        for square in chess.SQUARES:
            if self.board.piece_at(square) is None:
                continue
            board_matrix[square // 8][square % 8]["piece"] = self.board.piece_at(square).piece_type
            board_matrix[square // 8][square % 8]["color"] = "white" if self.board.piece_at(square).color else "black"
        result["board"] = board_matrix

        status_dict = []
        for status in self.status:
            status_dict.append(asdict(status))
        result["status"] = status_dict
        result["is_piece_chosen"] = self._abscent_square is not None
        return result