import poke_battle_sim as pb
import copy
import random
from poke_battle_sim.conf import global_settings as gs

articuno = pb.Pokemon(
    "Articuno",
    10,
    ["tackle", "tailwind"],
    "male",
    stats_actual=[100, 50, 50, 50, 50, 55],
)

pikachu = pb.Pokemon(
    "Pikachu",
    13,
    ["thunder-shock", "growl"],
    "male",
    stats_actual=[100, 50, 50, 50, 50, 50],
)

from poke_battle_sim.core.pokemon import Pokemon



class MinimaxTrainer(pb.Trainer):
    def __init__(self, name: str, poke_list: list[Pokemon], selection):
        super().__init__(name, poke_list, selection)
        self.name = name
        self.poke_id = 0
        self.selection = selection

    
    def simulate_turn(self, battle: pb.Battle, move1, move2):     
        new_battle = copy.deepcopy(battle)
        new_battle.turn(
            t1_turn=self.get_translated_move_name(move1),
            t2_turn=self.get_translated_move_name(move2),
        )

        return new_battle

    def evaluate_state(self, battle: pb.Battle) -> int:
        point_modifier: int = 0
        
        # Get current Pokemon for each trainer
        our_pokemon = battle.t1.current_poke
        opponent_pokemon = battle.t2.current_poke

        # Calculate HP fractions
        our_hp_fraction = our_pokemon.cur_hp / our_pokemon.max_hp
        opp_hp_fraction = opponent_pokemon.cur_hp / opponent_pokemon.max_hp

        # # HP State Scoring
        # if our_hp_fraction < 1.0:  # Any damage
        #     point_modifier -= 15
        # if our_hp_fraction < 0.5:  # Below half health
        #     point_modifier -= 25
        # if our_hp_fraction < 0.25:  # Critical health
        #     point_modifier -= 40

        # # Opponent HP Scoring
        # if opp_hp_fraction < 1.0:  # Any damage
        #     point_modifier += 10
        # if opp_hp_fraction < 0.5:  # Below half health
        #     point_modifier += 20
        # if opp_hp_fraction < 0.25:  # Critical health
        #     point_modifier += 35

        #new attempt at hp

        health_points = 50

        health_difference = our_hp_fraction - opp_hp_fraction

        point_modifier += health_difference * health_points

        #number of pokemon left alive


        # # Type Advantage Scoring
        # if our_pokemon and opponent_pokemon:
        #     for our_type in our_pokemon.types:
        #         if our_type:  
        #             for opp_type in opponent_pokemon.types:
        #                 if opp_type:
        #                     effectiveness = pb.PokeSim.get_type_ef(our_type, opp_type)
        #                     if effectiveness > 1:  # Super effective
        #                         point_modifier += 45
        #                     elif effectiveness < 1:  # Not very effective
        #                         point_modifier -= 30
        #                     elif effectiveness == 0:  # Immune
        #                         point_modifier -= 60

        # Status Condition Scoring
        if our_pokemon.nv_status:
            if our_pokemon.nv_status == gs.BURNED:
                point_modifier -= 20  # Significant penalty for burn
            elif our_pokemon.nv_status == gs.PARALYZED:
                point_modifier -= 40  # Major penalty for paralysis
            elif our_pokemon.nv_status == gs.POISONED:
                point_modifier -= 20  # Moderate penalty for poison
            elif our_pokemon.nv_status == gs.BADLY_POISONED:
                point_modifier -= 35  # Higher penalty for toxic
            elif our_pokemon.nv_status == gs.ASLEEP:
                point_modifier -= 45  # Major penalty for sleep

        # if opponent_pokemon.nv_status:
        #     if opponent_pokemon.nv_status == gs.BURNED:
        #         point_modifier += 25  # Reward for opponent's burn
        #     elif opponent_pokemon.nv_status == gs.PARALYZED:
        #         point_modifier += 35  # Good reward for opponent's paralysis
        #     elif opponent_pokemon.nv_status == gs.POISONED:
        #         point_modifier += 20  # Moderate reward for poison
        #     elif opponent_pokemon.nv_status == gs.BADLY_POISONED:
        #         point_modifier += 30  # Higher reward for toxic
        #     elif opponent_pokemon.nv_status == gs.ASLEEP:
        #         point_modifier += 40  # Major reward for sleep

        # # Enhanced Weather/Field Effects Scoring
        # if battle.battlefield:
        #     weather = battle.battlefield.weather
            
        #     if weather == gs.RAIN:
        #         # Water moves powered up, Fire moves weakened
        #         if 'water' in our_pokemon.types:
        #             point_modifier += 25  # Boosted water STAB
        #         if 'fire' in our_pokemon.types:
        #             point_modifier -= 20  # Weakened fire moves
        #         # Thunder always hits in rain
        #         if any(move.name.lower() == 'thunder' for move in our_pokemon.moves):
        #             point_modifier += 15
                    
        #     elif weather == gs.HARSH_SUNLIGHT:
        #         # Fire moves powered up, Water moves weakened
        #         if 'fire' in our_pokemon.types:
        #             point_modifier += 25  # Boosted fire STAB
        #         if 'water' in our_pokemon.types:
        #             point_modifier -= 20  # Weakened water moves
        #         # Solar Beam doesn't need charging
        #         if any(move.name.lower() == 'solar beam' for move in our_pokemon.moves):
        #             point_modifier += 15
                    
        #     elif weather == gs.SANDSTORM:
        #         # Rock, Ground, Steel types get SpDef boost
        #         if any(type_ in ['rock', 'ground', 'steel'] for type_ in our_pokemon.types):
        #             point_modifier += 20
        #         # Other types take damage
        #         elif not any(type_ in ['rock', 'ground', 'steel'] for type_ in our_pokemon.types):
        #             point_modifier -= 15
                    
        #     elif weather == gs.HAIL:
        #         # Ice types don't take damage, others do
        #         if 'ice' in our_pokemon.types:
        #             point_modifier += 20
        #         else:
        #             point_modifier -= 15
        #         # Blizzard always hits in hail
        #         if any(move.name.lower() == 'blizzard' for move in our_pokemon.moves):
        #             point_modifier += 15
                    
        #     elif weather == gs.FOG:
        #         # Reduces accuracy of all moves
        #         point_modifier -= 10  # General penalty for accuracy reduction
        #         # If we have moves that ignore accuracy, that's pretty worth
        #         if any(move.name.lower() in ['swift', 'aerial ace', 'magical leaf'] for move in our_pokemon.moves):
        #             point_modifier += 15

        #     # Check opponent's weather interaction
        #     if weather != gs.CLEAR:
        #         # Opponent type advantages in weather
        #         if weather == gs.RAIN and 'water' in opponent_pokemon.types:
        #             point_modifier -= 20
        #         elif weather == gs.HARSH_SUNLIGHT and 'fire' in opponent_pokemon.types:
        #             point_modifier -= 20
        #         elif weather == gs.SANDSTORM and any(type_ in ['rock', 'ground', 'steel'] for type_ in opponent_pokemon.types):
        #             point_modifier -= 15
        #         elif weather == gs.HAIL and 'ice' in opponent_pokemon.types:
        #             point_modifier -= 15

        # # Ability Scoring
        # if our_pokemon.ability:
        #     valuable_abilities = ['intimidate', 'levitate', 'speed-boost', 'drought', 'drizzle']
        #     if our_pokemon.ability in valuable_abilities:
        #         point_modifier += 25

        return point_modifier

    def get_opponent_stats(self, opponent):
        return opponent.copy()

    
    def get_translated_move_name(self, move):
        if type(move) == int:
            return ['other', 'switch']
        else:
            return ["move", move.name]

    # what is the point of this? it seems like we loop through this stuff anyways in minimax?
    def choose_move(self, battle: pb.Battle):
        new_battle = copy.deepcopy(battle)
        bestMove = None

        max_score = -float("Inf")

        # consider the switch
        #trainer selector function

        for move in self.current_poke.moves + [0,1]:


            """This might break things when the pokemon faints and has to choose what to switch to
            so maybe we could put it in a different place? discuss with team"""
            if type(move) == int:
                battle.t1.poke_id = move

            """we are only going to run the minimax call if:
            its a valid switch and move is an int
            its a normal move and we've checked if it's valid"""
            if type(move) == int and self.validSwitch(move, True):
                score = self.minimax(new_battle, move, 1, False)
            elif type(move) != int and battle.t1.can_use_move(self.get_translated_move_name(move)):
                score = self.minimax(new_battle, move, 1, False)
            else:
                continue
            
            
            """we occasionally get an error whre score doesn't get assigned a value
            I'm not sure how that's possible because we will pass if score doesn't get a value"""
        
            if score > max_score:
                max_score = score
                bestMove = move

        print(max_score)

        return self.get_translated_move_name(bestMove)
    
    def validSwitch(self, pokeID, isMaxPlayer):
        #check if player can switch out and check if its a valid pokemon to switch to
        if isMaxPlayer: #I think these flags maybe fix the issue of need two minimax trainers??
            if battle.t1.can_switch_out() and  battle.t1.poke_list[pokeID].cur_hp > 0:
                return True
            else:
                return False
        else:
            if battle.t2.can_switch_out() and battle.t2.poke_list[pokeID].cur_hp > 0:
                return True
            else:
                return False


    def minimax(
        self, battle: pb.Battle, move, depth, isMaxPlayer
    ):

        if depth == 0 or battle.is_finished():
            score = self.evaluate_state(battle)

            return score

        if isMaxPlayer:
            max_score = -float("Inf")

            for cur_move in self.current_poke.moves + [0,1]:


                if type(cur_move) == int:
                    self.poke_id = cur_move

                # if cur_move is an int(if we are switching, we need to check if it's valid othwesie we shouldn't consider it)
                # if it isn't valid switch we pass and don't even consider it.
                if type(cur_move) == int and self.validSwitch(cur_move, True):
                    score = self.minimax(battle, cur_move, 1, False)
                elif type(cur_move) != int and battle.t1.can_use_move(self.get_translated_move_name(cur_move)):
                    score = self.minimax(battle, cur_move, 1, False)
                else:
                    continue

                max_score = max(score, max_score)

            return max_score

        else:
            min_score = float("Inf")

            for opp_move in battle.t2.current_poke.moves + [0,1]:
                
                if type(opp_move) == int:
                    t2PokeID = opp_move

                #check if its a valid swap
                if type(opp_move) == int and self.validSwitch(opp_move, isMaxPlayer):
                    new_battle = self.simulate_turn(battle, move, opp_move)
                elif type(opp_move) != int and battle.t2.can_use_move(self.get_translated_move_name(opp_move)):
                    new_battle = self.simulate_turn(battle, move, opp_move)
                else:
                    continue

                score = self.minimax(new_battle, None, depth - 1, True)

                min_score = min(score, min_score)

            return min_score


t2PokeID = 0

#this is for minimaxTrainer or t1
def selection_function(battle):
    battle.t1.current_poke = battle.t1.poke_list[battle.t1.poke_id]

#this will be non minimax or t2
def selection_function2(battle):
    battle.t2.current_poke = battle.t2.poke_list[t2PokeID]



articuno = pb.Pokemon(
    "Articuno",
    50,
    ["tackle"],
    "male",
    stats_actual=[165, 105, 120, 115, 145, 105],
)

gengar = pb.Pokemon(
    "Gengar",
    10,
    ["shadow-ball", "hypnosis"],
    "male",
    stats_actual=[100, 50, 50, 50, 50, 55],
)

tyranitar = pb.Pokemon(
    "Tyranitar",
    50,
    ["earthquake", "crunch"],
    "male",
    stats_actual=[175, 154, 130, 115, 120, 81],
)

empoleon = pb.Pokemon(
    "Empoleon",
    10,
    ["surf", "ice-beam"],
    "male",
    stats_actual=[100, 50, 50, 50, 50, 55],
)

garchomp = pb.Pokemon(
    "Garchomp",
    10,
    ["dragon-claw", "earthquake"],
    "male",
    stats_actual=[100, 50, 50, 50, 50, 55],
)

blissey = pb.Pokemon(
    "Blissey",
    10,
    ["tackle"],
    "female",
    stats_actual=[100, 50, 50, 50, 50, 55],
)

pikachu = pb.Pokemon(
    "Pikachu",
    50,
    ["thunder-shock", "growl"],
    "male",
    stats_actual=[110, 75, 60, 70, 70, 110],
)

gyarados = pb.Pokemon(
    "Gyarados",
    50,
    ["waterfall", "dragon-dance"],
    "male",
    stats_actual=[170, 145, 99, 80, 120, 101],
)

milotic = pb.Pokemon(
    "Milotic",
    13,
    ["surf", "recover"],
    "female",
    stats_actual=[100, 50, 50, 50, 50, 50],
)

starmie = pb.Pokemon(
    "Starmie",
    13,
    ["psychic", "thunderbolt"],
    "genderless",
    stats_actual=[100, 50, 50, 50, 50, 50],
)

vaporeon = pb.Pokemon(
    "Vaporeon",
    13,
    ["surf", "ice-beam"],
    "male",
    stats_actual=[100, 50, 50, 50, 50, 50],
)

kingdra = pb.Pokemon(
    "Kingdra",
    13,
    ["surf", "dragon-pulse"],
    "male",
    stats_actual=[100, 50, 50, 50, 50, 50],
)

pikachu2 = pb.Pokemon(
    "Pikachu",
    50,
    ["thunder-shock", "growl"],
    "male",
    stats_actual=[110, 75, 60, 70, 70, 110],
)

gyarados2 = pb.Pokemon(
    "Gyarados",
    50,
    ["waterfall", "dragon-dance"],
    "male",
    stats_actual=[170, 145, 99, 80, 120, 101],
)


ash = MinimaxTrainer("Ash", [pikachu2, gyarados2], selection_function)
misty = pb.Trainer("Misty", [pikachu, gyarados], selection_function2)
battle = pb.Battle(ash, misty)

battle = pb.Battle(ash, misty)



def t2RandomTurn(battle):
    
    currentPokeMoves = battle.t2.current_poke.moves
    randomMove = random.choice(currentPokeMoves)

    while not battle.t2.can_use_move(["move", randomMove.name]):
        randomMove = random.choice(currentPokeMoves)

    return ["move", randomMove.name]



    # currentPokeMoves = battle.t2.current_poke.moves
    # randomMove = random.choice(currentPokeMoves)
    # return ["move", randomMove.name]


battle.start()

"""we still get an error where t2 tries to use a move not in their moveset
but it's pretty rare. I'm wondering if this happens when they have no valid
moves at all?? Also does this engine have struggle implemented?"""


while not battle.is_finished():

    battle.turn(t1_turn=ash.choose_move(battle), t2_turn=t2RandomTurn(battle))
    print("turn")
    print(battle.get_cur_text())


print(battle.get_cur_text())

#battleCopy = copy.deepcopy(battle)

#print(battle.t1)
#print(battleCopy.t1)


