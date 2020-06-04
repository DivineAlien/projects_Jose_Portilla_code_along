"""
milestone project for python course
blackjack
"""
import random


print('inside my blackjack module')
suites = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
         'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7,
          'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10,
          'Ace': 11}
player_hits = True
playing = True


class Card:
    """
    card object representation of a card in blackjack

    attributes
    ----------
    suite
    rank
    """

    def __init__(self, suite: str, rank: str):
        """
        creating a card
        """
        self.suite = suite
        self.rank = rank

    def __str__(self):
        """
        :return: str
        """
        return f'{self.rank} of {self.suite}'


class Deck:
    """
    this is a deck object that have array of 52 card objects

    attribute
    ---------
    deck

    methods
    --------
    shuffle
    deal
    """

    def __init__(self):
        # starting with empty deck then creating it
        self.deck = []
        for suite in suites:
            for rank in ranks:
                self.deck.append(Card(suite, rank))

    def __str__(self):
        """
        showing the cards in the deck
        :return: List[Card]
        """
        return str([card.__str__() for card in self.deck])

    def shuffle(self):
        """
        shuffling the cards in the deck
        :return: None
        """
        random.shuffle(self.deck)

    def deal(self):
        """
        :return: Card
        """
        return self.deck.pop()


class Hand:
    """
    hold the cards value
    adjust the aces values

    attributes
    -------------
    cards: array
    value: int
    aces_with_value_of_11: int

    methods
    --------
    add_card
    adjust_value_for_ace
    """

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces_with_value_of_11 = 0

    def add_card(self, card: Card):
        """
        adds card object from Deck.deal()
        and sets it's value
        """
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == 'Ace':
            self.aces_with_value_of_11 += 1

    def adjust_value_for_ace(self):
        """
        if the is a ace that it's value counted as 11
        then value will subtract by 10 and ace will be removed from the list
        """
        while self.value > 21 and self.aces_with_value_of_11:
            self.value -= 10
            self.aces_with_value_of_11 -= 1


class Chips:
    """
    chips object for bets

    attributes
    ----------
    total
    bet

    methods
    -----------
    win_bet
    lose_bet
    """

    def __init__(self, total: int = 100, bet: int = 1):
        self.total = total
        self.bet = bet

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


"""
functions for playing the black jack game
take_bet
"""


def take_bet(chips: Chips):
    """
    from input asks player how many chips do they wanna bet
    and set the bet for chips object inplace
    """

    total = chips.total

    while True:
        try:
            chips.bet = int(input(f'please enter your bet amount\tcurrent chips = {total}\n'))
        except ValueError:
            print('please enter a number')
        else:
            if chips.bet > total:
                print('you don\'t have enough chips\n')
            else:
                break


def take_hit(deck: Deck, hand: Hand):
    """
    if a player take a hit this function will be called
    """
    hand.add_card(deck.deal())
    hand.adjust_value_for_ace()


def hit_or_stand(deck: Deck, hand: Hand):

    global player_hits

    while True:
        player_answer = input('please enter [hit] or [stand]\n').lower()
        if player_answer == 'hit':
            take_hit(deck, hand)
            break
        elif player_answer == 'stand':
            player_hits = False
            break
        else:
            print('please enter [hit] or [stand]')
            continue


def show_visible_cards(player: Hand, dealer: Hand):
    """
    show all cards from player hands
    show all cards except last one from dealers hand
    """
    print(f'dealer visible cards:\n{[card.__str__() for card in dealer.cards[0:-1]]}\none card hidden\n')
    print(f'player cards: \n{[card.__str__() for card in player.cards]}\nvalue={player.value}')


def show_all_cards(player: Hand, dealer: Hand):
    """
    show all cards from both player and dealer
    """
    print(f'dealer all cards: \n{[card.__str__() for card in dealer.cards]}\nvalue={dealer.value}')
    print(f'player all cards: \n{[card.__str__() for card in player.cards]}\nvalue={player.value}')


def player_busts(chips: Chips):

    print('player busted')
    chips.lose_bet()


def player_wins(chips: Chips):

    print('player won')
    chips.win_bet()


def dealer_busts(chips: Chips):

    print('dealer busts player wins')
    chips.win_bet()


def dealer_wins(chips: Chips):

    print('dealer wins player busts')
    chips.lose_bet()


def push():

    print('player and dealer tie! PUSH')


"""
logic that starts the game
controls the game flow while the it's executing
"""


def play():
    global player_hits
    global playing

    # Set up the Player's chips
    player_chips = Chips()

    # while the player have chips and want to play the game
    while player_chips.total and playing:
        # Print an opening statement
        print('welcome to blackjack')
        player_hits = True

        # Create & shuffle the deck, deal two cards to each player
        deck = Deck()
        deck.shuffle()

        player_hand = Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())

        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        # Prompt the Player for their bet
        take_bet(player_chips)

        # Show cards (but keep one dealer card hidden)
        show_visible_cards(player_hand, dealer_hand)

        while player_hits:  # recall this variable from our hit_or_stand function

            # Prompt for Player to Hit or Stand
            hit_or_stand(deck, player_hand)

            # Show cards (but keep one dealer card hidden)
            show_visible_cards(player_hand, dealer_hand)

            # If player's hand exceeds 21, run player_busts() and break out of loop
            if player_hand.value > 21:
                player_busts(player_chips)
                break

        # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                take_hit(deck, dealer_hand)

            # Show all cards
            show_all_cards(player_hand, dealer_hand)

            # Run different winning scenarios
            if dealer_hand.value > 21:
                dealer_busts(player_chips)
            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_chips)
            elif dealer_hand.value < player_hand.value:
                player_wins(player_chips)
            else:
                push()

        # Inform Player of their chips total
        print(f'player total chips are {player_chips.total}')

        # Ask to play again
        while player_chips.total:
            play_again = input('do you want to play again? y/n\n').lower()
            if play_again[0] == 'y':
                break
            elif play_again[0] == 'n':
                playing = False
                break
            else:
                print('please enter [y] or [n]')


# -----------------
# ---game starts
# -----------------
if __name__ == '__main__':
    play()
