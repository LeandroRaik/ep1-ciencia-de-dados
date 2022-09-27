import json
from statistics import mean

from mrjob.job import MRJob
from mrjob.step import MRStep

#python map_reduce_average_damage.py file.json > log.txt

class AverageDamage(MRJob):
    def steps(self):
        return [MRStep(mapper=self.mapper, reducer=self.reducer)]

    def mapper(self, _, line):
        pokemon_detail = json.loads(line)
        pokemon_detail = pokemon_detail["dano_recebido"]
        all_damages = [
            (key, value)
            for key, value in pokemon_detail.items()
            
        ]
        for damage in all_damages:
            damage_name = damage[0]
            damage_value = damage[1]
            yield (damage_name, damage_value)

    def reducer(self, key, value):
        yield (key, mean(value))


if __name__ == "__main__":
    AverageDamage.run()