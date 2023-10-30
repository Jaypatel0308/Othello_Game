import o
import o_m
import tkinter

DEFAULT_ROWS = 8
DEFAULT_COLUMNS = 8
DEFAULT_FIRST_PLAYER = o.BLACK
DEFAULT_TOP_LEFT_PLAYER = o.WHITE
DEFAULT_VICTORY_TYPE = o.MOST_CELLS

# GUI Constants
BACKGROUND_COLOR = o_m.BACKGROUND_COLOR
GAME_HEIGHT = 300
GAME_WIDTH = 300

class OthelloGUI:
    def __init__(self):
        self.rows = DEFAULT_ROWS
        self.columns = DEFAULT_COLUMNS
        self.first_player = DEFAULT_FIRST_PLAYER
        self.top_left_player = DEFAULT_TOP_LEFT_PLAYER
        self.victory_type = DEFAULT_VICTORY_TYPE

        self.game_state = o.OthelloGame(self.rows, self.columns, self.first_player, self.top_left_player, self.victory_type)

        self.root_window = tkinter.Tk()
        self.root_window.title("Othello Game")
        self.root_window.configure(background = BACKGROUND_COLOR)
        self.board = o_m.GameBoard(self.game_state, GAME_WIDTH, GAME_HEIGHT, self.root_window)
        self.black_score = o_m.Score(o.BLACK, self.game_state, self.root_window)
        self.white_score = o_m.Score(o.WHITE, self.game_state, self.root_window)
        self.player_turn = o_m.Turn(self.game_state, self.root_window)

        self.board.get_board().bind('<Configure>', self.on_board_resized)
        self.board.get_board().bind('<Button-1>', self.on_board_clicked)        

        self.menu_bar = tkinter.Menu(self.root_window)
        self.game_menu = tkinter.Menu(self.menu_bar, tearoff = 0)
        self.game_menu.add_command(label = 'New Game', command = self.new_game, font=o_m.DIALOG_FONT)
        self.game_menu.add_command(label = 'Game Settings', command = self.configure_game_settings, font=o_m.DIALOG_FONT)
        self.game_menu.add_separator()
        self.game_menu.add_command(label = 'Exit', command = self.root_window.destroy, font=o_m.DIALOG_FONT)
        self.menu_bar.add_cascade(label = 'Game', menu = self.game_menu, font=o_m.FONT)
        
        self.root_window.config(menu = self.menu_bar)
        self.black_score.get_score_label().grid(row = 0, column = 0, sticky = tkinter.S)
        self.white_score.get_score_label().grid(row = 0, column = 1, sticky = tkinter.S)
        self.board.get_board().grid(row = 1, column = 0, columnspan = 2, padx = 50, pady = 10, sticky = tkinter.N + tkinter.E + tkinter.S + tkinter.W)
        self.player_turn.get_turn_label().grid(row = 2, column = 0, columnspan = 2, padx = 10, pady = 10)

        self.root_window.rowconfigure(0, weight = 1)
        self.root_window.rowconfigure(1, weight = 1)
        self.root_window.rowconfigure(2, weight = 1)
        self.root_window.columnconfigure(0, weight = 1)
        self.root_window.columnconfigure(1, weight = 1)


    def start(self) -> None:
        self.root_window.mainloop()


    def configure_game_settings(self) -> None:
        dialog = o_m.OptionDialog(self.rows, self.columns, self.first_player, self.top_left_player, self.victory_type)
        dialog.show()
        if dialog.was_ok_clicked():
            self.rows = dialog.get_rows()
            self.columns = dialog.get_columns()
            self.first_player = dialog.get_first_player()
            self.top_left_player = dialog.get_top_left_player()
            self.victory_type = dialog.get_victory_type()

            self.new_game()

    def new_game(self) -> None:
        self.game_state = o.OthelloGame(self.rows, self.columns, self.first_player, self.top_left_player, self.victory_type)
        self.board.new_game_settings(self.game_state)
        self.board.redraw_board()
        self.black_score.update_score(self.game_state)
        self.white_score.update_score(self.game_state)
        self.player_turn.update_turn(self.game_state.get_turn())

    def on_board_clicked(self, event: tkinter.Event) -> None:
        move = self.convert_point_coord_to_move(event.x, event.y)
        row = move[0]
        col = move[1]
        try:
            self.game_state.move(row, col)
            self.board.update_game_state(self.game_state)
            self.board.redraw_board()
            self.black_score.update_score(self.game_state)
            self.white_score.update_score(self.game_state)
            
            if self.game_state.is_game_over():
                self.player_turn.display_winner(self.game_state.return_winner())
            else:
                self.player_turn.switch_turn(self.game_state)
        except:
            pass

    def convert_point_coord_to_move(self, pointx: int, pointy: int) -> None:
        row = int(pointy // self.board.get_cell_height())
        if row == self.board.get_rows():
            row -= 1
        col = int(pointx // self.board.get_cell_width())
        if col == self.board.get_columns():
            col -= 1
        return (row, col)
        

    def on_board_resized(self, event: tkinter.Event) -> None:
        self.board.redraw_board()

if __name__ == '__main__':
    OthelloGUI().start()