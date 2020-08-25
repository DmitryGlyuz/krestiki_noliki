import random

# Initializing field
field_dict = {}
abc = ['A', 'B', 'C']
for i in abc:
    for n in range(1, 4):
        field_dict.update({i + str(n): '-'})

# List with available cells
available_cells = list(field_dict.keys())
print(available_cells)


# This function shows field
def show_field():
    print('\n  A B C')
    for line in range(1, 4):
        field_line = str(line)
        for letter in abc:
            field_line += ' ' + field_dict[letter + str(line)]
        print(field_line)


def update_field(cell_name, sign):
    global game_over
    def check_for_winner(line_list):
        for sign in ['X', 'O']:
            if line_list.count(sign) == 3:
                return sign
        else:
            return False
    field_dict[cell_name] = sign
    available_cells.remove(cell_name)

    # Scan lines
    for letter in abc:
        scanning_line = []
        for i in range(1, 4):
            scanning_line.append(field_dict[letter + str(i)])
        win_sign = check_for_winner(scanning_line)
        if win_sign is not False:
            break
    show_field()
    if win_sign is not False:
        final = 'You won!' if user_sign == win_sign else 'You lost!'
        print(final)
        game_over = True
    if not available_cells:
        print('No available cells.')
        game_over = True


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
    first_turn = ' make the first turn!'
    if pc_sign == 'X':
        print('I' + first_turn)
        user_turn = False
    else:
        print('You' + first_turn)
        user_turn = True
    game_over = False
    while game_over is False:
        if user_turn is True:
            turn_done = False
            while turn_done is False:
                turn = input('\nYour turn: ').upper()
                if turn in available_cells:
                    update_field(turn, user_sign)
                    turn_done = True
                elif turn in field_dict.keys():
                    print('This cell is already filled. Try again.')
                else:
                    print('Wrong value. Try again!')
            user_turn = False
        else:
            computer_turn()
            user_turn = True

    print('Game over!')
