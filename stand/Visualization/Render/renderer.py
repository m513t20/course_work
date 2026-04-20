import pygame

from Config import *

class Renderer:
    def __init__(self, screen):
        self.screen = screen

    def draw_board(self, state):
        self.screen.fill((0, 0, 0))

        is_white_turn = state.get("is_white_turn", True) if state else True
        turn_color = COLOR_SIDEBAR_WHITE if is_white_turn else COLOR_SIDEBAR_BLACK
        
        pygame.draw.rect(self.screen, turn_color, (0, 0, TILE_SIZE, HEIGHT))
        pygame.draw.rect(self.screen, turn_color, (9 * STEP, 0, TILE_SIZE, HEIGHT))

        for logical_row in range(ROWS):
            visual_row = 7 - logical_row
            
            for col_10x8 in range(1, 9):
                visual_col = logical_row + 1
                visual_row = col_10x8 - 1

                is_light_square = (logical_row + (col_10x8 - 1)) % 2 == 0
                color = COLOR_WHITE if not is_light_square else COLOR_BLACK

                rect_x = visual_col * STEP
                rect_y = visual_row * STEP

                pygame.draw.rect(self.screen, color, (rect_x, rect_y, TILE_SIZE, TILE_SIZE))

        if not state:
            return

        statuses = state.get("status", [])
        for status in statuses:
            desc = status.get("description", "")
            if desc not in ["availble moves", "check", "desync"]:
                continue

            sq = status.get("square") or status.get("Square")
            if not sq:
                continue

            logical_col, logical_row = sq             
            visual_col = logical_row + 1
            visual_row = 7 - logical_col

            highlight_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            
            if desc == "availble moves":
                highlight_surface.fill(COLOR_HIGHLIGHT)
            elif desc == "check":
                highlight_surface.fill(COLOR_CHECK)
            elif desc == "desync":
                highlight_surface.fill(COLOR_DESYNC)
            
            self.screen.blit(highlight_surface, (visual_col * STEP, visual_row * STEP))

            if desc == "desync" and "figure" in status:
                fig_id = status["figure"]
                text = PIECES_UNICODE["white"].get(fig_id, "?") 
                text_surface = self.font.render(text, True, (255, 0, 0)) 
                text_rect = text_surface.get_rect(center=((visual_col) * STEP + TILE_SIZE // 2, 
                                                          visual_col * STEP + TILE_SIZE // 2))
                self.screen.blit(text_surface, text_rect)

        board = state.get("board", [])
        for logical_row in range(ROWS):
            visual_row = 7 - logical_row
            
            for col_8x8 in range(8):
                
                piece_data = board[logical_row][col_8x8]
                if "piece" in piece_data:
                    visual_col = logical_row + 1
                    visual_row = 7 - col_8x8

                    p_id = piece_data["piece"]
                    p_color = piece_data["color"]
                    
                    text = PIECES_UNICODE[p_color].get(p_id, "?")
                    text_color = (0, 0, 0) if p_color == "black" else (255, 255, 255)
                    
                    text_surface = self.font.render(text, True, text_color)
                    text_rect = text_surface.get_rect(center=(visual_col * STEP + TILE_SIZE // 2, 
                                                              visual_row * STEP + TILE_SIZE // 2))
                    self.screen.blit(text_surface, text_rect)
        

        game_over_text = None
        for status in statuses:
            desc = status.get("description", "")
            if desc in ["mate", "checkmate"]:
                is_white_turn = state.get("is_white_turn", True)
                winner = "ЧЕРНЫЕ" if is_white_turn else "БЕЛЫЕ"
                game_over_text = f"МАТ! ПОБЕДИЛИ {winner}"
            elif desc in ["stalemate", "draw"]:
                game_over_text = "НИЧЬЯ!"

        if game_over_text:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)) 
            self.screen.blit(overlay, (0, 0))

            big_font = pygame.font.SysFont("Arial", 60, bold=True)
            text_surf = big_font.render(game_over_text, True, (255, 50, 50))
            text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            
            shadow_surf = big_font.render(game_over_text, True, (0, 0, 0))
            shadow_rect = shadow_surf.get_rect(center=(WIDTH // 2 + 3, HEIGHT // 2 + 3))
            
            self.screen.blit(shadow_surf, shadow_rect)
            self.screen.blit(text_surf, text_rect)
       