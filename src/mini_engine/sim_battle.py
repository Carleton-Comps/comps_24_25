import poke_battle_sim as pb

class BattleSim:
    def __init__(self, battle: pb.Battle) -> None:
        self.battle = battle
        self.pokemon1 = {"name": "", "stats": [], "cur_hp": 0, "type": set()}
        self.pokemon2 = {"name": "", "stats": [], "cur_hp": 0, "type": set()}
        
    def get_battle_info(self):
        # Get both pokemon info
        # For each pokemon, get their stats, cur hp, and moves

        pass
    
    def damage_calculator(self, move, target):
        
    def simulate_turn(self, move1, move2):
        pass