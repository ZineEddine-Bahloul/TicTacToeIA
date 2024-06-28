document.addEventListener('DOMContentLoaded', () => {
    const boardElement = document.getElementById('board');
    const messageElement = document.getElementById('message');
    const resetButton = document.getElementById('reset');
    let board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ];
    let player = 1;
    let aiThinking = false;

    function createBoard() {
        boardElement.innerHTML = '';
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
                const cell = document.createElement('div');
                cell.classList.add('cell');
                cell.dataset.row = i;
                cell.dataset.col = j;
                cell.addEventListener('click', playerMove);
                boardElement.appendChild(cell);
            }
        }
    }

    function updateBoard() {
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
                const cell = document.querySelector(`.cell[data-row='${i}'][data-col='${j}']`);
                if (board[i][j] === 1) {
                    cell.textContent = 'X';
                    cell.classList.add('human');
                } else if (board[i][j] === 2) {
                    cell.textContent = 'O';
                    cell.classList.add('ai');
                } else {
                    cell.textContent = '';
                    cell.classList.remove('human', 'ai');
                }
            }
        }
    }

    function playerMove(event) {
        if (aiThinking) return; // Prevent player move while AI is thinking
        const row = parseInt(event.target.dataset.row);
        const col = parseInt(event.target.dataset.col);
        if (board[row][col] !== 0) return;

        board[row][col] = player;
        updateBoard();

        fetch('/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                board: board,
                player: player,
                row: row,
                col: col
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                messageElement.textContent = data.error;
                return;
            }
            board = data.board;
            updateBoard();
            if (data.winner !== null) {
                if (data.winner === 0) {
                    messageElement.textContent = "It's a draw!";
                } else if (data.winner === 1) {
                    messageElement.textContent = `Player ${data.winner} wins!`;
                    boardElement.classList.add('human-win');
                } else {
                    messageElement.textContent = `Player ${data.winner} wins!`;
                    boardElement.classList.add('ai-win');
                }
                disableBoard();
            } else {
                player = player === 1 ? 2 : 1;
                if (player === 2) {
                    aiMove();
                }
            }
        })
        .catch(error => {
            console.error("Error:", error);
            messageElement.textContent = "Error processing move.";
        });
    }

    function aiMove() {
        aiThinking = true; // Disable board interactions
        fetch('/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                board: board,
                player: 2
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                messageElement.textContent = data.error;
                return;
            }
            board = data.board;
            updateBoard();
            aiThinking = false; // Re-enable board interactions
            enableBoard()
            if (data.winner !== null) {
                if (data.winner === 0) {
                    messageElement.textContent = "It's a draw!";
                } else if (data.winner === 1) {
                    messageElement.textContent = `Player ${data.winner} wins!`;
                    boardElement.classList.add('human-win');
                } else {
                    messageElement.textContent = `Player ${data.winner} wins!`;
                    boardElement.classList.add('ai-win');
                }
                disableBoard();
            } else {
                player = player === 1 ? 2 : 1;
            }
        })
        .catch(error => {
            console.error("Error:", error);
            messageElement.textContent = "Error processing AI move.";
            aiThinking = false; // Re-enable board interactions even on error
        });
    }

    function disableBoard() {
        boardElement.classList.add('disabled');
    }

    function enableBoard() {
        boardElement.classList.remove('disabled');
    }

    resetButton.addEventListener('click', () => {
        board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ];
        player = 1;
        aiThinking = false;
        messageElement.textContent = '';
        boardElement.classList.remove('human-win', 'ai-win', 'disabled');
        createBoard();
        updateBoard();
    });

    createBoard();
    updateBoard();
});
