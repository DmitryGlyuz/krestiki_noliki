# Initializing field
field_dict = {}
abc = ['A', 'B', 'C']
for i in abc:
    for n in range(1, 4):
        field_dict.update({i + str(n): '-'})


# This function shows field
def show_field():
    print('\n  A B C')
    for line in range(1, 4):
        field_line = str(line)
        for letter in abc:
            field_line += ' ' + field_dict[letter + str(line)]
        print(field_line)


def update_field(cell_name, sign):
    field_dict[cell_name.upper()] = sign


if __name__ == '__main__':
    print("Hello! Let's play TIC-TAC-TOE!\n"
          "Choose who will you play for:\n"
          "   1 - cross\n"
          "   2 - zeros")
    choice = None
    user_sign = ''
    while user_sign == '':
        choice = input('Your choice: ')
        if choice == '1':
            user_sign = 'X'
        elif choice == '2':
            user_sign = 'O'
        else:
            print('Wrong value! Try again.')

    game_over = False
    while game_over is False:
        show_field()
        turn = input('Your turn: ')
        update_field(turn, user_sign)
    print('Game over!')
