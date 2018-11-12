import pandas as pd
import numpy
import json
from abc import ABCMeta, abstractmethod
import re

from osm_layers.osm2layers import *
import imp

if __name__ == "__main__":
    with open("./raw/map.geojson") as f:
        tmp = " ".join(f.readlines())
    fullmap = json.loads(tmp)

    layers_full = osm2layers(fullmap)
    for layer in layers_full.keys():
        with open('./data_layers/'+layer+'.geojson','w') as f:
            json.dump(layers_full[layer],f,indent=2,ensure_ascii=False)

