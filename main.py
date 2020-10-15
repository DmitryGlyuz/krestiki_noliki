import random

# Constants with columns
ABC = ['A', 'B', 'C']
# And strings
NUMBERS = [str(number) for number in range(1, 4)]


class Board:
    class Cell:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.value = '-'
            self.marked = False
            self.on_lines = []

        def __str__(self):
            return self.value

        def mark(self, sign):
            if sign in ('X', 'O'):
                self.value = sign
                self.marked = True
                for line in self.on_lines:
                    line.update()
            else:
                raise ValueError

    class Line():
        def __init__(self, c1, c2, c3):
            self.c1 = c1
            self.c2 = c2
            self.c3 = c3
            self.free = True
            self.cells = (self.c1, self.c2, self.c3)
            self.ids = ''
            for cell in self.cells:
                self.ids += f'{cell.x}{cell.y} '
                cell.on_lines.append(self)
            self.crossed_out = False
            self.crossed_by = None
            self.full = False
            self.counter = {
                'X': 0,
                'O': 0
            }

        def show(self):
            return f'{self.c1} {self.c2} {self.c3}'

        def update(self):
            for key in self.counter.keys():
                self.counter[key] = 0
            for cell in self.cells:
                if cell.marked is True:
                    self.counter[cell.value] += 1
                    self.free = False
            for sign, number in self.counter.items():
                if number == 3:
                    self.crossed_out = True
                    self.crossed_by = sign
            if sum(self.counter.values()) == 3:
                self.full = True

    def __init__(self):
        # Create cells
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
    signs = ('X', "O")
    available_signs = list(signs)
    log = []

    def __init__(self, sign=None, area=None):
        self.board = area

        if sign:
            if sign in self.signs:
                self.sign = sign
                self.available_signs.remove(sign)
            else:
                raise ValueError

        else:
            self.sign = self.available_signs.pop()
        self.enemy_sign = self.signs[1] if self.sign == self.signs[0] else self.signs[0]

    def turn(self, key):
        self.board.cells[key].mark(self.sign)
        self.log.append((self.sign, key))

    def check_available_cells(self):
        available_cells = []
        for id, cell in self.board.cells.items():
            if not cell.marked:
                available_cells.append(id)
        return available_cells

    def random_decision(self):
        self.turn(random.choice(self.check_available_cells()))

    def smart_decision(self):
        available_cells = self.check_available_cells()
        # print(f'Доступные ячейки:\n {available_cells}\nПроверяю каждую.')
        # Dictionary with priorities
        priorities = {
            1: [],  # leads to victory
            2: [],  # prevents opponent's victory
        }
        rating = {}
        for cell_id in available_cells:
            rating[cell_id] = 0

        for cell_id in available_cells:
            free_lines = 0
            cell = self.board.cells[cell_id]
            # print(f'\nЯчейка {cell_id}:\nНаходится на линиях {[line.ids for line in board.cells[cell_id].on_lines]}')
            for line in cell.on_lines:
                if line.counter[self.sign] == 2:
                    priorities[1].append(cell_id)
                    break
                elif line.counter[self.enemy_sign] == 2:
                    priorities[2].append(cell_id)
                    break
                else:
                    if line.free:
                        rating[cell_id] += 1
                        free_lines += 1
                    if not line.full:
                        rating[cell_id] += 1
                        if line.counter[self.sign] == 1:
                            rating[cell_id] += 1
            if len(cell.on_lines) == 3 and free_lines == 3:
                rating[cell_id] += 3

        if priorities[1]:
            self.turn(random.choice(priorities[1]))
        elif priorities[2]:
            self.turn(random.choice(priorities[2]))
        else:
            max_rating = max(rating.values())
            max_rating_cells = []
            for k, v in rating.items():
                if v == max_rating:
                    max_rating_cells.append(k)
            self.turn(random.choice(max_rating_cells))


class Game:
    def __init__(self, brd):
        self.board = brd
        self.winning_sign = None
        pass

    def is_over(self):
        for cell in self.board.cells.values():
            if cell.marked is False:
                break
        else:
            return True

        for category in self.board.lines.values():
            for line in category:
                if line.crossed_out:
                    self.winning_sign = line.crossed_by
                    return True
        else:
            return False

    def info(self):
        print('Horizontal:')
        for (k, v) in board.lines.items():
            print(f'{k.title()}:')
            for line in v:
                print(f'{line.ids} - {"free" if line.free else "not free"}')


#         # Add cells which lead to victory to list with the first priority, don't scan nothing else
#         # Add cells which prevent opponent's victory
#         # Take random cell from priorities[1]
#     # Else if this list is not empty
#         # Take random cell from priorities[2]
if __name__ == '__main__':

    # Greeting
    print("Hello! Let's play TIC-TAC-TOE!\n"
          "Choose who will you play for:\n"
          "   X - cross\n"
          "   O - zeros\n"
          "   Z - Computer vs. Computer")
    board = Board()

    game = Game(board)
    choice = ''
    while choice not in Player.signs and choice != 'Z':
        choice = input('Your choice: ').upper()
    user = Player(sign=choice if choice in Player.signs else None, area=board)
    pc = Player(area=board)

    # Show message who turns first
    print(f"{'You' if user.sign == 'X' else 'I'} make the first turn!")
    print(board)
    # Start the game
    while not game.is_over():
        # User's turn

        if not Player.log and user.sign == 'X' or Player.log and Player.log[-1][0] == pc.sign:
            turns = len(Player.log)
            while not len(Player.log) > turns:
                if choice == 'Z':
                    user.smart_decision()
                    print(f"{user.sign}'s turn: {Player.log[-1][1]}")
                else:
                    selected_cell = input('\nYour turn: ').upper()
                    # Check if input is correct
                    if selected_cell not in board.cells.keys():
                        print('Wrong value. Try again!')
                    elif not board.cells[selected_cell].marked:
                        user.turn(selected_cell)
                    else:
                        print('This cell is already filled. Try again.')
        else:
            pc.smart_decision()
            print(f"\n{'PC' if choice != 'Z' else pc.sign}'s turn: {Player.log[-1][1]} ")
        print(board)
    if not game.winning_sign:
        print('No available cells!')
    else:
        if choice == 'Z':
            print(f'{game.winning_sign} won!')
        else:
            print(f'You {"won" if user.sign == game.winning_sign else "lost"}!')
    print('Game over!')
