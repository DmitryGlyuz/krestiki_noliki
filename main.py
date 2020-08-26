import random

# Initializing field
field_dict = {}
abc = ['A', 'B', 'C']
numbers = [str(number) for number in range(1, 4)]
for letter in abc:
    for number in numbers:
        field_dict.update({letter + number: '-'})

# List with available cells
available_cells = list(field_dict.keys())

# Making scan list
scan_list = []
# Horizontal
for number in numbers:
    scan_list.append([letter + number for letter in abc])
# Vertical
for letter in abc:
    scan_list.append([letter + number for number in numbers])


# Diagonals
def add_diagonal(numbers_list):
    scan_list.append([letter + number for letter, number in zip(abc, numbers_list)])


add_diagonal(numbers)
add_diagonal(reversed(numbers))


# This function shows field
def show_field():
    print('\n  A B C')
    for number in numbers:
        field_line = number
        for show_field_letter in abc:
            field_line += ' ' + field_dict[show_field_letter + number]
        print(field_line)


# Update field
def update_field(cell_name, sign):
    # Open acceыs to write game-Over Boolean
    global game_over

    # This functions finds if there three signs in line
    def check_for_winner(line):
        for xo_sign in ['X', 'O']:
            if line.count(xo_sign) == 3:
                return xo_sign
        else:
            return False

    # Change the vale in cell
    field_dict[cell_name] = sign
    available_cells.remove(cell_name)

    # Show updated field
    show_field()

    # Scan lines
    # Go through scan_list
    for line in scan_list:
        # Get signs from current line
        line_content = [field_dict[key] for key in line]

        # Check if there are three signs
        win_sign = check_for_winner(line_content)

        # Stop scanning if someone wins
        if win_sign is not False:
            break

    # Show message if someone wins
    if win_sign is not False:
        final = 'You won!' if user_sign == win_sign else 'You lost!'
        print(final)
        game_over = True

    # Show message if there are no available cells
    elif not available_cells:
        print('No available cells.')
        game_over = True


# Computer's turn
def computer_turn():
    pc_turn = random.choice(available_cells)
    print(f'\nMy turn: {pc_turn}')
    update_field(pc_turn, pc_sign)


if __name__ == '__main__':
    # Greeting
    print("Hello! Let's play TIC-TAC-TOE!\n"
          "Choose who will you play for:\n"
          "   1 - cross (X)\n"
          "   2 - zeros (O)")

    # Select who turns first
    choice = None
    user_sign = ''
    while user_sign == '':
        choice = input('Your choice: ')
        if choice == '1':
            user_sign, pc_sign = 'X', 'O'
        elif choice == '2':
            user_sign, pc_sign = 'O', 'X'
        else:
            print('Wrong value. Try again.')

    show_field()

    # Show message who turns first
    # and start the game
    first_turn = ' make the first turn!'
    if pc_sign == 'X':
        print('I' + first_turn)
        user_turn = False
    else:
        print('You' + first_turn)
        user_turn = True
    game_over = False
    while game_over is False:
        # User's turn
        if user_turn is True:
            turn_done = False
            while turn_done is False:

                turn = input('\nYour turn: ').upper()
                # Check if input is correct
                if turn in available_cells:
                    update_field(turn, user_sign)
                    turn_done = True
                elif turn in field_dict.keys():
                    print('This cell is already filled. Try again.')
                else:
                    print('Wrong value. Try again!')
            user_turn = False
        # Computer's turn
        else:
            computer_turn()
            user_turn = True

    print('Game over!')
