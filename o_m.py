import o
import tkinter

BACKGROUND_COLOR = '#696969'
GAME_COLOR = '#C4A484'
FONT = ('Comic sans ms', 30)
DIALOG_FONT = ('Comic sans ms', 20)
PLAYERS = {o.BLACK: 'Black', o.WHITE: 'White'}
VICTORY_TYPES = {o.MOST_CELLS: 'Most Cells', o.LEAST_CELLS: 'Least Cells'}

class GameBoard:
    def __init__(self, game_state: o.OthelloGame, game_width: float, game_height: float, root_window):
        self.game_state = game_state
        self.rows = self.game_state.get_rows()
        self.cols = self.game_state.get_columns()
        self.board = tkinter.Canvas(master = root_window, width = game_width, height = game_height, background = GAME_COLOR)

    def new_game_settings(self, game_state):
        self.game_state = game_state
        self.rows = self.game_state.get_rows()
        self.cols = self.game_state.get_columns()

    def redraw_board(self):
        self.board.delete(tkinter.ALL)
        self.redraw_lines()
        self.redraw_cells()

    def redraw_lines(self):
        row_multiplier = float(self.board.winfo_height()) / self.rows
        col_multiplier = float(self.board.winfo_width()) / self.cols
        
        for row in range(1, self.rows):
            self.board.create_line(0, row * row_multiplier, self.get_board_width(), row * row_multiplier)

        for col in range(1, self.cols):
            self.board.create_line(col * col_multiplier, 0, col * col_multiplier, self.get_board_height())

    def redraw_cells(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.game_state.get_board()[row][col] != o.NONE:
                    self.draw_cell(row, col)
                
    def draw_cell(self, row: int, col: int):
        self.board.create_oval(col * self.get_cell_width(), row * self.get_cell_height(), (col + 1) * self.get_cell_width(), (row + 1) * self.get_cell_height(), fill = PLAYERS[self.game_state.get_board()[row][col]])                               

    def update_game_state(self, game_state: o.OthelloGame):
        self.game_state = game_state

    def get_cell_width(self) -> float:
        return self.get_board_width() / self.get_columns()

    def get_cell_height(self) -> float:
        return self.get_board_height() / self.get_rows()

    def get_board_width(self) -> float:
        return float(self.board.winfo_width())

    def get_board_height(self) -> float:
        return float(self.board.winfo_height())

    def get_rows(self) -> int:
        return self.rows

    def get_columns(self) -> int:
        return self.cols

    def get_board(self) -> tkinter.Canvas:
        return self.board


class Score:
    def __init__(self, color: str, game_state: o.OthelloGame, root_window):
        self.player = color
        self.score = game_state.get_total_cells(self.player)
        self.score_label = tkinter.Label(master = root_window,text = self.score_text(),background = BACKGROUND_COLOR, fg = PLAYERS[color],font = FONT)

    def update_score(self, game_state: o.OthelloGame):
        self.score = game_state.get_total_cells(self.player)
        self.change_score_text()

    def get_score_label(self) -> tkinter.Label:
        return self.score_label

    def get_score(self) -> int:
        return self.score

    def change_score_text(self):
        self.score_label['text'] =  self.score_text()

    def score_text(self) -> str:
        return PLAYERS[self.player] + ' - ' + str(self.score)


class Turn:
    def __init__(self, game_state: o.OthelloGame, root_window):
        self.player = game_state.get_turn()
        self.turn_label = tkinter.Label(master = root_window,text = self.turn_text(),background = BACKGROUND_COLOR, fg = PLAYERS[self.player],font = FONT)

    def display_winner(self, winner: str):
        if winner == None:
            victory_text = 'Tie game. Nobody wins!'
            text_color = 'BLACK'
        else:
            victory_text = PLAYERS[winner] + ' player wins!'
            text_color = PLAYERS[winner]
        self.turn_label['text'] = victory_text
        self.turn_label['fg'] = text_color

    def switch_turn(self, game_state: o.OthelloGame):
        self.player = game_state.get_turn()
        self.change_turn_text()

    def change_turn_text(self):
        self.turn_label['text'] = self.turn_text()
        self.turn_label['fg'] = PLAYERS[self.player]

    def get_turn_label(self):
        return self.turn_label

    def update_turn(self, turn: str):
        self.player = turn
        self.change_turn_text()

    def turn_text(self):
        return PLAYERS[self.player] + " player's turn"

    def opposite_turn(self):
        return {o.BLACK: o.WHITE, o.WHITE: o.BLACK}[self.player]

class OptionDialog:
    def __init__(self, current_rows, current_columns, current_first_player,current_top_left_player, current_victory_type):
        self.dialog_window = tkinter.Toplevel()
        self.row_column_option_list = (4, 6, 8, 10 ,12, 14, 16)
        self.player_option_list = ('Black', 'White')
        self.victory_option_list = ('Most Cells', 'Least Cells')

        self.rows = current_rows
        self.columns = current_columns
        self.first_player = current_first_player
        self.top_left_player = current_top_left_player
        self.victory_type = current_victory_type
        
        self.row_frame = tkinter.Frame(master = self.dialog_window)
        self.row_label = tkinter.Label(master = self.row_frame,text = 'Rows:',font = DIALOG_FONT)
        self.row_label.grid(row = 0, column = 0, sticky = tkinter.E,padx = 10, pady = 10)
        self.rows = tkinter.IntVar()
        self.rows.set(current_rows)
        self.row_option_menu = tkinter.OptionMenu(self.row_frame,self.rows,*self.row_column_option_list)
        self.row_option_menu.grid(row = 0, column = 1, sticky = tkinter.W,padx = 10, pady = 10)
        self.row_frame.grid(row = 0, column = 0, sticky = tkinter.W,padx = 10, pady = 10)
        
        self.column_frame = tkinter.Frame(master = self.dialog_window)
        self.column_label = tkinter.Label(master = self.column_frame,text = 'Columns:',font = DIALOG_FONT)
        self.column_label.grid(row = 0, column = 0, sticky = tkinter.E,padx = 10, pady = 10)
        self.columns = tkinter.IntVar()
        self.columns.set(current_columns)
        self.column_option_menu = tkinter.OptionMenu(self.column_frame,self.columns, *self.row_column_option_list)
        self.column_option_menu.grid(row = 0, column = 1, sticky = tkinter.W, padx = 10, pady = 10)
        self.column_frame.grid(row = 0, column = 1, sticky = tkinter.W, padx = 10, pady = 10)

        self.first_player_frame = tkinter.Frame(master = self.dialog_window)
        self.first_player_label = tkinter.Label(master = self.first_player_frame, text = 'First player:', font = DIALOG_FONT)
        self.first_player_label.grid(row = 0, column = 0, sticky = tkinter.E, padx = 10, pady = 10)
        self.first_players = tkinter.StringVar()
        self.first_players.set(PLAYERS[current_first_player])
        self.first_player_option_menu = tkinter.OptionMenu(self.first_player_frame, self.first_players, *self.player_option_list)
        self.first_player_option_menu.grid(row = 0, column = 1, sticky = tkinter.W, padx = 10, pady = 10)
        self.first_player_frame.grid(row = 1, column = 0, sticky = tkinter.W, padx = 10, pady = 10)
        
        self.victory_type_frame = tkinter.Frame(master = self.dialog_window)
        self.victory_type_label = tkinter.Label(master = self.victory_type_frame, text = 'Victory type:', font = DIALOG_FONT)
        self.victory_type_label.grid(row = 0, column = 0, sticky = tkinter.E, padx = 10, pady = 10)
        self.victory_types = tkinter.StringVar()
        self.victory_types.set(VICTORY_TYPES[current_victory_type])
        self.victory_type_option_menu = tkinter.OptionMenu(self.victory_type_frame, self.victory_types, *self.victory_option_list)
        self.victory_type_option_menu.grid(row = 0, column = 1, sticky = tkinter.W, padx = 10, pady = 10)
        self.victory_type_frame.grid(row = 1, column = 1, sticky = tkinter.W, padx = 10, pady = 10)
        
        self.top_left_player_frame = tkinter.Frame(master = self.dialog_window)
        self.top_left_player_label = tkinter.Label(master = self.top_left_player_frame, text = 'Top-left center position:', font = DIALOG_FONT)
        self.top_left_player_label.grid(row = 0, column = 0, sticky = tkinter.E, padx = 10, pady = 10)
        self.top_left_players = tkinter.StringVar()
        self.top_left_players.set(PLAYERS[current_top_left_player])
        self.top_left_player_option_menu = tkinter.OptionMenu(self.top_left_player_frame, self.top_left_players, *self.player_option_list)
        self.top_left_player_option_menu.grid(row = 0, column = 1, sticky = tkinter.W, padx = 10, pady = 10)
        self.top_left_player_frame.grid(row = 2, column = 0, columnspan = 2, sticky = tkinter.W, padx = 10, pady = 10)

        self.button_frame = tkinter.Frame(master = self.dialog_window)
        self.button_frame.grid(row = 3, column = 1, sticky = tkinter.E, padx = 10, pady = 10)
        
        self.ok_button = tkinter.Button(master = self.button_frame, text = 'OK', font = DIALOG_FONT, command = self.on_ok_button)
        self.ok_button.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.cancel_button = tkinter.Button(master = self.button_frame, text = 'Cancel', font = DIALOG_FONT, command = self.on_cancel_button)
        self.cancel_button.grid(row = 0, column = 1, padx = 10, pady = 10)
        
        self.dialog_window.rowconfigure(0, weight = 1)
        self.dialog_window.rowconfigure(1, weight = 1)
        self.dialog_window.rowconfigure(2, weight = 1)
        self.dialog_window.rowconfigure(3, weight = 1)
        self.dialog_window.columnconfigure(0, weight = 1)
        self.dialog_window.columnconfigure(1, weight = 1)

        self.ok_clicked = False


    def show(self):
        self.dialog_window.grab_set()
        self.dialog_window.wait_window()

    def was_ok_clicked(self) -> bool:
        return self.ok_clicked

    def get_rows(self) -> int:
        return self.rows

    def get_columns(self) -> int:
        return self.columns

    def get_first_player(self) -> str:
        return self.first_player[0]

    def get_top_left_player(self) -> str:
        return self.top_left_player[0]

    def get_victory_type(self) -> str:
        return self.victory_type[0]
    
    def on_ok_button(self):
        self.ok_clicked = True
        self.rows = self.rows.get()
        self.columns = self.columns.get()
        self.first_player = self.first_players.get()
        self.top_left_player = self.top_left_players.get()
        self.victory_type = self.victory_types.get()
        self.dialog_window.destroy()

    def on_cancel_button(self):
        self.dialog_window.destroy()