# Name: Muzna Maryam
# Connect 4 Game - can be played on the terminal
# Rules:
# There are 2 players "R" and "B" for red and blue respectively.
# The game board is a 6x7 grid.
# The players take turns until one player has 4 colors in a row which can be horizontally, vertically, or diagonally.


# This class represents the game board.
class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = []
        for _ in range(rows):
            row = []
            for _ in range(cols):
                row.append(" ")
            self.grid.append(row)

    # This method prints the current state of the grid to the console.
    def print_grid(self):
        print("\n\n")
        for row in self.grid:
            print(row)
        print("\n\n")

    # This method checks if the game is a draw by checking if all cells of the grid have been filled.
    def check_draw(self):
        for row in self.grid:
            for ele in row:
                if ele == " ":
                    return False
        return True

    # This method checks if the current player has won the game by
    # checking the rows, columns, and diagonals for four consecutive tokens of the same color.
    def check_win(self, r, c, player):
        # row wise
        count = 0
        for i in range(self.cols):
            if self.grid[r][i] == player:
                count += 1
            else:
                count = 0
            if count >= 4:
                return True

        # column wise
        count = 0
        for i in range(self.rows):
            if self.grid[i][c] == player:
                count += 1
            else:
                count = 0
            if count >= 4:
                return True

        # LR diagonal
        count = 0
        r_i = r
        c_i = c
        while not (r_i == (self.rows - 1) or c_i == 0):
            r_i += 1
            c_i -= 1

        while not (r_i < 0 or c_i >= self.cols):
            if self.grid[r_i][c_i] == player:
                count += 1
            else:
                count = 0
            if count >= 4:
                return True
            r_i -= 1
            c_i += 1

        # RL diagonal
        count = 0
        r_i = r
        c_i = c
        while not (r_i == (self.rows - 1) or c_i == (self.cols - 1)):
            r_i += 1
            c_i += 1

        while not (r_i < 0 or c_i < 0):
            if self.grid[r_i][c_i] == player:
                count += 1
            else:
                count = 0
            if count >= 4:
                return True
            r_i -= 1
            c_i -= 1

        return False

    # The reset() method is used to reset the game board to its initial state with all cells empty (filled with the
    # string " ").
    def reset(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col] = " "


# This function represents one turn of the game.
# The function asks the player to enter the column number (0-6) where they want to drop their colors.
def take_turn(grid, player):
    row_index = None
    while row_index == None:
        # get index from player
        col_index = input(f"Player: {player}, Enter column, or 'q' to quit, or 'r' to restart:")
        if col_index == 'q':
            exit()
        elif col_index == 'r':
            grid.reset()
            grid.print_grid()
            return take_turn(grid, player)

        try:
            col_index = int(col_index)
            if col_index < 0 or col_index >= grid.cols:
                print(f"\nPlease enter an integer in range 0 to {grid.cols}.\n")
                continue
        except:
            print("\nPlease enter an integer input.\n")
            continue

        # fill in the column
        for i in range(-1, -1 * grid.rows - 1, -1):
            if grid.grid[i][col_index] == ' ':
                grid.grid[i][col_index] = player
                row_index = i + grid.rows
                break
        if row_index == None:
            print("\nColumn full. Try again.\n")

    # check win
    win = grid.check_win(row_index, col_index, player)
    if win:
        return win, player

    # check draw
    draw = grid.check_draw()
    return draw, ""


# The function alternates between the two players and prints the state of the board after each turn.
# When the game ends, the function prints a message indicating whether the game was won by a player or ended in a draw.
def play() -> object:
    grid = Grid(6, 7)
    grid.print_grid()

    players = ["R", "B"]

    end = False
    turn = 0
    while not end:
        end, winner = take_turn(grid, players[turn])
        grid.print_grid()
        if end:
            if winner != "":
                print(f"{winner} has won the game!")
            else:
                print("Game ended. It's a draw.")
            break
        turn = (turn + 1) % 2


play()



