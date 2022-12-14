# import clear_output
from IPython.display import clear_output

#define global positional variables to be used for board display

global one, two, three, four, five, six, seven, eight, nine

seven = " "
eight = " "
nine = " "
four = " "
five = " "
six = " "
one = " "
two = " "
three = " "

#reset positional variables i.e. clear the board of moves made by the players
def reset():
    
    global one, two, three, four, five, six, seven, eight, nine
    
    seven = " "
    eight = " "
    nine = " "
    four = " "
    five = " "
    six = " "
    one = " "
    two = " "
    three = " "
    
    return

#function which creates the rows and columns of the three by three board
def board_process():
    # three user input rows:
    user_top = "| {" "} | {" "} | {" "} |".format(seven,eight,nine)
    user_mid = "| {" "} | {" "} | {" "} |".format(four,five,six)
    user_btm = "| {" "} | {" "} | {" "} |".format(one,two,three)
    # board concatenated string
    global board
    board = "+---+---+---+\n|   |   |   |\n" + user_top + "\n|   |   |   |\n+---+---+---+\n|   |   |   |\n" + user_mid + "\n|   |   |   |\n+---+---+---+\n|   |   |   |\n" + user_btm + "\n|   |   |   |\n+---+---+---+"
    return

#function to print the board
def displayboard(board):
    print("Here's the board:")
    print(board)

#function which allows first player to choose X or O to play the round with
def marker_input():
    
    global player1_marker
    player1_marker ="wrong"
    global player2_marker
    player2_marker = "wrong"    
    
    #accepted inputs
    marker_choice = ["X","O"]
    
    clear_output()
    
    while player1_marker not in marker_choice:
        
        player1_marker = input("Player1, select your marker, X or O: ")
        
        if player1_marker not in marker_choice:
            clear_output()
            print("Try again! You need to choose either X or O")
            
        elif player1_marker == "X":
            player2_marker = "O"
            
        elif player1_marker == "O":
            player2_marker = "X"
    
    return player1_marker, player2_marker

#game play for PLAYER ONE
def player_one_input():
    
    #set up variables
    player_one = "n/a"
    range_vals = range(1,10) #10 non-inclusive
    within_range = False
    global one, two, three, four, five, six, seven, eight, nine
    
    while player_one.isdigit() == False or within_range == False:
        
        player_one = input("Player 1, select your move: ")
        
        if player_one.isdigit() == False:
            clear_output()
            displayboard(board)
            print("Try again! Use the number pad to make a valid move.")
        
        elif player_one.isdigit() == True:
            if int(player_one) in range_vals:
                
                if int(player_one) == 1 and one == " ":
                    one = player1_marker
                    within_range = True
                elif int(player_one) == 1 and one != " ":
                    within_range = False
                    clear_output()
                    displayboard(board)
                    print("Try again! You can't go there")
                
                if int(player_one) == 2 and two == " ":
                    two = player1_marker
                    within_range = True
                elif int(player_one) == 2 and two != " ":
                    within_range = False
                    clear_output()
                    displayboard(board)
                    print("Try again! You can't go there")
                
                if int(player_one) == 3 and three == " ":
                    three = player1_marker
                    within_range = True
                elif int(player_one) == 3 and three != " ":
                    within_range = False
                    clear_output()
                    displayboard(board)
                    print("Try again! You can't go there")
            
                if int(player_one) == 4 and four == " ":
                    four = player1_marker
                    within_range = True
                elif int(player_one) == 4 and four != " ":
                    within_range = False
                    clear_output()
                    displayboard(board)
                    print("Try again! You can't go there")
                
                if int(player_one) == 5 and five == " ":
                    five = player1_marker
                    within_range = True
                elif int(player_one) == 5 and five != " ":
                    within_range = False
                    clear_output()
                    displayboard(board)
                    print("Try again! You can't go there")
                
                if int(player_one) == 6 and six == " ":
                    six = player1_marker
                    within_range = True
                elif int(player_one) == 6 and six != " ":
                    within_range = False
                    clear_output()
                    displayboard(board)
                    print("Try again! You can't go there")                
                
                if int(player_one) == 7 and seven == " ":
                    seven = player1_marker
                    within_range = True
                elif int(player_one) == 7 and seven != " ":
                    within_range = False
                    clear_output()
                    displayboard(board)
                    print("Try again! You can't go there") 
                
                if int(player_one) == 8 and eight == " ":
                    eight = player1_marker
                    within_range = True
                elif int(player_one) == 8 and eight != " ":
                    within_range = False
                    clear_output()
                    displayboard(board)
                    print("Try again! You can't go there")
                
                if int(player_one) == 9 and nine == " ":
                    nine = player1_marker
                    within_range = True
                elif int(player_one) == 9 and nine != " ":
                    within_range = False
                    clear_output()
                    displayboard(board)
                    print("Try again! You can't go there")
          
                else:
                    pass
                
            
            else:
                within_range = False
                clear_output()
                displayboard(board)
                print("Try again! Select a number from 1 to 9")
                
        else:
            pass
     
    return int(player_one)

#game play for PLAYER TWO
def player_two_input():
    
    #set up variables
    player_two = "n/a"
    range_vals = range(1,10) #10 non-inclusive
    within_range = False
    global one, two, three, four, five, six, seven, eight, nine
    
    while player_two.isdigit() == False or within_range == False:
        
        player_two = input("Player 2, select your move: ")
        
        if player_two.isdigit() == False:
            clear_output()
            displayboard(board)
            print("Try again! Use the number pad to make a valid move.")
        
        elif player_two.isdigit() == True:
            if int(player_two) in range_vals:
                
                if int(player_two) == 1 and one == " ":
                    one = player2_marker
                    within_range = True
                elif int(player_two) == 1 and one != " ":
                    within_range = False
                    clear_output()
                    displayboard(board)
                    print("Try again! You can't go there")
                
                if int(player_two) == 2 and two == " ":
                    two = player2_marker
                    within_range = True
                elif int(player_two) == 2 and two != " ":
                    within_range = False
                    clear_output()
                    displayboard(board)
                    print("Try again! You can't go there")
                
                if int(player_two) == 3 and three == " ":
                    three = player2_marker
                    within_range = True
                elif int(player_two) == 3 and three != " ":
                    within_range = False
                    clear_output()
                    displayboard(board)
                    print("Try again! You can't go there")
            
                if int(player_two) == 4 and four == " ":
                    four = player2_marker
                    within_range = True
                elif int(player_two) == 4 and four != " ":
                    within_range = False
                    clear_output()
                    displayboard(board)
                    print("Try again! You can't go there")
                
                if int(player_two) == 5 and five == " ":
                    five = player2_marker
                    within_range = True
                elif int(player_two) == 5 and five != " ":
                    within_range = False
                    clear_output()
                    displayboard(board)
                    print("Try again! You can't go there")
                
                if int(player_two) == 6 and six == " ":
                    six = player2_marker
                    within_range = True
                elif int(player_two) == 6 and six != " ":
                    within_range = False
                    clear_output()
                    displayboard(board)
                    print("Try again! You can't go there")                
                
                if int(player_two) == 7 and seven == " ":
                    seven = player2_marker
                    within_range = True
                elif int(player_two) == 7 and seven != " ":
                    within_range = False
                    clear_output()
                    displayboard(board)
                    print("Try again! You can't go there") 
                
                if int(player_two) == 8 and eight == " ":
                    eight = player2_marker
                    within_range = True
                elif int(player_two) == 8 and eight != " ":
                    within_range = False
                    clear_output()
                    displayboard(board)
                    print("Try again! You can't go there")
                
                if int(player_two) == 9 and nine == " ":
                    nine = player2_marker
                    within_range = True
                elif int(player_two) == 9 and nine != " ":
                    within_range = False
                    clear_output()
                    displayboard(board)
                    print("Try again! You can't go there")
                
                else:
                    pass
            
            else:
                within_range = False
                clear_output()
                displayboard(board)
                print("Try again! Select a number from 1 to 9")  
            
        else:
            pass
        
    return int(player_two)

#function which checks if a player has won (includes check for a draw)
def win_check():
    
    global one, two, three, four, five, six, seven, eight, nine, player1_marker, player2_marker, game_on
    
    #eight patterns of win
    #two potential winners
    #hence 16 variations
    
    winner = "No winner yet"
    winner_range = ["Player 1 is the winner!","Player 2 is the winner!","It's a draw!"]
    
    while winner not in winner_range:
            
        #Player one win check
        if seven == eight == nine == player1_marker:
            winner = winner_range[0]
                        
        elif seven == five == three == player1_marker:
            winner = winner_range[0]

        elif seven == four == one == player1_marker:
            winner = winner_range[0]

        elif eight == five == two == player1_marker:
            winner = winner_range[0]
            
        elif nine == six == three == player1_marker:
            winner = winner_range[0]
            
        elif one == five == nine == player1_marker:
            winner = winner_range[0]

        elif four == five == six == player1_marker:
            winner = winner_range[0]

        elif one == two == three == player1_marker:
            winner = winner_range[0]


        #Player two win check
        elif seven == eight == nine == player2_marker:
            winner = winner_range[1]

        elif seven == five == three == player2_marker:
            winner = winner_range[1]

        elif seven == four == one == player2_marker:
            winner = winner_range[1]

        elif eight == five == two == player2_marker:
            winner = winner_range[1]

        elif nine == six == three == player2_marker:
            winner = winner_range[1]

        elif one == five == nine == player2_marker:
            winner = winner_range[1]

        elif four == five == six == player2_marker:
            winner = winner_range[1]

        elif one == two == three == player2_marker:
            winner = winner_range[1]
        
        
        #draw check
        elif one != " " and two != " " and three != " " and four != " " and five != " " and six != " " and seven != " " and eight != " " and nine != " ":
            winner = winner_range[2]
        
        else:
            break

    if winner in winner_range:
        clear_output()
        board_process()
        displayboard(board)
        
        game_on = False
        
        return print(winner)
    
    else:
        pass

#function which asks if players wish to play the game again
def replay():
    
    global game, game_on
    
    replay_q = "?"
    replay_answers = ["Y","N"]
       
    while replay_q not in replay_answers:
        
        replay_q = input("Do you want to play again? Y or N: ")
        
        if replay_q not in replay_answers:
            clear_output()
            print("Please select Y or N or this will go on forever...")
        
        elif replay_q == "Y":
            game = True
            game_on = True
            return
        
        elif replay_q == "N":
            game = False
            return print("Okay, thanks for playing!")
        
        else:
            pass

game = True

#GAME PLAY
while game:

    game_on = True
    
    reset()
    
    #clear_output()
    
    marker_input()
    
    while game_on:

        clear_output()

        board_process()

        displayboard(board)

        player_one_input()

        win_check()
        if game_on == False:
            break

        clear_output()

        board_process()

        displayboard(board)

        player_two_input()

        win_check()
        if game_on == False:
            break

    replay()

