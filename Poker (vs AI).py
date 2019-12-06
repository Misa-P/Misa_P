import random
'''
Hands incorporated (no joker deck) in the game:
1. Royal flush (done) - score of 23
2. Straight flush (done) - score of 22
3. Four of a kind (done) - score of 21
4. Full house (done) - score of 20
5. Flush (flower) (done) - score of 19
6. Straight (combo) (done) - score of 18
7. Three of a kind (done) - score of 17
8. Two pairs (done) - score of 16
9. Pair (done) - score of 15
10. High card (done) - score equal to value of card (max 14)
============================================================================================================
Basic game complete, minimum possible product; not yet viable. Current issues + improvements needed:
1. AI only calls, never raises or folds. 
    a. Implement basic folding logic
    b. Implement basic raising logic
2. Include graphics
3. Freeze as executable possibly
4. Have a GUI rather than in Python terminal
5. Confirmations before moving between dealing and betting phases each round.
6. Confirmation of pot size before each betting phase
7. General error checking functions
8. Simplifying main body code
9. Inclusion of jokers?
10. Be clearer on game ending conditions and results: i.e. victory/loss?
11: Multiple AI players?
12. Inclusion of other human players?
'''

class card():
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

class player():
    def __init__(self, chips):
        self.hand = []
        self.chips = chips
        self.hand_score = 0

def callFoldOrRaise(player):
    decision = input("Call, fold, or raise?\n")
    if decision == 'call':
        return 'call'
    elif decision == 'fold':
        return 'fold'
    elif decision == 'raise':
        print('You currently possess ' + str(player.chips) + ' chips.\n')
        try:
            raise_amt = int(input('Enter amount to raise: '))
        except ValueError:
            print('Please enter an integer')
        if raise_amt > player.chips:
            print('Not enough chips')
        return raise_amt

def cardDeal(deck, player, number_dealt = 1):   # deals one card if not otherwise specified
    global cards_dealt
    for i in range(cards_dealt, cards_dealt + number_dealt):
        player.hand.append(deck[i])
        deck.pop(i)

    cards_dealt = cards_dealt + number_dealt

def cardValueDisplay(card_num):     # display royals as letters, not number values
    if card_num <= 10:
        return str(card_num)
    if card_num == 11:
        return 'J'
    if card_num == 12:
        return "Q"
    if card_num == 13:
        return 'K'
    if card_num == 14:
        return "A"

def chipCollection(player, amount):     # taking chips from each player to fill pot during each round
    global pot_value
    if amount <= player.chips:
        pot_value = pot_value + amount
        player.chips = player.chips - amount
    else:
        pot_value = pot_value + player.chips
        player.chips = 0

def deckCreation():     # creates an ordered deck
    deck = {}
    counter = 0
    for suit in range(0, 4):
        for card_value in range(2, 15):
            deck[counter] = card(suit, card_value)
            counter += 1
    return deck

def draw(player1, player2):
    global pot_value
    player1.chips += pot_value / 2
    player2.chips += pot_value / 2
    pot_value = 0

def handCalc(player):           # evaluating each hand for comparison
    if player.hand_score <= 14:
        return ('High card')
    elif player.hand_score == 23:
        return ('Royal flush')
    elif player.hand_score == 22:
        return ('Straight flush')
    elif player.hand_score == 21:
        return ('Four of a kind')
    elif player.hand_score == 20:
        return ('Full house')
    elif player.hand_score == 19:
        return ('Flush')
    elif player.hand_score == 18:
        return ('Straight')
    elif player.hand_score == 17:
        return ('Three of a kind')
    elif player.hand_score == 16:
        return ('Two pairs')
    elif player.hand_score == 15:
        return ('One pair')

def handValue(player, river):       # primary hand value logic. See header comments for score values
    all_cards = []
    straight = False
    triple = False

    for i in range(0, len(player.hand)):
        all_cards.append((player.hand[i].value, player.hand[i].suit))
    for i in range(len(player.hand), len(player.hand) + len(river.hand)):
        all_cards.append((river.hand[i - len(player.hand)].value, river.hand[i - len(player.hand)].suit))

    all_cards = sorted(all_cards, reverse = True)

    if all_cards[0][0] == all_cards[1][0] - 1 and all_cards[1][0] == all_cards[2][0] - 1 and \
            all_cards[2][0] == all_cards[3][0] - 1 and all_cards[3][0] == all_cards[4][0] - 1:
        straight = True
        if all_cards[0][1] == all_cards[1][1] and all_cards[1][1] == all_cards[2][1] and all_cards[2][
            1] == all_cards[3][1] and all_cards[3][1] == all_cards[4][1]:
            if all_cards[0][0] == 14:
                return 23
            else:
                return 22

    for i in range(0, len(all_cards) - 2):
        if all_cards[i][0] == all_cards[i+1][0] and all_cards[i+1][0] == all_cards[i+2][0]:
            triple = True
            if all_cards[i + 2][0] == all_cards[i + 3][0]:
                return 21
            elif i == 0 and all_cards[3][0] == all_cards[4][0]:
                return 20
            elif i == 2 and all_cards[0][0] == all_cards[1][0]:
                return 20

    if all_cards[0][1] == all_cards[1][1] and all_cards[1][1] == all_cards[2][1] and all_cards[2][1] == all_cards[3][1] and all_cards[3][1] == all_cards[4][1]:
        return 19

    if straight:
        return 18

    if triple:
        return 17

    for i in range(0, len(all_cards) - 1):
        if all_cards[i][0] == all_cards[i+1][0]:
            if i == 0:
                if all_cards[i+2][0] == all_cards[i+3][0] or all_cards[i+3][0] == all_cards[i+4][0]:
                    return 16
                else:
                    return 15
            elif i == 1:
                if all_cards[i+2][0] == all_cards[i+3][0]:
                    return 16
                else:
                    return 15
            else:
                return 15

    return all_cards[0][0]      # returns high card value; high card if no other condition satisfied, max 14

def playerWin(winner, loser):
    global pot_value, game_flag
    winner.chips += pot_value
    pot_value = 0
    if loser.chips <= 0:
        game_flag = False

def showDown(player1, player2, river):
    global game_flag, ante

    print('Your hand: ', end = ' ')
    for i in range(0,len(player1.hand)):
        print(str(cardValueDisplay(player1.hand[i].value)) + ' of ' + suitDisplay(player1.hand[i].suit), end = ', ')

    print('Your opponent\'s hand: ', end = ' ')
    for i in range(0, len(player2.hand)):
        print(str(cardValueDisplay(player2.hand[i].value)) + ' of ' + suitDisplay(player2.hand[i].suit), end = ', ')

    print('River: ', end = ' ')
    for i in range(0, len(river.hand)):
        print(str(cardValueDisplay(river.hand[i].value)) + ' of ' + suitDisplay(river.hand[i].suit), end = ', ')
    print()

    print("You hand is: " + handCalc(player1))
    print("Your opponent\'s hand is: " + handCalc(player2))

    if player1.hand_score > player2.hand_score:
        playerWin(player1, player2)
    if player2.hand_score > player1.hand_score:
        playerWin(player2, player1)
    if player1.hand_score == player2.hand_score:
        draw(player1, player2)

def shuffleDeck(sorted_deck):       # shuffles the input deck
    dummy = []
    shuffled_deck = {}

    for i in range(0, len(sorted_deck)):
        dummy.append(i)
    random.shuffle(dummy)
    for j in range(0,len(sorted_deck)):
        shuffled_deck[j] = sorted_deck[dummy[j]]

    return shuffled_deck

def suitDisplay(suit_num):      # process suits for display instead of leaving as numerical values
    if suit_num == 0:
        return 'Spades'
    if suit_num == 1:
        return 'Hearts'
    if suit_num == 2:
        return 'Clubs'
    if suit_num == 3:
        return 'Diamonds'

def main():
    global cards_dealt, pot_value, game_flag, ante
    game_flag = True
    user = player(500)
    opponent = player(500)
    river = player(0)


    try:
        ante = int(input('Base ante value: '))
        if ante > 500:
            print('Please enter only integer values less than 500')
            return
    except ValueError:
        print('Please enter only integer values less than 500')
        return

    while game_flag:
        round_flag = True
        user.hand = []
        opponent.hand = []
        river.hand = []
        cards_dealt = 0
        pot_value = 0
        deck = shuffleDeck(deckCreation())

        chipCollection(user, ante)
        chipCollection(opponent, ante)

        cardDeal(deck, user, 2)
        cardDeal(deck, opponent, 2)

        print("Chips left: " + str(user.chips) + ', Opponent\'s chips: ' + str(opponent.chips))
        for i in range(0, len(user.hand)):
            print('Card ' + str(i+1) + ': ' + str(cardValueDisplay(user.hand[i].value)) + ' of ' + suitDisplay(user.hand[i].suit))

        user_decision = callFoldOrRaise(user)
        if isinstance(user_decision, str):
            if user_decision == 'fold':
                playerWin(opponent, user)
                round_flag = False
            elif user_decision == 'call':
                pass
        else:
            chipCollection(user, user_decision)
            chipCollection(opponent, user_decision)

        if round_flag:
            cardDeal(deck, river)
            print("Chips left: " + str(user.chips) + ', Opponent\'s chips: ' + str(opponent.chips))
            for i in range(0, len(user.hand)):
                print('Card ' + str(i+1) + ': ' + str(cardValueDisplay(user.hand[i].value)) + ' of ' + suitDisplay(user.hand[i].suit))
            for i in range(0, len(river.hand)):
                print('River card ' + str(i+1) + ': ' + str(cardValueDisplay(river.hand[i].value)) + ' of ' + suitDisplay(river.hand[i].suit))

            user_decision = callFoldOrRaise(user)
            if isinstance(user_decision, str):
                if user_decision == 'fold':
                    round_flag = False
                    playerWin(opponent, user)
                elif user_decision == 'call':
                    pass
            else:
                chipCollection(user, user_decision)
                chipCollection(opponent, user_decision)

            if round_flag:
                cardDeal(deck, river)
                print("Chips left: " + str(user.chips) + ', Opponent\'s chips: ' + str(opponent.chips))
                for i in range(0, len(user.hand)):
                    print(
                        'Card ' + str(i + 1) + ': ' + str(cardValueDisplay(user.hand[i].value)) + ' of ' + suitDisplay(user.hand[i].suit))
                for i in range(0, len(river.hand)):
                    print('River card ' + str(i + 1) + ': ' + str(cardValueDisplay(river.hand[i].value)) + ' of ' + suitDisplay(
                        river.hand[i].suit))

                user_decision = callFoldOrRaise(user)
                if isinstance(user_decision, str):
                    if user_decision == 'fold':
                        playerWin(opponent, user)
                        round_flag = False
                    elif user_decision == 'call':
                        pass
                else:
                    chipCollection(user, user_decision)
                    chipCollection(opponent, user_decision)

                if round_flag:
                    cardDeal(deck, river)
                    print("Chips left: " + str(user.chips) + ', Opponent\'s chips: ' + str(opponent.chips))
                    for i in range(0, len(user.hand)):
                        print('Card ' + str(i + 1) + ': ' + str(cardValueDisplay(user.hand[i].value)) + ' of ' + suitDisplay(
                            user.hand[i].suit))
                    for i in range(0, len(river.hand)):
                        print('River card ' + str(i + 1) + ': ' + str(cardValueDisplay(river.hand[i].value)) + ' of ' + suitDisplay(
                            river.hand[i].suit))

                    user_decision = callFoldOrRaise(user)
                    if isinstance(user_decision, str):
                        if user_decision == 'fold':
                            playerWin(opponent, user)
                            round_flag = False
                        elif user_decision == 'call':
                            pass
                    else:
                        chipCollection(user, user_decision)
                        chipCollection(opponent, user_decision)

                    if round_flag:
                        user.hand_score = handValue(user, river)
                        opponent.hand_score = handValue(opponent, river)
                        showDown(user, opponent, river)

        print("You currently have " + str(user.chips) + ' chips remaining.')
        print("Your opponent currently has " + str(opponent.chips) + ' chips remaining.')
        print('Buy-in is currently at ' + str(ante) + ' chips each round.\n')

        if user.chips < ante or opponent.chips < ante:      # ends the game when someone has no chips left. Can be improved
            break

        if input("The next round will begin shortly, enter any command to continue, or 'quit' to end the game.") == 'quit':
            break

main()