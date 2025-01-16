import poke_battle_sim as pb

class BattleSim:
    def __init__(self, battle: pb.Battle) -> None:
        self.battle = battle
        
    def get_battle_info(self):
        # Get both pokemon info
        # For each pokemon, get their stats, cur hp, and moves


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

        pass
    
    def simulate_turn(self, move1, move2):
        pass