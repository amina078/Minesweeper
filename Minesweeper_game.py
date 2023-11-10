import random


alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def show_board(board,board_size):
    #print all the col numbers
    print(" ", end = " ") #this is the first empty space between col numbers and row letters
    for col_num in range(1,board_size + 1): #+1 was added to include the last column also
        print(col_num, end = " ")
    print()

    #print row letters and rows
    row_letters = alphabets[0: board_size]
    for r in range(board_size):  #every row in the board
        print(row_letters[r], end = " ") #in the starting of every row, the row letters are printed
        for cell in board[r]: #every cell in each row
            print(cell, end = " ")
        print()

def fill_board(game_board,mines,board_size,row,col):
    if game_board[row][col] != "#": #if the cell does not contain #, then it is a mine
        return #game ends without showing the board
    if game_board[row][col] == "#":
        mine_count = count_adjacent_mines(game_board,mines,board_size,row,col)
        if mine_count > 0:#if there is a mine present adjacent to the cell, then put the mine count in the cell
            game_board[row][col] = str(mine_count)      
        else:
            game_board[row][col] = " " #if there is no mine adjacent to the cell, then the cell is empty
        if mine_count == 0:
            #row starts is the top adjacent row to the current cell. If the current cell is the top cell, then it is taking top adjacent as 0
            row_starts = max(row - 1, 0) 
            #row ends is the bottom adjacent row to the current cell. If the current cell is the the last cell, then it is taking the board size as the bottom adjacent       
            row_ends = min(row + 2, board_size)
            col_starts = max(col - 1, 0)
            col_ends = min(col + 2, board_size)
            for r in range (row_starts, row_ends): #adjecent row cells
                for c in range (col_starts, col_ends):
                    #recursion
                    fill_board(game_board,mines,board_size,r,c) #by using the fill board function, the adjecent cell is being filled with mine count

#I inserted all possible location from the board size and then python will randomly choose a location for mines
def generate_mines(board_size,num_mines):
    mines = []
    for i in range (board_size): #row
        for j in range (board_size): #column
            mines.append((i,j)) #the location where all particular cells are stored
    return random.sample(mines,num_mines)


def count_adjacent_mines(board,mines,board_size,row,col):
    count = 0
    row_starts = max(row - 1, 0)
    row_ends = min(row + 2, board_size)
    col_starts = max(col - 1, 0)
    col_ends = min(col + 2, board_size)

    for r in range (row_starts, row_ends):
        for c in range (col_starts, col_ends):
            if (r,c) in mines:
                count += 1
    return count

def play_game():
    board_size = int(input("Please insert the board size: "))
    while board_size <= 0:
        board_size = int(input("The board size cannot be 0 or a negative number. Enter a new number: "))
    num_mines = int(input("Please insert the number of mines: "))
    while num_mines <= 0:
        num_mines = int(input("The number of mines cannot be 0 or a negative number. Enter a new number: "))

    #initializing the board
    board = []
    for i in range(board_size): #row
        row = []
        for j in range(board_size): #column
            row.append("#")
        board.append(row)

    mines = generate_mines(board_size,num_mines) #getting all the locations where I put the mines 
    print(board_size,num_mines)
    show_board(board,board_size)

    #asking users to insert their guess
    while True: #ask for the move again and again
        move_input = input("Which cell you would like to reveal? (e.g A1): ")
        if len(move_input) < 2:
            print("The input was invalid. Please insert a valid move!")
            continue #go to the next iteration and ask for the move again

        if not move_input[0].isalpha():
            print("The first charecter should be a letter!")
       
        if not move_input[1].isdigit():
            print("The first charecter should be a number!")   
       
        row = alphabets.index(move_input[0].upper()) #the program finds move user's input row letter from the list of alphabet and converts it to the row index
        column = int(move_input[1: ]) - 1#-1 because the row index 1 is row 0 in the board isalpha is digit
        if column > board_size or column < 0 or row > board_size or row < 0: #checking if the move is outside of the board
            print("Move is outside of the range of the board. Please enter a valid move: ")
            continue

        #checking move input is amongst the mine locations
        if (row,column) in mines:
            board[row][column] = "X"
            show_board(board,board_size)
            print("Oh no, you lost!")
            break #game is over
        else:
            mine_count = count_adjacent_mines (board,mines,board_size,row,column)
            if mine_count == 0: 
                fill_board(board,mines,board_size,row,column) #if cell is 0, go to the adjecent cell and fill the adjecent cell
            else: #if more than 0, then I am putting the mine count in current cell
                board[row][column] = str(mine_count)
            show_board(board,board_size)

            #the winning: by deafult we are winning unless we find any # left in the board
            win = True
            for i in range(board_size):
                for j in range(board_size):
                    if board[i][j] == '#':
                        win = False
                        break

            if win:
                print("Congratulations! You have won!")


print("Welcome to Minesweeper")
know_game = input("Would you like to learn how to play the game? Yes or No? ")
if know_game.lower() == "yes":
    with open(r"c:\Users\home\Minesweeper\Readme.md") as readme:
        readme_contents = readme.read()
        print(readme_contents)

while True: #this is an infinite loop for asking users if they want to play again and again
    play_game()
    replay = input("Do you want to play again or leave the game? Yes or No? ")
    if replay.lower() == "no": #.lower was used to convert the input into all lower case
        break #the user leaves the game

