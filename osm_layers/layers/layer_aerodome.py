import pandas as pd
import numpy
import json
from abc import ABCMeta, abstractmethod
import re

from .layers import *
from .functions import *

class layer_aerodrome(layers):
    def __init__(self):
        self.layer_type = "aerodrome_label"
        self.data_source = ['osm']
        self.fields = ['name','name:en','name:de','name:zh','iata','icao','ele','class']
    
    def condition(self, feature):
        var_list = ['aerodrome','aerodrome:type']
        return combined_keys(feature, var_list)
    
    def update_feature(self, feature):
        feature = feature.copy()
        feature["tippecanoe"] = { "layer" : "aerodrome_label" }
        feature['properties']['name'] = name_variable(feature)
        feature['properties']['name:en'] = name_en_variable(feature)
        feature['properties']['name:de'] = name_de_variable(feature)
        feature['properties']['icao'] = value_empty(feature,'icao')
        feature['properties']['iata'] = value_empty(feature,'iata')
        feature['properties']['ele'] = value_empty(feature,'ele')
        ae = value_empty(feature,'aerodrome')
        ae_type = value_empty(feature,'aerodrome:type')
        if ae == 'international'or ae_type == 'international':
            feature['properties']['class'] = 'international'
        elif ae == 'public' or re.search('public',ae_type) is not None or ae_type == 'civil':
            feature['properties']['calss'] = 'public'
        elif ae == 'regional' or ae_type == 'regional':
            feature['properties']['class'] = 'regional'
        elif ae == 'military' or re.search('military',ae_type) is not None or value_empty(feature,'military') == 'airfield':
            feature['properties']['class'] = 'military'
        elif ae == 'private' or ae_type == 'private':
            feature['properties']['class'] = 'private'
        else:
            feature['properties']['class'] = 'other'
        return feature
    