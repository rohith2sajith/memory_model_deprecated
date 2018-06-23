class Maze(object):
    def __init__(self,board):
        self.board = board
        self.setup_maze(self.board)

    def setup_maze(self,board):
        for k in range(12):
            board[k][0].is_travellable = True

        for m in range(19):
            board[29][m + 11].is_travellable = True

        board[26][27].is_travellable = True
        board[26][28].is_travellable = True
        board[26][29].is_travellable = True
        board[27][27].is_travellable = True
        board[27][28].is_travellable = True
        board[27][29].is_travellable = True
        board[28][27].is_travellable = True
        board[28][28].is_travellable = True
        board[28][29].is_travellable = True

        for a in range(3):
            for b in range(12):
                board[b + 6][a + 4].is_travellable = True

        for a in range(2):
            for b in range(15):
                board[a + 22][b + 4].is_travellable = True

        for a in range(5):
            for b in range(8):
                board[b + 15][a + 22].is_travellable = True

        for a in range(3):
            for b in range(6):
                board[a + 15][b + 13].is_travellable = True

        for a in range(4):
            for b in range(7):
                board[a + 6][b + 13].is_travellable = True

        for a in range(1):
            for b in range(7):
                board[a + 6][b + 20].is_travellable = True

        for a in range(2):
            for b in range(6):
                board[b][a + 25].is_travellable = True

        for a in range(1):
            for b in range(6):
                board[a + 24][b + 4].is_travellable = True

        for a in range(2):
            for b in range(3):
                board[a + 21][b + 27].is_travellable = True

        for a in range(1):
            for b in range(4):
                board[a + 23][b + 22].is_travellable = True

        for a in range(2):
            for b in range(4):
                board[a + 16][b].is_travellable = True

        for a in range(2):
            for b in range(3):
                board[b + 18][a].is_travellable = True


