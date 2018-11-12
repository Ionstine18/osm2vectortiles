import numpy
import json
from abc import ABCMeta, abstractmethod
import re

from .layers import *
from .functions import *

class layer_water_polygon(layers):
    def __init__(self):
        self.layer_type = "water_polygon"
        self.data_source = ['osm']
        self.fields = ['class']
        
    def condition(self, feature):
        if feature['geometry']['type'] != 'Polygon':
            return False
        covered = value_empty(feature,'covered')
        landuse = value_empty(feature,'landuse')
        natural = value_empty(feature,'natural')
        waterway = value_empty(feature,'waterway')
        if covered in ['yes']:
            return False
        if landuse in ['reservoir']:
            return True
        if natural in ['water','bay']:
            return True
        if waterway in ['river','riverbank','stream','canal','drain','ditch']:
            return True
        return False
    
    def update_feature(self, feature):
        feature = feature.copy()
        feature["tippecanoe"] = {"layer" : "water_polygon" }
        feature['properties']['layer'] = value_empty(feature,'layer')
        feature['properties']['service'] = value_empty(feature,'service')
        feature['properties']['level'] = value_empty(feature,'level')
        feature['properties']['brunnel'] = brunnel(feature)
        feature['properties']['indoor'] = value_empty(feature,'indoor')
        highway = value_empty(feature,'highway')
        if highway_is_link(feature) or highway == 'steps':
            feature['properties']['ramp'] = 1
        elif is_ramp(feature):
            feature['properties']['ramp'] = 1
        else:
            feature['properties']['ramp'] = 0
        hc = highway_class(feature)
        feature['properties']['class'] = hc
        public_transport = value_empty(feature,'public_transport')
        highway = value_empty(feature, 'highway')
        scl = ""
        if (highway != "" or public_transport != "") and hc == "path":
            scl = public_transport if public_transport != "" else highway
        feature['properties']['subclass'] = scl
        oneway = value_empty(feature,'oneway')
        feature['properties']['is_oneway'] = 1 if oneway == 'yes' else 0
        return feature