import json
from pprint import pprint


class PokemonData:
    def __init__(self) -> None:
        self.data = self._load_data()

    def _load_data(self):
        """
        Loads the JSON file as a Python object that the other methods in this class can interact with.
        Should not be called outside this module
        """
        file = "data/gen9ou-0.json"

        with open(file, "r") as j:
            data = json.loads(j.read())

        return data["data"]

    def get_all_pokemon(self) -> list:
        """
        Returns a list of all legal Pokemon in the format
        """
        return list(self.data.keys())

    def get_pokemon_info(self, pokemon: str) -> dict:
        """
        Returns all the aggregated battle information of the requested Pokemon
        """
        return self.data[pokemon]

    def get_matchup_info(self, pokemon: str, opponent: str) -> list:
        """
        Returns a list encoding common opponent Pokemon that force switches/KOs vs the current Pokemon
        list[1]
        """
        poke_data = self.get_pokemon_info(pokemon)

        return poke_data["Checks and Counters"][opponent]

    def get_most_common_build(self, pokemon: str):
        poke_data = self.get_pokemon_info(pokemon)

        poke_builds = poke_data["Spreads"]

        most_common_build = max(poke_builds, key=poke_builds.get)

        return most_common_build

    def get_most_common_tera(self, pokemon: str):
        poke_data = self.get_pokemon_info(pokemon)

        poke_tera = poke_data["Tera Types"]

        most_common_tera = max(poke_tera, key=poke_tera.get)

        return most_common_tera


if __name__ == "__main__":
    d = PokemonData()
    pokemon = "Iron Valiant"

    pprint(d.get_matchup_info("Kingambit", "Iron Hands"))
