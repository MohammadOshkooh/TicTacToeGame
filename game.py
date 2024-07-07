from time import sleep

from peer import Peer


class TicTacToe(Peer):
    def __init__(self, port, host='127.0.0.1'):
        super().__init__(port, host)
        self.board = [' ' for _ in range(9)]
        self.current_turn = 'X'
        self.my_turn = True  # Indicates whether it's the current player's turn

    def print_board(self):
        for i in range(3):
            print(f"{self.board[3 * i]} | {self.board[3 * i + 1]} | {self.board[3 * i + 2]}")
            if i < 2:
                print("---------")

    def make_move(self, position):
        """Makes a move on the board if the position is valid."""
        if self.check_winner():
            return False

        if self.board[position] == ' ':
            self.board[position] = self.current_turn
            self.current_turn = 'O' if self.current_turn == 'X' else 'X'
            self.print_board()
            return True
        else:
            print("Position already taken. Try again.")
            return False

    def check_winner(self):
        winning_positions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        for positions in winning_positions:
            if (self.board[positions[0]] == self.board[positions[1]] == self.board[positions[2]] and
                    self.board[positions[0]] != ' '):
                print(f"Player {self.board[positions[0]]} wins!")
                self.send(f"Player {self.board[positions[0]]} wins!")
                self.my_turn = True  # Game ends, no more turns
                return True
        if ' ' not in self.board:
            self.my_turn = False  # Game ends, no more turns
            return True
        return False

    def on_receive(self, data):
        print(f"Processing received move: {data}")
        if "win" in data:
            return
        try:
            position = int(data)
            self.my_turn = True
            self.make_move(position)
        except:
            pass

    def start_game(self):
        self.print_board()

        while not self.check_winner():
            if self.my_turn and not self.check_winner():
                try:
                    sleep(0.5)
                    position = int(input("Enter position (0-8): "))
                    if position < 0 or position > 8:
                        print("Invalid position. Try again.")
                        continue
                    if self.make_move(position):
                        self.send(str(position))
                        self.my_turn = False  # After making a move, it's the opponent's turn
                except ValueError:
                    print("Invalid input. Enter a number between 0 and 8.")
