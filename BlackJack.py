import numpy.random as npr
from time import sleep


class Deck:
    def __init__(self):
        self.cards = None

    def create(self):
        suits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        deck = [r + '-' + s for r in ranks for s in suits]
        self.cards = deck

    def shuffle(self, create_new_deck=False):
        if create_new_deck:
            self.create()

        deck = self.cards.copy()
        shuffled = []

        while deck:
            random_choice = npr.randint(0, len(deck))
            shuffled.append(deck[random_choice])
            del deck[random_choice]

        self.cards = shuffled

    def draw_card(self):
        deck = self.cards
        random_choice = npr.randint(0, len(deck))
        card = deck[random_choice]
        del self.cards[random_choice]
        return card


class Game:
    def __init__(self):
        self.cards = []
        self.card_value = 0

    def check_bust(self):
        return self.card_value > 21

    def set_card_value(self):
        rank_list = list(map(lambda c: c.split('-')[0], self.cards))
        rank_dict = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                     '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}
        non_aces = list(filter(lambda c: c != 'A', rank_list))
        aces = list(filter(lambda c: c == 'A', rank_list))
        self.card_value = 0

        for c in non_aces:
            self.card_value += rank_dict[c]

        if aces:
            for a in aces:
                if self.card_value + 11 > 21:
                    self.card_value += 1
                else:
                    self.card_value += 11

    def has_blackjack(self):
        if len(self.cards) == 2:
            rank_list = list(map(lambda c: c.split('-')[0], self.cards))
            if 'A' in rank_list:
                tens = ['10', 'K', 'Q', 'J']
                for r in tens:
                    if r in rank_list:
                        return True
        return False

    def add_card(self, deck):
        card = deck.draw_card()
        self.cards.append(card)


class Player(Game):
    def __init__(self, money=2000):
        super(Player, self).__init__()
        self.name = None
        self.money = money
        self.bet = 0

    def set_name(self):
        name = input('Please enter your name: ')
        self.name = name

    def add_money(self, winnings):
        self.money += winnings

    def show_money(self):
        print('\nYour money: ' + str(self.money))

    def set_bet(self):
        player_bet = int(input('How much would you like to bet?'))
        self.money -= player_bet
        self.bet = player_bet

    def clear(self):
        self.bet = 0
        self.cards = []
        self.card_value = 0

    def display(self):
        print()
        print(self.name)
        print("Cards: " + str(self.cards))
        print("Card Value: " + str(self.card_value))
        print('Money: ' + str(self.money) + ', ' + 'Bet: ' + str(self.bet))

    def initialize(self, deck_obj):
        self.clear()
        self.show_money()
        self.set_bet()
        self.add_card(deck_obj)
        self.add_card(deck_obj)
        self.set_card_value()

    def hit_or_stay(self, deck_obj):
        user_input = input('\nWould you like to hit or stay? hit/stay: ').lower()
        if user_input == 'hit':
            self.add_card(deck_obj)
            self.set_card_value()
            if self.check_bust():
                return 'bust'
            else:
                return 'hit'
        elif user_input == 'stay':
            return 'stay'
        else:
            return self.hit_or_stay(deck_obj)

    def turn(self, deck_obj):
        hit_stay_choice = None
        while hit_stay_choice != 'stay' and hit_stay_choice != 'bust':
            hit_stay_choice = self.hit_or_stay(deck_obj)
            if hit_stay_choice != 'stay' and hit_stay_choice != 'bust':
                self.display()


class Dealer(Game):
    def __init__(self):
        super(Dealer, self).__init__()
        self.name = 'Dealer'

    def clear(self):
        self.cards = []
        self.card_value = 0

    def display(self, which=True):
        """True for hidden, False for full"""
        if which:
            hidden = ['X', self.cards[1]]
            print()
            print(self.name)
            print("Cards: " + str(hidden))
        else:
            print()
            print(self.name)
            print("Cards: " + str(self.cards))
            print("Card Value: " + str(self.card_value))

    def initialize(self, deck_obj):
        self.clear()
        self.add_card(deck_obj)
        self.add_card(deck_obj)
        self.set_card_value()

    def turn(self, deck_obj):
        while self.card_value < 17:
            sleep(1)
            self.add_card(deck_obj)
            self.set_card_value()
            self.display(False)


def user_interface(deck_obj, player_obj, dealer_obj):
    deck_obj.shuffle(True)
    player_obj.initialize(deck_obj)
    dealer_obj.initialize(deck_obj)

    print('\nDealing...')
    sleep(1)

    if player_obj.has_blackjack():
        player_obj.display()
        print('Blackjack!')
        player_obj.add_money(player_obj.bet * 3)
    else:
        dealer_obj.display(True)
        player_obj.display()
        player_obj.turn(deck_obj)

        if player_obj.check_bust():
            player_obj.display()
            print('\nBust!')
        else:
            sleep(1)
            dealer_obj.display(False)
            dealer_obj.turn(deck_obj)

            if dealer_obj.check_bust():
                print('Dealer bust!')
                player_obj.add_money(player_obj.bet * 2)
            else:
                if player_obj.card_value > dealer_obj.card_value:
                    print("\n" + player_obj.name + ' ' + 'wins!')
                    player_obj.add_money(player_obj.bet * 2)
                elif player_obj.card_value < dealer_obj.card_value:
                    print("\n" + player_obj.name + ' ' + 'loses!')
                else:
                    print('\nPush!')
                    player_obj.add_money(player_obj.bet)

        player_obj.show_money()
        again = input('\nWould you like to play again? y/n').lower()
        if again == 'y':
            return user_interface(deck_obj, player_obj, dealer_obj)
        else:
            return 'Finished'


print('Welcome to Blackjack Version 1.5')
new_deck = Deck()
new_player = Player()
new_dealer = Dealer()
new_player.set_name()
user_interface(new_deck, new_player, new_dealer)
