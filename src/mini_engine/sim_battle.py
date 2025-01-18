import poke_battle_sim as pb

class BattleSim:
    def __init__(self, battle: pb.Battle) -> None:
        self.battle = battle
        self.pokemon1 = {"name": "", "stats": [], "cur_hp": 0, "type": set(), "moves": []}
        self.pokemon2 = {"name": "", "stats": [], "cur_hp": 0, "type": set(), "moves": []}
        
    def get_battle_info(self):
        # Get both pokemon info
        # For each pokemon, get their stats, cur hp, and moves

        # Trainer 1's Pokémon (pokemon1)
        trainer1_pokemon = self.battle.t1.current_poke
        self.pokemon1["name"] = trainer1_pokemon.name
        self.pokemon1["stats"] = trainer1_pokemon.stats 
        self.pokemon1["cur_hp"] = trainer1_pokemon.cur_hp
        self.pokemon1["type"] = set(trainer1_pokemon.types) #set because Pokémon can have one or two types
        self.pokemon1["moves"] = [
            {"name": move.name, "power": move.power, "type": move.type, "pp": move.pp}
            for move in trainer1_pokemon.moves
        ]

        # Trainer 2's Pokémon (pokemon2)
        trainer2_pokemon = self.battle.t2.current_poke
        self.pokemon2["name"] = trainer2_pokemon.name
        self.pokemon2["stats"] = trainer2_pokemon.stats
        self.pokemon2["cur_hp"] = trainer2_pokemon.cur_hp
        self.pokemon2["type"] = set(trainer2_pokemon.types) #set because Pokémon can have one or two types
        self.pokemon2["moves"] = [
            {"name": move.name, "power": move.power, "type": move.type, "pp": move.pp}
            for move in trainer2_pokemon.moves
        ]
        pass
    
    def damage_calculator(self, move, target):
        
    def simulate_turn(self, move1, move2):
        pass