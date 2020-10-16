import random

# Constants with columns & strings
ABC = ['A', 'B', 'C']
NUMBERS = [str(number) for number in range(1, 4)]

# We use log to check who made the last turn and how many turns were made in total
log = []


class Board:
    class Cell:
        def __init__(self, x, y):
            self.x = x  # Position in string
            self.y = y  # Position in column
            self.value = '-'

            # marked becomes True when player put own sign in the cell
            self.marked = False

            # List of lines where the cell is located
            self.on_lines = []

        def __str__(self):
            return self.value

        def free_lines(self):
            result = 0
            for line in self.on_lines:
                if line.free:
                    result += 1
            return result

        def lines_occupied(self):
            return len(self.on_lines)

        def mark(self, sign):
            if sign in ('X', 'O'):
                # Put the sign
                self.value = sign
                self.marked = True

                # Update counters and other attributes of the lines with the cell
                for line in self.on_lines:
                    line.update()
            else:
                raise ValueError

    class Line:
        def __init__(self, c1, c2, c3):
            # Adding cells included in the line
            self.cells = (c1, c2, c3)

            # The line adds itself to the list self.on_lines of each cell
            for cell in self.cells:
                cell.on_lines.append(self)

            # free is True only when there are no marked cells
            self.free = True

            # When the line is crossed out this attribute takes the winning sign as its value
            self.crossed_out = False

            # This is True when ever cell on the line is marked
            self.full = False

            # Indicators that show how many cells are marked on the line
            self.counter = {'X': 0, 'O': 0}

        # String with values of every cell on the line. Used for displaying the Board
        def show(self):
            output = ''
            for cell in self.cells:
                output += f'{cell.value} '
            return output

        # Updates attributes after marking of any cell on line
        def update(self):
            # Reset values
            for key in self.counter.keys():
                self.counter[key] = 0

            # Count marked cells
            for cell in self.cells:
                if cell.marked is True:
                    self.counter[cell.value] += 1
                    self.free = False

            # Check if line is crossed out
            for sign, number in self.counter.items():
                if number == 3:
                    self.crossed_out = sign

            # Check if there are no free cells
            if sum(self.counter.values()) == 3:
                self.full = True

    def __init__(self):
        # Create cells, fill dictionary by strings with coodrinates as key and Cell object as value
        self.cells = {}
        for x in ABC:
            for y in NUMBERS:
                self.cells.update({x + y: self.Cell(x, y)})

        # Create lines
        def diagonal(nums):
            return self.Line(*[self.cells[x + y] for x, y in zip(ABC, nums)])
        self.lines = {
            'horizontal': [],
            'vertical': [],
            'diagonal': [diagonal(NUMBERS), diagonal(reversed(NUMBERS))]
        }
        for y in NUMBERS:
            self.lines['horizontal'].append(self.Line(*[self.cells[x + y] for x in ABC]))
        for x in ABC:
            self.lines['vertical'].append(self.Line(*[self.cells[x + y] for y in NUMBERS]))

    def __str__(self):
        output = '\n  A B C'
        for n in range(3):
            output += f"\n{n + 1} {self.lines['horizontal'][n].show()}"
        return output


class Player:
    # Tuple for storing signs
    signs = ('X', "O")

    # List for the player to take one of the signs
    available_signs = list(signs)

    def __init__(self, sign=None, initial_board=None):
        # to access the board
        self.board = initial_board

        # we specify the sign as a parameter if the user has selected something
        if sign:
            if sign in self.signs:
                self.sign = sign
                self.available_signs.remove(sign)
            else:
                raise ValueError
        # Otherwise, we take the signs in order from the remaining ones
        else:
            self.sign = self.available_signs.pop()

        # Check what is our sign and give another for enemy's attribute which used for making decisions
        self.enemy_sign = self.signs[1] if self.sign == self.signs[0] else self.signs[0]

    # we mark the selected cell with our sign
    def turn(self, key):
        self.board.cells[key].mark(self.sign)
        log.append((self.sign, key))

    # Returns a list with unmarked cells for making decision
    def check_available_cells(self):
        available_cells = []
        for cell_id, cell in self.board.cells.items():
            if not cell.marked:
                available_cells.append(cell_id)
        return available_cells

    # Simple random decision
    def random_decision(self):
        self.turn(random.choice(self.check_available_cells()))

    # Smart decision-making algorithm
    def smart_decision(self):
        available_cells = self.check_available_cells()

        # Dictionary with first priorities
        priorities = {
            1: [],  # leads to victory
            2: [],  # prevents opponent's victory
            3: []   # corner cells located on empty lines
        }

        # Dictionary with ratings of every available cell
        rating = {}
        for cell_id in available_cells:
            rating[cell_id] = 0

        for cell_id in available_cells:
            cell = self.board.cells[cell_id]

            if cell.lines_occupied() == 3 and cell.free_lines() == 3:
                priorities[3].append(cell_id)

            # Checking each line where the cell is located
            for line in cell.on_lines:
                # Priority 1: cells which lead to victory
                if line.counter[self.sign] == 2:
                    priorities[1].append(cell_id)
                    break

                # Priority 2: cells which prevent opponent;s victory
                elif line.counter[self.enemy_sign] == 2:
                    priorities[2].append(cell_id)
                    break

                # Count rating of every available cell
                else:
                    # +1 for each free line
                    if line.free:
                        rating[cell_id] += 1

                    # +1 for each line with free cells
                    elif not line.full:
                        rating[cell_id] += 1

                        # +1 for each line where there is a cell with player's sign
                        if line.counter[self.sign] == 1:
                            rating[cell_id] += 1

        # If some priority list is not empty take random cell from that
        for priority in priorities.values():
            if priority:
                self.turn(random.choice(priority))
                break

        # Or take One of the cells with the highest rating
        else:
            max_rating_cells = []
            for k, v in rating.items():
                if v == max(rating.values()):
                    max_rating_cells.append(k)
            self.turn(random.choice(max_rating_cells))


class Game:
    modes = {
        1: 'cross (X)',
        2: 'zeros (O)',
        3: 'PC vs PC'
    }

    def __init__(self, brd):
        self.board = brd
        self.winning_sign = None

    # Gameplay :)
    def play(self, mode):
        # Define players and their own signs
        if mode == 'PC vs PC':
            user = Player(initial_board=self.board)
        else:
            if mode == 'cross (X)':
                user = Player('X', self.board)
            else:
                user = Player('O', self.board)

            # Show message who turns first
            show_message(f"\n{'You make' if user.sign == 'X' else 'PC makes'} the first turn!")
        pc = Player(initial_board=self.board)
        # Show board if game works in console
        if __name__ == '__main__':
            print(self.board)
        # Main process
        while not self.is_over():
            # First player;s turn
            if not log and user.sign == 'X' or log and log[-1][0] == pc.sign:
                if mode == 'PC vs PC':
                    user.smart_decision()
                    show_message(f"\n{user.sign}'s turn: {log[-1][1]}")
                else:
                    user.turn(input_cell())
            # Second player's turn
            else:
                pc.smart_decision()
                show_message(f"\n{'PC' if mode != 'PC vs PC' else pc.sign}'s turn: {log[-1][1]}")

            # Show board in console
            if __name__ == '__main__':
                print(self.board)

        # If draw game
        if not game.winning_sign:
            show_message('\nDraw game! No available cells.')
        # Show winner
        else:
            if mode == 'PC vs PC':
                show_message(f'\n{game.winning_sign} won!')
            else:
                show_message(f'\nYou {"won" if user.sign == game.winning_sign else "lost"}!')
        show_message('Game over!')

    def is_over(self):
        # Check for not marked cells
        for cell in self.board.cells.values():
            if cell.marked is False:
                break
        else:
            return True

        # Check if there are crossed out line
        for category in self.board.lines.values():
            for line in category:
                if line.crossed_out:
                    self.winning_sign = line.crossed_out
                    return True
        else:
            return False


# Create required objects
board = Board()
game = Game(board)

if __name__ == '__main__':
    # Functions instead of print/input to use from Game object
    def show_message(message):
        print(message)

    def input_cell():
        while True:
            selected_cell = input('\nYour turn: ').upper()
            # Check if input is correct
            if selected_cell not in board.cells.keys():
                print('Wrong value. Try again!')
            elif board.cells[selected_cell].marked:
                print('This cell is already filled. Try again.')
            else:
                return selected_cell

    # Greeting
    print("Hello! Let's play TIC-TAC-TOE!\nChoose who will you play for:")
    for (k, v) in game.modes.items():
        print(f'   {k} - {v}')

    # Choose mode
    user_choice = ''
    while user_choice not in game.modes.keys():
        try:
            user_choice = int(input('Your choice: '))
        except ValueError:
            print('Value error!')

    # Start the game
    game.play(game.modes[user_choice])
