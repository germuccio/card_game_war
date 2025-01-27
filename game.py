import random
from enum import Enum
from typing import List, Optional


class Suit(Enum):
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"
    SPADES = "Spades"


class Rank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    @property
    def display(self):
        if self.value <= 10:
            return str(self.value)
        return self.name.capitalize()


class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank.display} of {self.suit.value}"

    def __lt__(self, other):
        return self.rank.value < other.rank.value


class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self._create_deck()

    def _create_deck(self):
        self.cards = [Card(suit, rank) for suit in Suit for rank in Rank]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards: int) -> List[Card]:
        if num_cards > len(self.cards):
            raise ValueError("Not enough cards in deck")
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards


class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand: List[Card] = []
        self.score = 0

    def add_cards(self, cards: List[Card]):
        self.hand.extend(cards)

    def play_card(self) -> Optional[Card]:
        if not self.hand:
            return None
        return self.hand.pop(0)

    def add_to_score(self, points: int = 1):
        self.score += points


class Game:
    def __init__(self, player1_name: str, player2_name: str):
        self.deck = Deck()
        self.player1 = Player(player1_name)
        self.player2 = Player(player2_name)
        self.round_number = 0

    def setup_game(self):
        self.deck.shuffle()
        cards_per_player = len(self.deck.cards) // 2
        self.player1.add_cards(self.deck.deal(cards_per_player))
        self.player2.add_cards(self.deck.deal(cards_per_player))

    def play_round(self) -> Optional[Player]:
        self.round_number += 1
        print(f"\nRound {self.round_number}")

        card1 = self.player1.play_card()
        card2 = self.player2.play_card()

        if not card1 or not card2:
            return None

        print(f"{self.player1.name} plays: {card1}")
        print(f"{self.player2.name} plays: {card2}")

        if card1.rank.value > card2.rank.value:
            self.player1.add_to_score()
            winner = self.player1
        elif card2.rank.value > card1.rank.value:
            self.player2.add_to_score()
            winner = self.player2
        else:
            print("It's a tie!")
            return None

        print(f"{winner.name} wins the round!")
        return winner

    def play_game(self):
        self.setup_game()
        print("Game started!")
        print(f"Players: {self.player1.name} vs {self.player2.name}")
        print("\nPress Enter to play each round or 'q' to quit")

        while self.player1.hand and self.player2.hand:
            user_input = input("\nPress Enter to continue or 'q' to quit: ")
            if user_input.lower() == 'q':
                print("\nGame terminated by user!")
                return
                
            self.play_round()
            print(f"Cards remaining - {self.player1.name}: {len(self.player1.hand)}, "
                  f"{self.player2.name}: {len(self.player2.hand)}")
            print(f"Scores - {self.player1.name}: {self.player1.score}, "
                  f"{self.player2.name}: {self.player2.score}")

        print("\nGame Over!")
        if self.player1.score > self.player2.score:
            winner = self.player1
        elif self.player2.score > self.player1.score:
            winner = self.player2
        else:
            print("It's a tie game!")
            return

        print(f"{winner.name} wins the game with {winner.score} points!")


def get_player_name(player_number: int) -> str:
    while True:
        name = input(f"Enter name for Player {player_number}: ").strip()
        if name:  # Check if name is not empty
            return name
        print("Name cannot be empty. Please try again.")

if __name__ == "__main__":
    print("Welcome to the Card Game!")
    print("-------------------------")
    player1_name = get_player_name(1)
    player2_name = get_player_name(2)
    
    game = Game(player1_name, player2_name)
    game.play_game()