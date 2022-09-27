# from functools import reduce
# from mrjob.job import MRJob
# from mrjob.step import MRStep
# import pandas as pd

# csvfile = pd.read_csv("file.csv")

# print(csvfile)

# #print(csvfile.iloc[1])

import json

from mrjob.job import MRJob
from mrjob.step import MRStep

class CountByType(MRJob):
    def steps(self):
        return [MRStep(mapper=self.mapper, reducer=self.reducer)]

    def mapper(self, _, line):
        pokemon_detail = json.loads(line)
        color = pokemon_detail["tipos"][0]
        yield (color, 1)

    def reducer(self, key, value):
        yield (key, sum(value))


if __name__ == "__main__":
    CountByType.run()
