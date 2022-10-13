import random
from IPython.display import clear_output

#Global variables

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8,'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11, 'ace':1}
#NOTE Ace is 11 but ace is 1 in the values dictionary

still_playing = True

round_count = 0
dealer_score = 0
player_score = 0

round_count = 0
round_outcome = "N/A"

class Card:
    
    def __init__(self,suit,rank,value):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
    
    def __str__(self):
        return self.rank + " of " + self.suit

#create deck with all 52 cards
deck = []
for suit in suits:
    for rank in ranks:
        deck.append(Card(suit,rank,values[rank]))

#create interim new deck which will be shuffled and use to create shuffled_deck
n_deck = deck
random.shuffle(n_deck)

shuffled_deck = n_deck

#shuffled_deck to be used in the game

class Player:

    def __init__(self,name,balance,cards=[],aces=0):
        self.name = name
        self.cards = []
        self.balance = balance
        self.cards = cards
        self.aces = aces
        #print("{} has {} chips".format(name,balance))

    def ace_adjust(self):
        if self.aces > 0:
            #some logic to deal with ace adjustment
            pass

    def hit(self):
        global shuffled_deck
        if len(shuffled_deck) < 1:
            reset_deck()
            print("New deck of {} cards".format(len(shuffled_deck)))
        else:
            self.cards.append(shuffled_deck.pop())
        
          
    def __str__(self):
        return "The {}'s hand is {}".format(self.name,self.cards)
        
class Person(Player):
    
    def __init__(self,name,balance=10,cards=[],aces=0,bet=1):
        Player.__init__(self,name,balance,cards=[],aces=0)
        self.bet = bet
        print("{} has joined the game!".format(self.name))
    
    def make_bet(self):
        #accepts user input when making a bet
        '''bet_choice = "N/A"
        accepted_bet_answers = ["Y", "N"]
        new_bet = 0
        while bet_choice not in accepted_bet_answers:
            bet_choice = input("Do you want to bet more than 1 chip? Y or N")
            if bet_choice == "Y":
                while new_bet not in range[2,10]:
                    new_bet = int(input("Select a new bet between 2 and 10 chips: ")
                                              
            elif bet_choice == "N":
                pass
        '''
        #take bet from balance
        #at the moment, just a singe chip bet
        self.bet = 1
        self.balance -= self.bet
        
    
    def ace_adjust(self):
        if self.aces > 0:
            #some logic to dealwith ace adjustment
            pass
        
def reset_deck():
    #create deck with all 52 cards
    global deck
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append(Card(suit,rank,values[rank]))

    #create interim new deck which will be shuffled and use to create shuffled_deck
    n_deck = deck
    random.shuffle(n_deck)
    global shuffled_deck
    shuffled_deck = n_deck
    
    print("This is a new deck with {} cards".format(len(shuffled_deck)))
    
    #shuffled_deck to be used in the game

def replay():
    
    global game
    
    replay_q = "?"
    replay_answers = ["Y","N"]
       
    while replay_q not in replay_answers:
        
        replay_q = input("Do you want to start a fresh game? Y or N: ")
        
        if replay_q not in replay_answers:
            clear_output()
            print("Please select Y or N or this will go on forever...")
        
        elif replay_q == "Y":
            game = True
            still_playing = True
            return
        
        elif replay_q == "N":
            game = False
            return print("Okay, thanks for playing!")
        
        else:
            pass

def still_play():
    
    global still_playing
    
    s_p = "N/A"
    s_p_a = ["Y","N"]
    while s_p not in s_p_a:
        s_p = input("Do you want to continue? Y or N: ")
        if s_p not in s_p_a:
            clear_output()
            print("Please select Y or N...")
        elif s_p == "Y":
            still_playing = True
            continue
        elif s_p == "N":
            still_playing = False
            return print ("Okay, take your chips, if any, and run!")

#Game logic

game = True

while game:
    
    print("This is a new game")
    
    round_count = 0
    
    #reset - new deck, new players, new table
    reset_deck()
    
    #assign Players with human player as a Person
    dealer = Player("dealer",1000000)
    player = Person("player")
    
    #set up still_playing while loop
    still_playing = True
    
    while still_playing:
        
        clear_output()
        
        #keep count of the rounds played in this game
        round_count += 1
        print("It is round: {}".format(round_count))
                
        #check if player is out of chips
        if player.balance < 1:
            still_playing = False
            game = False
            print("You're out of chips, game over!")
            break
            #return
        else:
            pass
        
        #check if deck has enough cards to deal one hand to each player
        if len(shuffled_deck)<5:
            reset_deck()
        else:
            pass
        
        #discard any existing hands
        player.cards = []
        dealer.cards = []
        
        #reset player scores
        
        player_score = 0
        dealer_score = 0
        
        #player makes bet
        player.make_bet()
        print("{} has made a bet of {}. \n{}'s balance is {} chips".format(player.name,player.bet,player.name,player.balance))
        
        #deal
        for x in range(2):
            for y in (dealer,player):
                y.hit()

        #show one dealer card
        print("The dealer has a {}".format(dealer.cards[0]))
        
        #assign dealer score
        for d in dealer.cards:
            dealer_score += d.value

        #show player cards
        print("{} has:".format(player.name))
        for z in player.cards:
            player_score += z.value
            print(z)
        print("with value {}".format(player_score))
        
        '''ace adjustment here after the deal?'''
        
        #game-play
        
        #set up round_outcome while loop 
        global round_outcome
        round_outcome = "N/A"
        acceptable_outcomes = ["dealer_wins","player_wins"]
                
        while round_outcome not in acceptable_outcomes:
            
            #set up player_move while loop
            player_move = "N/A"
            acceptable_moves = ["hit","stick"]

            while player_move not in acceptable_moves:

                player_move = input("Do you want to hit or stick? : ")
                if player_move == "hit":
                    #execute request
                    player.hit()
                    print(player.cards[-1])
                    #update score
                    player_score += player.cards[-1].value
                    #display new score
                    print("Your score is now: {}".format(player_score))
                    #reset player_move in order to keep while loop going
                    player_move = "N/A"
                    pass
                
                elif player_move == "stick":
                    #execute request
                    print("Okay, you have {}. It's the dealer's move".format(player_score))
                    #break out of player_move while loop
                    break
                
                else:
                    print("Please type either hit or stick ")
                    continue
                
                #ace adjustment
                '''if player.cards[-1].rank == "Ace":
                    #ask if player wants it to be a 1 instead
                    pass
                '''
                               
                #player goes bust, break to end while loop
                if player_score > 21:
                    print("player goes bust!")
                    dealer.balance += player.bet
                    player.bet = 0
                    print("The dealer had {} and {}".format(dealer.cards[0],dealer.cards[1]))
                    #end of move
                    #end of round
                    round_outcome = "dealer_wins"
                    break
                    
                #player has hit and is not over 21 - needs to be given choice again
                elif player_score < 21:
                    continue    
                
                #else, player has 21 i.e. blackjack
                else:
                    print("Blackjack!")
                    print("Now it's the dealer's turn")
                    #break out of player_move while loop
                    break
                
                #end of player's next move while loop
            
            #continuation of the same round but after end of player's move
            
            if round_outcome in acceptable_outcomes:
                break
            
            else:
                pass
            
            #check player's score
            
            #player didn't hit enough to beat dealer's original hand
            if player_score <= dealer_score:
                #display outcome
                print("The dealer has a higher score of {}".format(dealer_score))
                print("with cards {} and {}".format(dealer.cards[0],dealer.cards[1]))
                #dealer wins player's bet
                dealer.balance += player.bet
                #player's bet reset
                player.bet = 0
                #end of the round
                round_outcome = "dealer_wins"
                #break out of round_outcome while loop
                break
            
            #player's score is above dealer's score so dealer needs to hit
            
            elif player_score > dealer_score:
                
                #show dealer hand
                print("The dealer has {} and {}".format(dealer.cards[0],dealer.cards[1]))
                
                #dealer must hit until wins or goes bust
                while dealer_score <= 21 and dealer_score < player_score:
                    #dealer hit
                    dealer.hit()
                    print("The dealer hits and gets {}".format(dealer.cards[-1]))
                    #update dealer score
                    dealer_score = dealer_score + dealer.cards[-1].value
                    print("The dealer's score is {}".format(dealer_score))
                    
                    #if the dealer score is now equal to or above the player's score, the while loop should end
                    #if the dealer has gone bust, the while loop should end
                #end of dealer hit while loop
                
                #end of elif player has higher score than dealer 
                pass
            
            #check outcomes
        
            #dealer has higher or equal score to player and is within 21 limit
            if dealer_score >= player_score and dealer_score <= 21:
                print("Dealer wins!")
                dealer.balance += player.bet
                #player's bet reset
                player.bet = 0
                #end of round
                round_outcome = "dealer_wins"
                #need to start new round so break out of this round while loop
                break

            #dealer goes bust
            elif dealer_score > 21:
                print("Dealer loses!")
                #dealer loses twice the player's bet
                dealer.balance = dealer.balance - 2*(player.bet)
                #player gains twice his/her bet
                player.balance = player.balance + 2*(player.bet)
                #player's bet reset
                player.bet = 0
                #end of round
                round_outcome = "player_wins"
                #need to start new round so break out of this round while loop
                break
            
            #redundant else pass
            else:
                pass
            
            #end of round_outcome while loop
            pass
             
        #ask if want to keep playing with existing deck and existing balance   
        still_play()
        #end of still_playing while loop
        
    #ask if want to start all over again
    replay()
    #end of game while loop
