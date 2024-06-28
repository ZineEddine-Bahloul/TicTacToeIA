import numpy as np
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def create_board():
    return np.zeros((3, 3), dtype=int)

def make_move(board, player, row, col):
    if board[row][col] == 0:
        board[row][col] = player
        return True
    return False

def check_winner(board):
    for player in [1, 2]:
        for i in range(3):
            if all([board[i][j] == player for j in range(3)]) or all([board[j][i] == player for j in range(3)]):
                return player
        if all([board[i][i] == player for i in range(3)]) or all([board[i][2-i] == player for i in range(3)]):
            return player
    return 0

def is_draw(board):
    return all([cell != 0 for row in board for cell in row])

def minimax(board, is_maximizing):
    win = check_winner(board)
    if win == 1:
        return -10
    elif win == 2:
        return 10
    elif is_draw(board):
        return 0 
    if is_maximizing:
        value = -np.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 2
                    value = max(value, minimax(board, False))
                    board[i][j] = 0
    else:
        value = np.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 1
                    value = min(value, minimax(board, True))
                    app.logger.debug(f"value: {value}")
                    app.logger.debug(f"position player 1 :{i,j}")
                    board[i][j] = 0
    return value

def best_move(board):
    best_score = -np.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = 2
                score = minimax(board, False)
                app.logger.debug(f"score: {score}")
                board[i][j] = 0
                if score == 10 :
                    return (i,j)
                elif score > best_score:
                    best_score = score
                    move = (i, j)
    return move

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    app.logger.debug(f"Received data: {data}")
    if not data or 'board' not in data or 'player' not in data:
        return jsonify({"error": "Invalid request data"}), 400

    board = np.array(data['board'])
    player = data['player']
    app.logger.debug(f"Board before move: {board}")
    app.logger.debug(f"Player: {player}")

    if player == 1:
        row = data['row']
        col = data['col']
    else:
        move = best_move(board)
        app.logger.debug(f"AI move: {move}")
        if move is None:
            return jsonify({"error": "AI move generation failed"}), 500
        make_move(board, player, move[0], move[1])
        row, col = move

    winner = check_winner(board)
    app.logger.debug(f"Board after move: {board}")
    if winner != 0:
        return jsonify({"board": board.tolist(), "winner": winner})
    elif is_draw(board):
        return jsonify({"board": board.tolist(), "winner": 0})
    return jsonify({"board": board.tolist(), "winner": None})

if __name__ == "__main__":
    app.run(debug=False)
