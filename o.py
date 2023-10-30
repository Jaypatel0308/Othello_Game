NONE = '.'
BLACK = 'B'
WHITE = 'W'
MOST_CELLS = 'M'
LEAST_CELLS = 'L'

class InvalidMoveException(Exception):
    pass

# The Othello class that manages the game
class OthelloGame:
    
    def __init__(self, rows: int, cols: int, turn: str,top_left: str, victory_type: str):
        self.rows = rows
        self.cols = cols
        self.current_board = self.new_game_board(rows, cols, top_left)
        self.turn = turn
        self.victory_type = victory_type


    def new_game_board(self, rows: int, cols: int, top_left: str) -> [[str]]:
        board =[]

        for row in range(rows):
            board.append([])
            for col in range(cols):
                board[-1].append(NONE)
                
        board[rows // 2 - 1][cols // 2 - 1] = top_left
        board[rows // 2 - 1][cols // 2] = self.opposite_turn(top_left)
        board[rows // 2][cols // 2 - 1] = self.opposite_turn(top_left)
        board[rows // 2][cols // 2] = top_left
        
        return board
    
    def move(self, row: int, col: int):
        self.require_valid_empty_space_to_move(row, col)
        possible_directions = self.adjacent_opposite_color_directions(row, col, self.turn)
        next_turn = self.turn
        
        for direction in possible_directions:
            if self.is_valid_directional_move(row, col, direction[0], direction[1], self.turn):
                next_turn = self.opposite_turn(self.turn)
            self.convert_adjacent_cells_in_direction(row, col, direction[0], direction[1], self.turn)
            
        if next_turn != self.turn:
            self.current_board[row][col] = self.turn
            if self.can_move(next_turn):
                self.switch_turn()
        else:
            raise InvalidMoveException()


    def is_valid_directional_move(self, row: int, col: int, rowdelta: int, coldelta: int, turn: str) -> bool:
        current_row = row + rowdelta
        current_col = col + coldelta

        last_cell_color = self.opposite_turn(turn)

        while True:
            if not self.is_valid_cell(current_row, current_col):
                break
            if self.cell_color(current_row, current_col) == NONE:
                break           
            if self.cell_color(current_row, current_col) == turn:
                last_cell_color = turn
                break

            current_row += rowdelta
            current_col += coldelta
            
        return last_cell_color == turn


    def adjacent_opposite_color_directions(self, row: int, col: int, turn: str) -> [tuple]:
        dir_list = []
        for rowdelta in range(-1, 2):
            for coldelta in range(-1, 2):
                if self.is_valid_cell(row+rowdelta, col + coldelta):
                    if self.current_board[row + rowdelta][col + coldelta] == self.opposite_turn(turn):
                        dir_list.append((rowdelta, coldelta))
        return dir_list
           

    def convert_adjacent_cells_in_direction(self, row: int, col: int,rowdelta: int, coldelta: int, turn: str):
        if self.is_valid_directional_move(row, col, rowdelta, coldelta, turn):
            current_row = row + rowdelta
            current_col = col + coldelta
            
            while self.cell_color(current_row, current_col) == self.opposite_turn(turn):
                self.flip_cell(current_row, current_col)
                current_row += rowdelta
                current_col += coldelta

    def is_game_over(self) -> bool:
        return self.can_move(BLACK) == False and self.can_move(WHITE) == False


    def can_move(self, turn: str) -> bool:
        for row in range(self.rows):
            for col in range(self.cols):
                if self.current_board[row][col] == NONE:
                    for direction in self.adjacent_opposite_color_directions(row, col, turn):
                        if self.is_valid_directional_move(row, col, direction[0], direction[1], turn):
                            return True
        return False

    def return_winner(self) -> str:
        black_cells = self.get_total_cells(BLACK)
        white_cells = self.get_total_cells(WHITE)

        if black_cells == white_cells:
            return None
        elif self.victory_type == MOST_CELLS:
            if black_cells > white_cells:
                return BLACK
            else:
                return WHITE
        else:
            if black_cells < white_cells:
                return BLACK
            else:
                return WHITE
            
    def switch_turn(self):
        self.turn = self.opposite_turn(self.turn)

    def get_board(self) -> [[str]]:
        return self.current_board

    def get_rows(self) -> int:
        return self.rows

    def get_columns(self) -> int:
        return self.cols

    def get_turn(self) -> str:
        return self.turn

    def get_total_cells(self, turn: str) -> int:
        total = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.current_board[row][col] == turn:
                    total += 1
        return total
    
    def flip_cell(self, row: int, col: int):
        self.current_board[row][col] = self.opposite_turn(self.current_board[row][col])


    def cell_color(self, row: int, col: int) -> str:
        return self.current_board[row][col]
        

    def opposite_turn(self, turn: str) -> str:
        return {BLACK: WHITE, WHITE: BLACK}[turn]

    def require_valid_empty_space_to_move(self, row: int, col: int) -> bool:
        if self.is_valid_cell(row, col) and self.cell_color(row, col) != NONE:
            raise InvalidMoveException()

    def is_valid_cell(self, row: int, col: int) -> bool:
        return self.is_valid_row_number(row) and self.is_valid_col_number(col)

    def is_valid_row_number(self, row: int) -> bool:
        return 0 <= row < self.rows

    def is_valid_col_number(self, col: int) -> bool:
        return 0 <= col < self.cols