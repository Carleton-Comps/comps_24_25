from poke_env.player.player import Player
from poke_env.player.battle_order import BattleOrder
from poke_env.environment.battle import Battle
from poke_env.environment.pokemon import Pokemon
from poke_env.player.random_player import RandomPlayer
from type_chart import TYPE_CHART
from vigor_chart import VIGOR_CHART
import numpy as np
from typing import List, Tuple, Optional, Union, Dict
import random


class MinMaxAgent(Player):
    def __init__(self, battle_format: str, max_depth: int = 2):
        super().__init__(battle_format=battle_format)
        self.max_depth = max_depth

    def choose_move(self, battle: Battle) -> BattleOrder:
        """Main method to choose moves using MinMax algorithm"""
        try:
            # If we need to switch Pokemon
            if battle.available_switches and not battle.available_moves:
                return self.create_order(random.choice(battle.available_switches))

            # Get moves for both players
            our_moves = self.get_possible_moves(battle)
            opponent_moves = self.get_possible_opponent_moves(battle)

            # Create payoff matrix
            payoff_matrix = self.create_payoff_matrix(battle, our_moves, opponent_moves)

            # Get best move using minimax and payoff matrix
            best_move = self.minimax(
                battle=battle,
                depth=self.max_depth,
                is_max_player=True,
                payoff_matrix=payoff_matrix,
            )

            if best_move is None or best_move[1] is None:
                return self.choose_random_move(battle)

            return self.create_order(best_move[1])

        except Exception as e:
            print(f"Error in choose_move: {str(e)}")
            return self.choose_random_move(battle)

    def create_payoff_matrix(
        self, battle: Battle, our_moves: List, opponent_moves: List
    ) -> Dict:
        """Create payoff matrix for all possible move combinations"""
        matrix = {}
        for our_move in our_moves:
            matrix[our_move] = {}
            for opp_move in opponent_moves:
                score = self.evaluate_move_combination(battle, our_move, opp_move)
                matrix[our_move][opp_move] = score
        return matrix

    def evaluate_move_combination(
        self,
        battle: Battle,
        our_move: Union[Pokemon, BattleOrder],
        opp_move: Union[Pokemon, BattleOrder],
    ) -> float:
        """Evaluate a specific move combination"""
        # Get base state evaluation
        base_score = self.evaluate_state(battle)

        # Additional move-specific scoring
        move_score = 0.0

        # Consider move power if it's an attack
        if isinstance(our_move, BattleOrder):
            move_score += getattr(our_move, "base_power", 0) * 0.5
            move_score += getattr(our_move, "accuracy", 100) * 0.1

        if isinstance(opp_move, BattleOrder):
            move_score -= getattr(opp_move, "base_power", 0) * 0.5

        return base_score + move_score

    def evaluate_state(self, battle: Battle) -> float:
        """Evaluate the current battle state"""
        try:
            # Get HP percentages (0-100)
            our_hp = battle.active_pokemon.current_hp_fraction * 100
            opponent_hp = battle.opponent_active_pokemon.current_hp_fraction * 100

            # Get Pokemon counts (0-6)
            our_pokemon_left = len(
                [mon for mon in battle.team.values() if not mon.fainted]
            )
            opponent_pokemon_left = len(
                [mon for mon in battle.opponent_team.values() if not mon.fainted]
            )

            # Calculate scores for different factors
            hp_score = our_hp - opponent_hp
            pokemon_score = (our_pokemon_left - opponent_pokemon_left) * 50
            status_score = 0

            # Status conditions
            if battle.active_pokemon.status is not None:
                status_score -= 20
            if battle.opponent_active_pokemon.status is not None:
                status_score += 20

            # Type advantage scoring
            type_score = 0
            our_types = battle.active_pokemon.types
            opponent_types = battle.opponent_active_pokemon.types

            # Calculate type advantage for our Pokemon against opponent
            for our_type in our_types:
                for opp_type in opponent_types:
                    if (
                        opp_type in TYPE_CHART
                        and our_type in TYPE_CHART[opp_type]["damageTaken"]
                    ):
                        damage_taken = TYPE_CHART[opp_type]["damageTaken"][our_type]
                        if damage_taken == 1:  # Super effective
                            type_score += 30
                        elif damage_taken == 2:  # Not very effective
                            type_score -= 15
                        elif damage_taken == 3:  # Immune
                            type_score -= 30

            # Calculate opponent's type advantage against us
            for opp_type in opponent_types:
                for our_type in our_types:
                    if (
                        our_type in TYPE_CHART
                        and opp_type in TYPE_CHART[our_type]["damageTaken"]
                    ):
                        damage_taken = TYPE_CHART[our_type]["damageTaken"][opp_type]
                        if damage_taken == 1:  # Super effective against us
                            type_score -= 30
                        elif damage_taken == 2:  # Not very effective against us
                            type_score += 15
                        elif damage_taken == 3:  # We're immune
                            type_score += 30

            # Vigor scoring
            vigor_score = 0

            # Calculate our Pokemon's vigor penalty
            if battle.active_pokemon.status:
                status = battle.active_pokemon.status.value
                if status in VIGOR_CHART:
                    vigor_info = VIGOR_CHART[status]
                    # Base penalty based on severity
                    base_penalty = vigor_info["severity"] * -10

                    # Additional penalties based on status effects
                    if "damage" in vigor_info:  # For burn, poison
                        vigor_score += base_penalty - 15
                    if "attack_modifier" in vigor_info:  # For burn
                        if any(
                            move.category == "PHYSICAL"
                            for move in battle.available_moves
                        ):
                            vigor_score -= 20
                    if "speed_modifier" in vigor_info:  # For paralysis
                        vigor_score -= 25
                    if "move_chance" in vigor_info:  # For sleep, freeze
                        if vigor_info["move_chance"] == 0:
                            vigor_score -= 40
                        else:
                            vigor_score -= 20

            # Calculate opponent's vigor penalty (reverse the scores)
            if battle.opponent_active_pokemon.status:
                status = battle.opponent_active_pokemon.status.value
                if status in VIGOR_CHART:
                    vigor_info = VIGOR_CHART[status]
                    base_bonus = vigor_info["severity"] * 10

                    if "damage" in vigor_info:
                        vigor_score += base_bonus + 15
                    if "attack_modifier" in vigor_info:
                        vigor_score += 20
                    if "speed_modifier" in vigor_info:
                        vigor_score += 25
                    if "move_chance" in vigor_info:
                        if vigor_info["move_chance"] == 0:
                            vigor_score += 40
                        else:
                            vigor_score += 20

            # Combine all scores
            total_score = (
                hp_score + pokemon_score + status_score + type_score + vigor_score
            )

            return total_score

        except Exception as e:
            print(f"Error in evaluate_state: {str(e)}")
            return 0.0

    def minimax(
        self, battle: Battle, depth: int, is_max_player: bool, payoff_matrix: Dict
    ) -> Tuple[float, Optional[Union[Pokemon, BattleOrder]]]:
        """Minimax algorithm using payoff matrix"""
        try:
            # Base case
            if depth == 0 or battle.finished:
                return self.evaluate_state(battle), None

            moves = (
                self.get_possible_moves(battle)
                if is_max_player
                else self.get_possible_opponent_moves(battle)
            )

            if not moves:
                return self.evaluate_state(battle), None

            best_move = moves[0]
            best_score = float("-inf") if is_max_player else float("inf")

            for move in moves:
                if is_max_player:
                    # Use worst possible outcome for this move
                    score = min(payoff_matrix[move].values())
                    if score > best_score:
                        best_score = score
                        best_move = move
                else:
                    # Use best possible outcome for opponent
                    score = max(payoff_matrix[move].values())
                    if score < best_score:
                        best_score = score
                        best_move = move

            return best_score, best_move

        except Exception as e:
            print(f"Error in minimax: {str(e)}")
            return 0.0, None

    def choose_random_move(self, battle: Battle) -> BattleOrder:
        """Choose a random move from available moves or switches"""
        if battle.available_moves:
            return self.create_order(random.choice(battle.available_moves))
        elif battle.available_switches:
            return self.create_order(random.choice(battle.available_switches))
        return self.create_order("struggle")

    def get_possible_moves(self, battle: Battle) -> List[Union[Pokemon, BattleOrder]]:
        """Get all possible moves and switches"""
        possible_moves = []
        if battle.available_moves:
            possible_moves.extend(battle.available_moves)
        if battle.available_switches:
            possible_moves.extend(battle.available_switches)
        return possible_moves

    def get_possible_opponent_moves(
        self, battle: Battle
    ) -> List[Union[Pokemon, BattleOrder]]:
        """Estimate opponent's possible moves"""
        return self.get_possible_moves(battle)


async def main():
    try:
        # Create players
        player1 = MinMaxAgent(battle_format="gen9randombattle", max_depth=2)
        player2 = RandomPlayer(battle_format="gen9randombattle")

        print("Starting battle...")
        print("Player 1: MinMax Agent")
        print("Player 2: Random Agent")

        # Run any number of battles
        await player1.battle_against(player2, n_battles=50)

        print("\nBattle Results:")
        print(f"MinMax Agent wins: {player1.n_won_battles}")
        print(f"Random Agent wins: {player2.n_won_battles}")

    except Exception as e:
        print(f"Error in main: {str(e)}")


if __name__ == "__main__":
    import asyncio

    asyncio.get_event_loop().run_until_complete(main())
