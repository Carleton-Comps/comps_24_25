import asyncio

import numpy as np

from poke_env.player import RandomPlayer
from poke_env.teambuilder import Teambuilder


class SingleTeamTeambuilder(Teambuilder):
    def __init__(self, team):
        self.team = self.join_team(self.parse_showdown_team(team))

    def yield_team(self):
        return self.team


# class RandomTeamFromPool(Teambuilder):
#     def __init__(self, teams):
#         self.teams = [self.join_team(self.parse_showdown_team(team)) for team in teams]

#     def yield_team(self):
#         return np.random.choice(self.teams)
     

team = """
Bloodmoon Ursaluna (M) @ Assault Vest
Ability: Mind's Eye
EVs: 252 HP / 252 SpA / 4 SpD
Modest Nature
IVs: 0 Atk
- Blood Moon
- Earth Power
- Moonblast
- Vacuum Wave

Dragonite (M) @ Loaded Dice
Ability: Multiscale
EVs: 252 Atk / 252 Spe / 4 HP
Adamant  Nature
IVs: 0 Atk
- Extreme Speed
- Scale Shot
- Fire Punch
- Dragon Dance

Gholdengo (M) @ Covert Cloak
Ability: Good as Gold
EVs: 208 SpA / 212 HP / 84 Spe / 4 Def
Modest Nature
- Make It Rain
- Shadow Ball
- Psyshock
- Nasty Plot

Archaludon (M) @ Sitrus Berry
Ability: Stamina
EVs: 204 HP / 28 Atk / 20 Def / 252 SpD / 4 Spe
Bold Nature
- Dragon Tail
- Body Press
- Foul Play
- Stealth Rock

Dondozo (M) @ Leftovers
Ability: Unaware
EVs: 252 HP / 252 Def / 4 SpD
Lax Nature
- Wave Crash
- Curse
- Yawn
- Protect

Meowscarada (M) @ Choice Band
Ability: Protean
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Flower Trick
- Knock Off
- Triple Axel
- U-Turn
"""
custom_builder = SingleTeamTeambuilder(team)
# custom_builder = RandomTeamFromPool([team_1, team_2])


async def main():

    # try:
    #     # Create players
    #     player1 = MinMaxAgent(battle_format="gen9randombattle", max_depth=2)
    #     player2 = RandomPlayer(battle_format="gen9randombattle")

    #     print("Starting battle...")
    #     print("Player 1: MinMax Agent")
    #     print("Player 2: Random Agent")

    #     # Run any number of battles
    #     await player1.battle_against(player2, n_battles=50)

    #     print("\nBattle Results:")
    #     print(f"MinMax Agent wins: {player1.n_won_battles}")
    #     print(f"Random Agent wins: {player2.n_won_battles}")

    # except Exception as e:
    #     print(f"Error in main: {str(e)}")

    # We create two players
    player_1 = RandomPlayer(
        battle_format="gen9ou", team=custom_builder, max_concurrent_battles=10
    )
    player_2 = RandomPlayer(
        battle_format="gen9ou", team=custom_builder, max_concurrent_battles=10
    )

    await player_1.battle_against(player_2, n_battles=5)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())