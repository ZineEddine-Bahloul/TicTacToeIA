import numpy as np

def create_board():
    return np.zeros((3, 3), dtype=int)

def display_board(board):
    print("-" * 13)
    for row in board:
        for x in row:
            print("|", end="")
            if x == 0:
                print(" ", end="")
            elif x == 1:
                print(" X ", end="")
            elif x == 2:
                print(" O ", end="")
        print()  # Nouvelle ligne à la fin de la rangée
        print("-" * 13)

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

def minimax(board, depth, is_maximizing):
    # to complete 
    return
def best_move(board):
    # to complete 
    return

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
            # move = best_move(board)
            # make_move(board, player_turn, move[0], move[1])
            row, col = map(int, input("Enter your move (row col): ").split())
            if not make_move(board, player_turn, row, col):
                print("Invalid move, try again.")
                continue
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
