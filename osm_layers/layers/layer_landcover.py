import numpy
import json
from abc import ABCMeta, abstractmethod
import re

from .layers import *
from .functions import *

class layer_landcover(layers):
    def __init__(self):
        self.layer_type = 'landcover'
        self.data_source = ['osm']
        self.fields = ['class','subclass']
    def condition(self, feature):
        if feature['geometry']['type'] != 'Polygon':
            return False
        landuse_range = ['allotments','farm','farmland','orchard','plant_nursery','vineyard','grass','grassland',
                         'meadow','forest','village_green','recreation_ground','park']
        natural_range = ['wood','wetland','grassland','glacier','bare_rock','scree','beach','sand']
        wetland_range = ['bog','swamp','wet_meadow','marsh','reedbed','saltern','tidalflat','saltmarsh','mangrove']
        leisure_range = ['park','garden']
        if value_empty(feature,'landuse') in landuse_range:
            return True
        if value_empty(feature,'natural') in natural_range:
            return True
        if value_empty(feature,'wetland') in wetland_range:
            return True
        if value_empty(feature,'leisure') in leisure_range:
            return True
        return False
    def update_feature(self, feature):
        feature = feature.copy()
        feature["tippecanoe"] = {"layer" : "landcover" }
        landuse = value_empty(feature,'landuse')
        natural = value_empty(feature,'natural')
        leisure = value_empty(feature,'leisure')
        wetland = value_empty(feature,'wetland')
        cl = ''
        if landuse in ['farmland', 'farm', 'orchard', 'vineyard', 'plant_nursery']:
            cl = 'farmland'
        elif natural in ['glacier', 'ice_shelf']: 
            cl = 'ice'
        elif natural == 'wood' or landuse in ['forest']:
            cl = 'wood'
        elif natural in ['bare_rock', 'scree']:
            cl = 'rock'
        elif natural == 'grassland' or landuse in ['grass', 'meadow', 'allotments', 
                                                   'grassland','park', 'village_green', 'recreation_ground'] or leisure in ['park', 'garden']:
            cl = 'grass'
        elif natural == 'wetland' or wetland in ['bog', 'swamp', 'wet_meadow', 'marsh', 'reedbed', 'saltern', 
                       'tidalflat', 'saltmarsh', 'mangrove']:
            cl = 'wetland'
        elif natural in ['beach', 'sand']:
            cl = 'sand'
        else:
            cl = ''
        feature['properties']['class'] = cl
        subclass = ''
        if landuse != '':
            subclass = landuse
        elif natural != '':
            subclass = natural
        elif leisure != '':
            subclass = leisure
        else:
            subclass = wetland
        feature['properties']['subclass'] = subclass
        return feature
