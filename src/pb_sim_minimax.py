import poke_battle_sim as pb
from poke_battle_sim.conf import global_settings as gs
import copy


class MinimaxState:
    def __init__(self, state: pb.Battle, opponent: pb.Trainer) -> None:
        self.battle = state
        self.opponent = opponent

    def copy(self):
        return copy.deepcopy(MinimaxState)


class MinimaxTrainer(pb.Trainer):
    def __init__(
        self, name: str, poke_list: list[pb.Pokemon], selection: callable = None
    ):
        super().__init__(name, poke_list, selection)

    def simulate_turn(self):
        pass

    def evaluate_state(self, battle: pb.Battle) -> int:
        point_modifier: int = 0
        
        # Get current Pokemon for each trainer
        our_pokemon = battle.t1.current_poke
        opponent_pokemon = battle.t2.current_poke

        # Calculate HP fractions
        our_hp_fraction = our_pokemon.cur_hp / our_pokemon.max_hp
        opp_hp_fraction = opponent_pokemon.cur_hp / opponent_pokemon.max_hp

        # HP State Scoring
        if our_hp_fraction < 1.0:  # Any damage
            point_modifier -= 15
        if our_hp_fraction < 0.5:  # Below half health
            point_modifier -= 25
        if our_hp_fraction < 0.25:  # Critical health
            point_modifier -= 40

        # Opponent HP Scoring
        if opp_hp_fraction < 1.0:  # Any damage
            point_modifier += 10
        if opp_hp_fraction < 0.5:  # Below half health
            point_modifier += 20
        if opp_hp_fraction < 0.25:  # Critical health
            point_modifier += 35

        # Type Advantage Scoring
        if our_pokemon and opponent_pokemon:
            for our_type in our_pokemon.types:
                if our_type:  
                    for opp_type in opponent_pokemon.types:
                        if opp_type:
                            effectiveness = pb.PokeSim.get_type_ef(our_type, opp_type)
                            if effectiveness > 1:  # Super effective
                                point_modifier += 45
                            elif effectiveness < 1:  # Not very effective
                                point_modifier -= 30
                            elif effectiveness == 0:  # Immune
                                point_modifier -= 60

        # Status Condition Scoring
        if our_pokemon.nv_status:
            if our_pokemon.nv_status == gs.BURNED:
                point_modifier -= 30  # Significant penalty for burn
            elif our_pokemon.nv_status == gs.PARALYZED:
                point_modifier -= 40  # Major penalty for paralysis
            elif our_pokemon.nv_status == gs.POISONED:
                point_modifier -= 25  # Moderate penalty for poison
            elif our_pokemon.nv_status == gs.BADLY_POISONED:
                point_modifier -= 35  # Higher penalty for toxic
            elif our_pokemon.nv_status == gs.ASLEEP:
                point_modifier -= 45  # Major penalty for sleep

        if opponent_pokemon.nv_status:
            if opponent_pokemon.nv_status == gs.BURNED:
                point_modifier += 25  # Reward for opponent's burn
            elif opponent_pokemon.nv_status == gs.PARALYZED:
                point_modifier += 35  # Good reward for opponent's paralysis
            elif opponent_pokemon.nv_status == gs.POISONED:
                point_modifier += 20  # Moderate reward for poison
            elif opponent_pokemon.nv_status == gs.BADLY_POISONED:
                point_modifier += 30  # Higher reward for toxic
            elif opponent_pokemon.nv_status == gs.ASLEEP:
                point_modifier += 40  # Major reward for sleep

        # Weather/Field Effects Scoring
        if battle.battlefield:
            if battle.battlefield.weather == gs.RAIN:
                if 'water' in our_pokemon.types:
                    point_modifier += 20
                if 'fire' in our_pokemon.types:
                    point_modifier -= 20
            elif battle.battlefield.weather == gs.HARSH_SUNLIGHT:
                if 'fire' in our_pokemon.types:
                    point_modifier += 20
                if 'water' in our_pokemon.types:
                    point_modifier -= 20

        # Ability Scoring
        if our_pokemon.ability:
            valuable_abilities = ['intimidate', 'levitate', 'speed-boost', 'drought', 'drizzle']
            if our_pokemon.ability in valuable_abilities:
                point_modifier += 25

        return point_modifier

    def get_opponent_stats(self, opponent):
        return opponent.copy()

    def get_translated_move_name(self, move):
        return ["move", move.name]

    def find_best_state(self, state: MinimaxState, opp_move, depth, isMaxPlayer) -> int:
        if state.battle.is_finished() or depth == 0:
            # Base case

            return self.evaluate_state(state.battle)

        if isMaxPlayer:
            best_score = -10000000000

            for max_cur_move in self.current_poke.moves:
                max_cur_score = self.find_best_state(
                    state, self.get_translated_move_name(max_cur_move), depth, False
                )

                best_score = max(best_score, max_cur_score)

            return best_score

        else:
            best_score = 10000000000
            opponent = state.opponent

            for min_cur_move in opponent.current_poke.moves:
                newState = copy.deepcopy(state)
                newState.battle.turn(
                    t1_turn=opp_move,
                    t2_turn=self.get_translated_move_name(min_cur_move),
                )

                cur_score = self.find_best_state(newState, None, depth - 1, True)

                best_score = min(cur_score, best_score)

            return best_score
