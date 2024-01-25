# game_logic.py
import random

class PokerGame:
    deck = []

    def __init__(self):
        self.players = []
        self.current_turn = 0
        self.last_card_played = None

    @staticmethod
    def get_shuffled_deck():
        shuffled_deck = PokerGame.deck.copy()
        random.shuffle(shuffled_deck)
        return shuffled_deck

    def start_game(self):
        self.display_full_deck()
        self.initialize_deck()
        self.initialize_players()
        PokerGame.deck = self.get_shuffled_deck()
        self.last_card_played = PokerGame.deck.pop(0)
        print(f"Game started! The first card displayed is: {self.last_card_played}")
        print(f"It's now {self.players[self.current_turn]['name']}'s turn.")

    def initialize_deck(self):
        PokerGame.deck = [
            {"rank": str(rank), "suit": suit}
            for rank in list(range(2, 11)) + ["A"]
            for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]
        ]

    def initialize_players(self):
        self.players = [
            {"name": "User", "hand": []},
            {"name": "PC", "hand": []}
        ]

    def display_hand(self, player_name):
        current_player = next(player for player in self.players if player['name'] == player_name)
        print(f"{current_player['name']}'s hand: {current_player['hand']}")

    def display_full_deck(self):
        print("Full Deck:")
        for card in self.deck:
            print(f"{card['rank']} of {card['suit']}")

    def play_card(self, player_name, card_choice=None):
        current_player = next(player for player in self.players if player['name'] == player_name)

        if player_name == 'User':
            choice = input(f"{current_player['name']}, do you want to (1) play a card or (2) draw a card? Enter 1 or 2: ")
            if choice == '1':
                card_played = self.choose_card_from_hand(current_player) if card_choice is None else card_choice
            elif choice == '2':
                card_played = self.draw_card(current_player)
            else:
                print("Invalid choice. Please enter 1 or 2.")
                self.play_card(player_name, card_choice)
        else:
            card_played = self.generate_pc_move()

        while not self.is_valid_play(card_played):
            print("Invalid play! Please choose a valid card.")
            card_played = self.choose_card_from_hand(current_player) if player_name == 'User' else self.generate_pc_move()

        print(f"{current_player['name']} played: {card_played}")
        current_player['hand'].remove(card_played)
        self.last_card_played = card_played

        if not current_player['hand']:
            print(f"{current_player['name']} has won the game!")
            self.end_game_options(current_player)

        self.next_turn()

    def choose_card_from_hand(self, current_player):
        card_played_str = input(f"{current_player['name']}, choose a card from your hand: ")
        card_played = self.parse_card_string(card_played_str)

        while card_played not in current_player['hand']:
            print("Invalid choice! The card is not in your hand. Choose a card from your hand.")
            card_played_str = input(f"{current_player['name']}, choose a card from your hand: ")
            card_played = self.parse_card_string(card_played_str)

        return card_played

    def generate_pc_move(self):
        current_player = self.players[self.current_turn]

        for card in current_player['hand']:
            if self.is_winning_card(card):
                return card

        for card in current_player['hand']:
            if self.is_valid_play(card):
                return card

        return self.draw_card(current_player)

    def parse_card_string(self, card_str):
        rank_str, suit_str = card_str[:-1], card_str[-1]
        return {"rank": rank_str, "suit": suit_str}

    def is_valid_play(self, card):
        return (
            card['rank'] not in ['Q', '8', '2', '3', 'A']
            and card['rank'] == self.last_card_played['rank']
        )

    def is_winning_card(self, card):
        return (
            card['rank'] not in ['Q', '8', '2', '3', 'A']
        )

    def draw_card(self, current_player):
        card_drawn = PokerGame.deck.pop(0)
        current_player['hand'].append(card_drawn)
        return card_drawn

    def next_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.players)
        print(f"It's now {self.players[self.current_turn]['name']}'s turn.")

    def end_game_options(self, winner):
        option = input(f"{winner['name']} has won! Do you want to (1) start a new game or (2) quit? Enter 1 or 2: ")
        if option == '1':
            self.start_game()
        elif option == '2':
            print("Thanks for playing! Goodbye.")
            exit()
        else:
            print("Invalid option. Please enter 1 or 2.")
            self.end_game_options(winner)
