import poke_battle_sim as pb
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
        return 5

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
