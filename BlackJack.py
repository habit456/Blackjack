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

    def card_count(self):
        return len(self.cards)

    def display_whole_deck(self):
        for c in self.cards:
            print(c)


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

    def check_blackjack(self):
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

    def sub_money(self, sub):
        self.money -= sub

    def show_money(self):
        print('\nYour money: ' + str(self.money))

    def set_bet(self):
        player_bet = int(input('How much would you like to bet?'))
        self.sub_money(player_bet)
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


def hit_or_stay(deck_obj, player_obj):
    user_input = input('\nWould you like to hit or stay? hit/stay: ').lower()
    if user_input == 'hit':
        player_obj.add_card(deck_obj)
        player_obj.set_card_value()
        if player_obj.check_bust():
            return 'bust'
        else:
            return 'hit'
    elif user_input == 'stay':
        return 'stay'
    else:
        return hit_or_stay(deck_obj, player_obj)


def user_interface(deck_obj, player_obj, dealer_obj):
    player_obj.clear()
    dealer_obj.clear()

    player_obj.show_money()
    player_obj.set_bet()
    print('\nDealing...')
    sleep(1)
    deck_obj.shuffle(True)

    dealer_obj.add_card(deck_obj)
    dealer_obj.add_card(deck_obj)
    player_obj.add_card(deck_obj)
    player_obj.add_card(deck_obj)

    dealer_obj.set_card_value()
    player_obj.set_card_value()

    if player_obj.check_blackjack():
        player_obj.display()
        print('Blackjack!')
        player_obj.add_money(player_obj.bet * 3)
        player_obj.show_money()
        again = input('\nWould you like to play again? y/n').lower()
        if again == 'y':
            return user_interface(deck_obj, player_obj, dealer_obj)
        else:
            return 'Finished'

    dealer_obj.display(True)
    player_obj.display()

    hit_stay_choice = None
    while hit_stay_choice != 'stay' and hit_stay_choice != 'bust':
        hit_stay_choice = hit_or_stay(deck_obj, player_obj)
        if hit_stay_choice != 'stay' and hit_stay_choice != 'bust':
            player_obj.display()

    if hit_stay_choice == 'bust':
        print('Bust!')
        player_obj.show_money()
        again = input('\nWould you like to play again? y/n').lower()
        if again == 'y':
            return user_interface(deck_obj, player_obj, dealer_obj)
        else:
            return 'Finished'

    sleep(1)
    dealer_obj.display(False)

    while dealer_obj.card_value < 17:
        sleep(1)
        dealer_obj.add_card(deck_obj)
        dealer_obj.set_card_value()
        dealer_obj.display(False)

    if dealer_obj.check_bust():
        print('Dealer bust!')
        player_obj.add_money(player_obj.bet * 2)
        player_obj.show_money()
        again = input('\nWould you like to play again? y/n').lower()
        if again == 'y':
            return user_interface(deck_obj, player_obj, dealer_obj)
        else:
            return 'Finished'
    else:
        if player_obj.card_value > dealer_obj.card_value:
            print("\n" + player_obj.name + ' ' + 'wins!')
            player_obj.add_money(player_obj.bet * 2)
            player_obj.show_money()
            again = input('\nWould you like to play again? y/n').lower()
            if again == 'y':
                return user_interface(deck_obj, player_obj, dealer_obj)
            else:
                return 'Finished'
        elif player_obj.card_value < dealer_obj.card_value:
            print("\n" + player_obj.name + ' ' + 'loses!')
            player_obj.show_money()
            again = input('\nWould you like to play again? y/n').lower()
            if again == 'y':
                return user_interface(deck_obj, player_obj, dealer_obj)
            else:
                return 'Finished'
        else:
            print('\nPush!')
            player_obj.add_money(player_obj.bet)
            player_obj.show_money()
            again = input('\nWould you like to play again? y/n').lower()
            if again == 'y':
                return user_interface(deck_obj, player_obj, dealer_obj)
            else:
                return 'Finished'


print('Welcome to Blackjack 1.0')
new_deck = Deck()
new_player = Player()
new_dealer = Dealer()
new_player.set_name()
user_interface(new_deck, new_player, new_dealer)

