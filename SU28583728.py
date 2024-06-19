import stdarray
import stdio
import sys

# Need to make sure that s is in the outer 3 row & col according to game rules
def check_sink_range(row_max, col_max): 
    while not stdio.isEmpty():
        data_input = stdio.readLine()
        input_data = data_input.strip().split()
        command = input_data[0]
        if command == 's':
            length = int(input_data[1])
            row = int(input_data[2])
            col = int(input_data[3])
        
        # Checking if the sink coordinates are out of bounds 
            if not (0 <= row < row_max and 0 <= col < col_max):
                stdio.writeln("ERROR: Sink in the wrong position\n")
                return sys.exit()
        
        # Checking if the sink starts or ends outside the allowed bounds
            if not ((0 <= row < 3 or row_max - 3 <= row < row_max) and (0 <= col < 3 or col_max - 3 <= col < col_max)):
                stdio.writeln("ERROR: Sink in the wrong position\n")
                return sys.exit()
        
        # Checking if a part of the sink goes beyond the bounds
            if ((row + length > row_max) or (col + length > col_max)):
                stdio.writeln("ERROR: Sink in the wrong position\n")
                return sys.exit()

        # If all checks pass
            return True
        else:
        # If it's not a sink placement command, ignore
            return True

# Need to make sure that piece is in correct range
def check_piece_range(row_max, col_max):
    while not stdio.isEmpty():
        data_input = stdio.readLine()
        input_data = data_input.strip().split()
        command = input_data[0]
        # Only checking for piece commands
        if command in ["l", "d"]:  
            row = int(input_data[2])
            col = int(input_data[3])

        # Checking if the piece's position is out of bounds
            if not (0 <= row < row_max and 0 <= col < col_max):
                stdio.writeln("ERROR: Piece in the wrong position\n")
                return False

        # Checking if the piece is within the outer three rows or columns
            if (0 <= row < 3 or row_max - 3 <= row < row_max) or (0 <= col < 3 or col_max - 3 <= col < col_max):
                stdio.writeln("ERROR: Piece in the wrong position\n")
                return False

        # If all checks pass
            return True
        else:
            return True 

def check_piece_upright(row, col, board, input_data):
    command = input_data[0]
    if command in ["l", "d"]:
        row = input_data[2]
        col = input_data[3]
        column_max = len(board)

        #integer value that represents a d/D piece that is a 2 by 2 piece basically spans 4 cells
        integer_value = (row*column_max) + col        
        intstr = str(integer_value)
    
        if (row > 0 and board[row-1][col] != intstr) and (col < column_max - 1 and board[row][col+1] != intstr) and (col > 0 and board[row][col-1] != intstr) and (row == column_max - 1 or (row < column_max - 1 and board[row+1][col] != intstr)):
            return True
        else:
            return False
    else:
        return False
  
def get_piece_fields(row, col, board, input_data):

    command = input_data[0]
    if command in ["l", "d"]:
        if input_data[2] >= len(board) or input_data[3] >= len(board[0]) or input_data[2] < 0 or input_data[3] < 0:
            stdio.writeln("Error: coordinates are out of bounds.")
            return []

        piece = board[row][col]
        field = []
        for k in range(len(board)):
            for j in range(len(board[k])):
                if board[k][j] == piece:
                    field.append((k, j))
    
        for coordinates in field:
            stdio.writeln("Field: {}".format(coordinates))
    
        return field

# Now creating the game board   
def initialize_board(row_max, col_max):
    return stdarray.create2D(row_max, col_max, " ")   

def read_board(board):
    # The number of columns
    col_max = len(board[0])  
    # Displaying column headers
    header = "  " 
    for i in range(col_max):
        # Right-align column numbers
        header += " {:>2}".format(i)  
    stdio.writeln(header)

    # Printing the top border of the board
    stdio.writeln("   +" + "--+" * col_max)

    # Looping through each row to print its contents
    for row in range(len(board) - 1, -1, -1):
        # Printing the row number on the left
        row_string = "{:>2} |".format(row)
        for col in range(col_max):
            element = board[row][col]
            # Each element should take up two characters and be right-aligned
            # Maintain space if empty
            formatted_element = "{:>2}".format(element) if element != ' ' else "  "  
            row_string += formatted_element + "|"
        stdio.writeln(row_string)
        # The row separator
        stdio.writeln("   +" + "--+" * col_max)  
    

def place_items(board, input_data, item_type):
    command = input_data[0]
    if command == 's':
        length = int(input_data[1])
        if length != 1 and length !=2:
            stdio.writeln(f"ERROR: Invalid piece type {length}\n")
            return sys.exit()
        
        row = int(input_data[2])
        col = int(input_data[3])
        if row + length > len(board) or col + length > len(board[0]):
            stdio.writeln("ERROR: Sink cannot be next to another sink\n")
            return sys.exit()

        for i in range(max(0, row-1), min(len(board), row + length + 1)):
            for j in range(max(0, col-1), min(len(board[0]), col + length + 1)):
                # Checking if there is a sink in the adjacent cells
                if board[i][j] == 's':  
                    stdio.writeln("ERROR: Sink cannot be next to another sink\n")
                    return sys.exit()

        for i in range(length):
            for j in range(length):
                if not ((row < 3 or row >= len(board) - 3) or (col < 3 or col >= len(board[0]) - 3)):
                    stdio.writeln("ERROR: Sink in the wrong position\n")
                    return sys.exit()
                if 0 <= row + i < len(board) and 0 <= col + j < len(board[0]):
                    board[row + i][col + j] = item_type

        # If all the checks pass, place the sink on the board
        for i in range(length):
            for j in range(length):
                board[row + i][col + j] = 's'

    elif command == 'x':
        length = 1
        row = int(input_data[1])
        col = int(input_data[2])
        for i in range(length):
            for j in range(length):
                if 0 <= row + i < len(board) and 0 <= col + j < len(board[0]):
                    board[row + i][col + j] =  item_type

# Setting up the pieces on the board before the game starts
def process_setup(board, input_data): 
    command = input_data[0]
    if command not in ['s', 'x', 'd', 'l']:
        stdio.writeln(f"ERROR: Invalid object type {command}\n")
        return sys.exit()

    if command == 'd' or command == 'l':
        piece_type = input_data[1].lower()
        row = int(input_data[2])
        col = int(input_data[3])

    # Validating the position before placing anything on the board
        if not (0 <= row < len(board) and 0 <= col < len(board[0])):
            stdio.writeln(f"ERROR: Field {row} {col} not on board\n")
            return sys.exit()
    
    if command in ['l', 'd']:
        if piece_type not in ['a', 'b', 'c', 'd']:
            stdio.writeln(f"ERROR: Invalid piece type {piece_type}\n")
            return sys.exit()
        if not ((3 <= row < row_max - 3) and (3 <= col < col_max - 3)):
            stdio.writeln("ERROR: Piece in the wrong position\n")
            return sys.exit()

    if command == 's' or command == 'x':
        place_items(board, input_data, command)
    else:
        label = input_data[1].upper() if command == 'd' else input_data[1].lower()
        length = 2 if piece_type == 'd' else 1
        if not check_bounds(board, row, col, length):
            stdio.writeln(f"ERROR: Field {row} {col} not on board\n")
            return
        if board[row][col] != ' ':
            stdio.writeln(f"ERROR: Field {row} {col} not free\n")
            return sys.exit()
        place_piece(board, length, row, col, label, command == 'd')

def check_bounds(board, row, col, length):
    # Once again checking that each part of the piece is within the board
    return all(0 <= row + i < len(board) and 0 <= col + j < len(board[0]) 
               for i in range(length) for j in range(length))     

def place_piece(board, length, row, col, label, is_dark):
    # Calculating identifier for a 'd' 2 by 2 type piece
    base_id = row * len(board[0]) + col  
    if board[row][col] == ' ':
        # Place the bottom left-most piece
        board[row][col] = label.upper() if is_dark else label.lower()  
        for i in range(length):
            for j in range(length):
                if i == 0 and j == 0:
                    continue  # Skip the origin since it's already placed
                new_row = row + i
                new_col = col + j
                if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]):
                    board[new_row][new_col] = str(base_id)
    else:
        stdio.writeln(f"ERROR: Field {row} {col} not free\n")

def is_valid_piece(player, piece):
    if player == "light" and piece.islower() and piece in 'abcd':
        return True
    elif player == "dark" and piece.isupper() and piece in 'ABCD':
        return True
    return False

def move_piece(board, row, col, direction, player, scores, original_positions, moved_pieces):
    dir_map = {'u': (1, 0), 'd': (-1, 0), 'l': (0, -1), 'r': (0, 1)}
    if direction not in dir_map:
        # Informing the gamer about the invalid direction
        stdio.writeln(f"ERROR: Invalid direction {direction}\n")  
        return False

    dr, dc = dir_map[direction]
    new_row, new_col = row + dr, col + dc

    if not (0 <= new_row < len(board) and 0 <= new_col < len(board[0])):
        stdio.writeln(f"ERROR: Cannot move beyond the board\n")
        return False
    
    # A blocked field 'x', no piece may be moved onto a blocked field
    if board[new_row][new_col] == 'x': 
        stdio.writeln(f"ERROR: Field {new_row}, {new_col} is blocked\n")
        return False
    
    # Checking if a 'd' piece is being moved for the second time in a turn
    if board[row][col].lower() == 'd' and board[row][col] in moved_pieces:
        stdio.writeln("ERROR: Cannot move a 2x2x2 piece on the second move\n")
        return False

    # Checking if a piece is moving back to it's original postion on 2nd move   
    if (new_row, new_col) == original_positions[board[row][col]]:
        stdio.writeln("ERROR: Piece cannot be returned to starting position\n")
        return False
    
    if board[new_row][new_col] == ' ':
        board[new_row][new_col] = board[row][col]
        board[row][col] = ' '

        # Mark the piece as moved after a successful first move
        moved_pieces[board[row][col]] = True
        return True  

    if board[new_row][new_col] == 's':
        piece_value = 2 if board[row][col].lower() == 'd' and board[row][col].upper() == 'D' else 1
        scores[player] += piece_value
        # The piece sinks
        board[row][col] = ' '  
        return True
    
    else:
        stdio.writeln(f"ERROR: Cannot move a 2x2x2 piece on the second move\n")
        sys.exit()

# Reading input from a text file or from the gamer in the terminal
def read_input(board):
    setup_phase = True
    moves = []
    # In this code, stdio.writeln will only be enabled when using the terminal
    #stdio.writeln("Enter setup commands, type '#' to end setup, and 'end' to finish input:") 

    while True:
        try:
            data_input = stdio.readLine().strip()
        except EOFError:
            #stdio.writeln("No more input available. Ending input processing.")
            break

        if data_input.lower() == 'end':
            #stdio.writeln("Ending input and processing moves.")
            # Exiting the loop when the gamer enters 'end'
            break  

        if data_input == '#':
            setup_phase = False
            #stdio.writeln("Setup complete. Enter game moves:")
            continue

        input_data = data_input.split()
        if setup_phase:
            process_setup(board, input_data)
        else:
            # Storing the moves to use in other methods
            moves.append(input_data)  
    
    read_board(board)
    return moves

# This method allows the game to be played in a session through executing the different commands
def game_loop(board, moves):
    scores = {'light': 0, 'dark': 0}
    is_light_turn = True
    move_index = 0

    # When there are no moves are provided
    if not moves:  
        # Optionally, check here if any moves are possible at all and decide the game outcome
        if not any_possible_moves(board, 'light') or not any_possible_moves(board, 'dark'):
            stdio.writeln("Light loses" if not any_possible_moves(board, 'light') else sys.exit())
            return

    while move_index < len(moves):
        player = 'light' if is_light_turn else 'dark'
        move = moves[move_index]
        move_count = 0
        # Array to keep track of original positions during a turn
        original_positions = {}  
        moved_pieces ={}
        no_legal_moves =True

        # Each player should make two moves per turn
        while move_count < 2 and move_index < len(moves):  
            move = moves[move_index]
            row, col, direction = int(move[0]), int(move[1]), move[2]

            if row >= len(board) or col >= len(board[0]) or row < 0 or col < 0:
                stdio.writeln(f"ERROR: Field {row} {col} not on board\n")
                move_index += 1
                continue

            piece = board[row][col]

            if piece == ' ':
                stdio.writeln(f"ERROR: No piece on field {row} {col}\n")
                move_index += 1
                continue

            # Storing the original position of the piece at the start of their turn
            if piece not in original_positions:
                original_positions[piece] = (row, col)

            if not is_valid_piece(player, board[row][col]):   
                stdio.writeln(f"ERROR: Piece does not belong to the correct player\n")
                move_index += 1
                continue

            # Now moving the piece
            if move_piece(board, row, col, direction, player, scores, original_positions, moved_pieces):
                no_legal_moves = False
                read_board(board)
            else:
                move_index += 1
                continue

            if no_legal_moves:
                stdio.writeln(f"{player.capitalize()} loses")

            move_index += 1
            move_count += 1
    
        # Swicthing players after each turn, note that the Light player always starts first 
        is_light_turn = not is_light_turn  
        
        # Checking the win condition after each player's turn
        if scores['light'] >= 4:
            stdio.writeln("Light wins!")
            break
        if scores['dark'] >= 4:
            stdio.writeln("Dark wins!")
            break

# Method that provides all possible moves for the game_loop
def any_possible_moves(board, player):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if is_valid_piece(player, board[row][col]):
                # Assuming that the validate_move method checks if a move is allowed from this position
                if validate_move(row, col, 'u', board, (row, col)) or \
                   validate_move(row, col, 'd', board, (row, col)) or \
                   validate_move(row, col, 'l', board, (row, col)) or \
                   validate_move(row, col, 'r', board, (row, col)):
                    return True
    return False

# validating moves provided by the player
def validate_move(row, col, direction, board, original_position):
    """Validate the move is within board and the direction is correct, and not returning to start."""
    directions = {'u': (1, 0), 'd': (-1, 0), 'l': (0, -1), 'r': (0, 1)}
    if direction not in directions:
        return False
    dr, dc = directions[direction]
    new_row, new_col = row + dr, col + dc
    if (new_row, new_col) == original_position:
        # Prevent the gamer from returning a piece to its original position
        return False  
    return 0 <= new_row < len(board) and 0 <= new_col < len(board[0]) and board[new_row][new_col] == ' '
        
if __name__ == "__main__":
    if len(sys.argv) < 4:
        stdio.writeln("ERROR: Too few arguments")
        sys.exit(1)
    elif len(sys.argv) > 4:
        stdio.writeln("ERROR: Too many arguments")
        sys.exit(1)

    # Check if each argument is an integer
    if not all(arg.isdigit() for arg in sys.argv[1:4]):
        stdio.writeln("ERROR: Illegal argument")
        sys.exit(1)
    
    row_max = int(sys.argv[1])
    col_max = int(sys.argv[2])
    gui_mode = int(sys.argv[3]) 
    
    if gui_mode == 1:
        # If gui_mode is 1, exit the program (not making use of GUI)
        sys.exit(0)
    
    board = initialize_board(row_max, col_max)

    # For the game to be played in terminal
    if gui_mode == 0:
        #stdio.writeln("Game mode is terminal-based.")
        moves = read_input(board)
        game_loop(board, moves)