import arcade

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
CELL_SIZE = 100
GRID_ROWS = 3
GRID_COLS = 3

# Game state
EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2
current_player = PLAYER_X
game_board = [[EMPTY for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
winner = None


def draw_board():
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            arcade.draw_rectangle_outline(x + CELL_SIZE // 2, y + CELL_SIZE // 2, CELL_SIZE, CELL_SIZE, arcade.color.BLACK)
            if game_board[row][col] == PLAYER_X:
                draw_x(x, y)
            elif game_board[row][col] == PLAYER_O:
                draw_o(x, y)


def draw_x(x, y):
    arcade.draw_line(x + 10, y + 10, x + CELL_SIZE - 10, y + CELL_SIZE - 10, arcade.color.BLACK, 2)
    arcade.draw_line(x + CELL_SIZE - 10, y + 10, x + 10, y + CELL_SIZE - 10, arcade.color.BLACK, 2)


def draw_o(x, y):
    radius = (CELL_SIZE // 3) * 1.4  # Make the circle 1.4 times bigger
    arcade.draw_circle_outline(x + CELL_SIZE // 2, y + CELL_SIZE // 2, radius, arcade.color.BLACK, 2)


def check_winner():
    global winner
    for row in range(GRID_ROWS):
        if game_board[row][0] == game_board[row][1] == game_board[row][2] != EMPTY:
            winner = game_board[row][0]
            return True

    for col in range(GRID_COLS):
        if game_board[0][col] == game_board[1][col] == game_board[2][col] != EMPTY:
            winner = game_board[0][col]
            return True

    if game_board[0][0] == game_board[1][1] == game_board[2][2] != EMPTY:
        winner = game_board[0][0]
        return True

    if game_board[0][2] == game_board[1][1] == game_board[2][0] != EMPTY:
        winner = game_board[0][2]
        return True

    # Check for draw
    if all(game_board[row][col] != EMPTY for row in range(GRID_ROWS) for col in range(GRID_COLS)):
        winner = 0
        return True

    return False


class TicTacToe(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.WHITE)

    def on_mouse_press(self, x, y, button, modifiers):
        global winner
        if winner is None:
            row = y // CELL_SIZE
            col = x // CELL_SIZE
            if game_board[row][col] == EMPTY:
                global current_player
                game_board[row][col] = current_player
                current_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X
                if check_winner():
                    return
                if all(cell != EMPTY for row in game_board for cell in row):
                    # If all cells are filled and there's no winner, it's a draw
                    self.on_draw()

    def on_draw(self):
        arcade.start_render()
        draw_board()
        if winner is not None:
            self.draw_result_screen()

    def draw_result_screen(self):
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, arcade.color.WHITE)
        if winner == 0:
            arcade.draw_text("It's a draw!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30, arcade.color.BLACK, font_size=20, anchor_x="center")
        else:
            arcade.draw_text(f"Player {winner} wins!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30, arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Press 'R' to play again", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40, arcade.color.BLACK, font_size=16, anchor_x="center")

    def on_key_press(self, key, modifiers):
        global winner
        if winner is not None and key == arcade.key.R:
            # Reset the game when 'R' is pressed
            self.reset_game()

    def reset_game(self):
        global game_board, current_player, winner
        game_board = [[EMPTY for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        current_player = PLAYER_X
        winner = None


def main():
    TicTacToe(SCREEN_WIDTH, SCREEN_HEIGHT, "Tic Tac Toe")
    arcade.run()


if __name__ == "__main__":
    main()
