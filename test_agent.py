import asyncio
from poke_env import RandomPlayer, LocalhostServerConfiguration, AccountConfiguration

async def main():
    try:
        # Create server configuration for localhost
        server_config = LocalhostServerConfiguration

        # Create account configurations for both players
        # For local server with --no-security, we don't need passwords
        account_config_1 = AccountConfiguration("TestPlayer1", None)
        account_config_2 = AccountConfiguration("TestPlayer2", None)

        # Initialize players with proper configurations
        player1 = RandomPlayer(
            battle_format="gen9randombattle",
            server_configuration=server_config,
            account_configuration=account_config_1,
            max_concurrent_battles=1,
            log_level=20  # INFO level logging
        )
        
        player2 = RandomPlayer(
            battle_format="gen9randombattle",
            server_configuration=server_config,
            account_configuration=account_config_2,
            max_concurrent_battles=1,
            log_level=20
        )

        print("Connecting to local Pokemon Showdown server...")
        
        # Start a battle between the two players
        print("Starting battle...")
        await player1.battle_against(player2, n_battles=1)

        # Print results
        print("\nBattle Results:")
        print(f"Player 1 ({player1.username}) won "
              f"{player1.n_won_battles} battles out of {player1.n_finished_battles}")
        print(f"Player 2 ({player2.username}) won "
              f"{player2.n_won_battles} battles out of {player2.n_finished_battles}")

        # Print specific battle results
        for battle_tag, battle in player1.battles.items():
            print(f"Battle {battle_tag}: {'Won' if battle.won else 'Lost'}")

    except ConnectionRefusedError:
        print("\nError: Could not connect to the Pokemon Showdown server.")
        print("Please ensure you have:")
        print("1. Installed Pokemon Showdown locally")
        print("2. Started the server with: node pokemon-showdown start --no-security")
        print("3. The server is running on the default localhost port")
    
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print("Please check your setup and try again.")

if __name__ == "__main__":
    # Verify python version
    import sys
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)

    print("Starting Pokemon Showdown test agent...")
    print("Make sure your local Pokemon Showdown server is running with --no-security flag")
    
    # Create and run the event loop
    asyncio.get_event_loop().run_until_complete(main())