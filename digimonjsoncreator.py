import json
import numpy as np

digimon = {
    1 : "Agumon",
    2 : "Gabumon",
    3 : "Tentomon",
    4 : "MetalGreymon"
    }
with open("digimon.json", "w") as write:
    json.dump(digimon, write)
