from poke_env.player.player import Player
from poke_env.player.battle_order import BattleOrder
import random

class CustomRandomAgent(Player):
    def choose_move(self, battle):
        """
        Implements the agent's logic for choosing a move in battle.
        This simple agent just picks moves completely at random.
        
        Args:
            battle: Battle instance representing the current state
            
        Returns:
            A string representing the chosen action in showdown format
        """
        # First, check if we have any available moves
        if battle.available_moves:
            # Randomly choose from available moves
            chosen_move = random.choice(battle.available_moves)
            return self.create_order(chosen_move)
            
        # If no moves are available, choose random switch
        elif battle.available_switches:
            chosen_switch = random.choice(battle.available_switches)
            return self.create_order(chosen_switch)
            
        # If no moves or switches available, struggle
        return self.create_order(BattleOrder.STRUGGLE)

    def teampreview(self, battle):
        """
        Implements team preview logic.
        This agent just picks a random team order.
        
        Args:
            battle: Battle instance representing the current state
            
        Returns:
            String of team order in showdown format
        """
        # Get list of indexes from 1 to team size
        team_indexes = list(range(1, len(battle.team) + 1))
        # Randomly shuffle them
        random.shuffle(team_indexes)
        # Return order in showdown's format
        return "/team " + "".join([str(i) for i in team_indexes])


async def main():
    try:
        # Create two instances of our custom agent
        player1 = CustomRandomAgent(
            battle_format="gen9randombattle",
            log_level=20  # INFO level to see what's happening
        )
        
        player2 = CustomRandomAgent(
            battle_format="gen9randombattle",
            log_level=20
        )

        print("Starting Pokemon Showdown test battle...")
        print("Make sure your local Pokemon Showdown server is running with --no-security flag")
        
        # Start a battle between the two players
        await player1.battle_against(player2, n_battles=1)

        # Print battle results
        print("\nBattle Results:")
        print(f"Player 1 won {player1.n_won_battles} battles out of {player1.n_finished_battles}")
        print(f"Player 2 won {player2.n_won_battles} battles out of {player2.n_finished_battles}")

        # Show specific battle outcomes
        for battle_tag, battle in player1.battles.items():
            print(f"Battle {battle_tag}: {'Won' if battle.won else 'Lost'}")
            
            # Print some battle statistics
            print(f"Number of turns: {battle.turn}")
            print(f"Won by: {'Player 1' if battle.won else 'Player 2'}")
            if battle.won:
                print("Winning Pokemon:", battle.active_pokemon.species)
            
    except ConnectionRefusedError:
        print("\nError: Could not connect to the Pokemon Showdown server.")
        print("Please ensure you have:")
        print("1. Started the server with: node pokemon-showdown start --no-security")
        print("2. The server is running on the default localhost port")
    
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.get_event_loop().run_until_complete(main())