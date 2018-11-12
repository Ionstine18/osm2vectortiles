import pandas as pd
import numpy
import json
from abc import ABCMeta, abstractmethod
import re

from .layers import *
from .functions import *

class layer_aeroway(layers):
    def __init__(self):
        self.layer_type = "aeroway"
        self.data_source = ['osm']
        self.fields = ['ref','class']
        
    def condition(self, feature):
        var_list = ['aeroway','area:aeroway']
        tmp = combined_keys(feature, var_list)
        tmp = tmp and (feature['geometry']['type'] == 'Polygon' or feature['geometry']['type'] == 'MultiPolygon')
        return tmp
    
    def update_feature(self, feature):
        feature = feature.copy()
        feature["tippecanoe"] = { "layer" : "aeroway" }
        ae = value_empty(feature, 'aeroway')
        if ae in ['runway', 'taxiway']:
            feature['properties']['ref'] = ae
        else:
            feature['properties']['ref'] = ''
        feature['properties']['class'] = ae
        if ae == '':
            ae_area = value_empty(feature, 'area:aeroway')
            feature['properties']['class'] = ae_area
        return feature