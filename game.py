import numpy as np

def create_board():
    return np.zeros((3, 3), dtype=int)

def display_board(board):
    print("-" * 10)
    for row in board:
        cmpt = 1
        for x in row:
            if x == 0:
                print(" ", end="")
            elif x == 1:
                print("X", end="")
            elif x == 2:
                print("O", end="")
            if cmpt != 3 :
                print(" | ", end="")
            cmpt += 1
        print()  # Nouvelle ligne à la fin de la rangée
        print("-" * 10)

def make_move(board, player, row, col):
    if board[row][col] == 0:
        board[row][col] = player
        return True
    return False

def check_winner(board):
    for player in [1, 2]:
        # Vérifier les lignes et les colonnes
        for i in range(3):
            if all([board[i][j] == player for j in range(3)]) or all([board[j][i] == player for j in range(3)]):
                return player
        # Vérifier les diagonales
        if all([board[i][i] == player for i in range(3)]) or all([board[i][2-i] == player for i in range(3)]):
            return player
    return 0

def is_draw(board):
    return all([cell != 0 for row in board for cell in row])

def minimax(board, is_maximizing):
    win = check_winner(board)
    if win == 0 :
        return 0 
    elif win == 1 or win == 2 :
        return 1
    if is_maximizing :
        value = -np.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 1
                    value = max(value, minimax(board,False))
                    board[i][j] = 0
    else :
        value = np.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 2
                    value = min(value, minimax(board,True))
                    board[i][j] = 0
    return value

def best_move(board) :
    best_score = -np.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = 2
                score = minimax(board,  False)
                board[i][j] = 0
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

# MAIN : 
def main():
    board = create_board()
    game_over = False
    player_turn = 1

    while not game_over:
        display_board(board)
        if player_turn == 1:
            row, col = map(int, input("Enter your move (row col): ").split())
            if not make_move(board, player_turn, row, col):
                print("Invalid move, try again.")
                continue
        else:
            move = best_move(board)
            make_move(board, player_turn, move[0], move[1])

        winner = check_winner(board)
        if winner != 0:
            display_board(board)
            print(f"Player {winner} wins!")
            game_over = True
        elif is_draw(board):
            display_board(board)
            print("It's a draw!")
            game_over = True
        else:
            player_turn = 2 if player_turn == 1 else 1

if __name__ == "__main__":
    main()
