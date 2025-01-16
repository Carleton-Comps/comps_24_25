import poke_battle_sim as pb

class BattleSim:
    def __init__(self, battle: pb.Battle) -> None:
        self.battle = battle
        self.pokemon_1 = {"name": "", "stats": [], "cur_hp": 0, "type": set(), "fainted": False}
        self.pokemon_2 = {"name": "", "stats": [], "cur_hp": 0, "type": set(), "fainted": False}

    def get_battle_info(self):
        # Get both pokemon info
        # For each pokemon, get their stats, cur hp, and moves

<<<<<<< HEAD

        poke_info = {}
        
        # Trainer 1 (Player)
        pokemon_1 = self.battle.t1.current_poke
        poke_info["pokemon_1"] = {
            "name": self.battle.t1.name,
            "pokemon": {
                "name": pokemon_1.name,
                "cur_hp": pokemon_1.cur_hp,
                "max_hp": pokemon_1.max_hp,
                "stats": pokemon_1.stats_base,
                "types": pokemon_1.types,
            },
        }

=======
>>>>>>> 09aee07dc27581d2770fa93d26f6bfb7eed16b32
        pass
    
    def damage_
    def simulate_turn(self, move1, move2):
        pass
