import random
from typing import List, Optional

class Card:
    """Represents a single playing card."""
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    
    def __init__(self, suit: str, rank: str):
        """Initialize a card with a suit and rank."""
        self.suit = suit
        self.rank = rank
        self.value = self.RANKS.index(rank)
    
    def __repr__(self):
        """String representation of the card."""
        return f"{self.rank} of {self.suit}"
    
    def __lt__(self, other):
        """Compare card values for sorting and comparison."""
        return self.value < other.value
    
    def __eq__(self, other):
        """Check if cards have the same value."""
        return self.value == other.value

class Deck:
    """Represents a standard 52-card deck."""
    def __init__(self):
        """Create a full deck of cards."""
        self.cards = [
            Card(suit, rank) 
            for suit in Card.SUITS 
            for rank in Card.RANKS
        ]
    
    def shuffle(self):
        """Shuffle the deck of cards."""
        random.shuffle(self.cards)
    
    def deal(self, num_players: int) -> List[List[Card]]:
        """Deal cards equally to specified number of players."""
        self.shuffle()
        hands = [[] for _ in range(num_players)]
        for i, card in enumerate(self.cards):
            hands[i % num_players].append(card)
        return hands

class Player:
    """Represents a player in the War card game."""
    def __init__(self, name: str, cards: List[Card]):
        """Initialize a player with a name and cards."""
        self.name = name
        self.cards = cards
    
    def play_card(self) -> Optional[Card]:
        """Play the top card from the player's hand."""
        return self.cards.pop(0) if self.cards else None
    
    def add_cards(self, cards: List[Card]):
        """Add cards to the player's hand."""
        self.cards.extend(cards)
    
    def has_cards(self) -> bool:
        """Check if the player still has cards."""
        return len(self.cards) > 0

class WarGame:
    """Manages the War card game logic."""
    def __init__(self, player_names: List[str] = None):
        """Initialize the game with players."""
        # Default to two players if no names provided
        if player_names is None:
            player_names = ['Player 1', 'Player 2']
        
        # Create and deal the deck
        deck = Deck()
        hands = deck.deal(len(player_names))
        
        # Create players
        self.players = [
            Player(name, hand) 
            for name, hand in zip(player_names, hands)
        ]
        
        # Track game state
        self.round = 0
        self.max_rounds = 1000  # Prevent infinite game
    
    def play_round(self) -> Optional[str]:
        """Play a single round of War."""
        self.round += 1
        
        # Check if game should end
        if self.round > self.max_rounds:
            return "Game ended in a draw"
        
        # Track cards played this round
        played_cards = []
        current_players = []
        
        # Each active player plays a card
        for player in self.players:
            if not player.has_cards():
                continue
            
            card = player.play_card()
            played_cards.append(card)
            current_players.append(player)
        
        # If only one player remains, they win
        if len(current_players) == 1:
            return f"{current_players[0].name} wins by default!"
        
        # Find the highest card
        max_card = max(played_cards)
        max_indices = [
            i for i, card in enumerate(played_cards) 
            if card == max_card
        ]
        
        # Handle war (tie)
        if len(max_indices) > 1:
            # Collect war cards
            war_cards = []
            war_players = [current_players[i] for i in max_indices]
            
            # Each war player puts down 3 cards face down
            for player in war_players:
                war_cards.extend(
                    player.play_card() for _ in range(3) 
                    if player.has_cards()
                )
                
                # Last card is the war card
                if player.has_cards():
                    card = player.play_card()
                    played_cards.append(card)
                    war_cards.append(card)
            
            # Winner takes all cards
            winner = max(war_players, key=lambda p: played_cards[current_players.index(p)])
            winner.add_cards(played_cards + war_cards)
            return f"War! {winner.name} wins the round"
        
        # Normal round - winner takes all cards
        winner = current_players[played_cards.index(max_card)]
        winner.add_cards(played_cards)
        
        return f"{winner.name} wins the round"
    
    def play_game(self) -> str:
        """Play the entire game until a winner is determined."""
        while True:
            # Count active players
            active_players = [p for p in self.players if p.has_cards()]
            
            # End game if only one player has cards
            if len(active_players) == 1:
                return f"{active_players[0].name} wins the game!"
            
            # Play a round
            result = self.play_round()
            
            # Optional: Uncomment to see round-by-round progress
            # print(f"Round {self.round}: {result}")
        
# Example game play
def main():
    game = WarGame()
    winner = game.play_game()
    print(winner)

if __name__ == "__main__":
    main()