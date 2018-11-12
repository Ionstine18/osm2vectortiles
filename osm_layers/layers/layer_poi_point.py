import numpy
import json
from abc import ABCMeta, abstractmethod
import re

from .layers import *
from .functions import *

class layer_poi_point(layers):
    def __init__(self):
        self.layer_type = "poi_point"
        self.data_source = ['osm']
        self.fields = ['name','name_en','name_de','agg_stop','class','rank','subclass']
        
    def condition(self, feature):
        if feature['geometry']['type'] != 'Point':
            return False
        return poi_condition(feature)
        
    def update_feature(self, feature):
        feature = feature.copy()
        feature["tippecanoe"] = {"layer" : "poi_point" }
        feature['properties']['name'] = name_variable(feature)
        feature['properties']['name_en'] = name_en_variable(feature)
        feature['properties']['name_de'] = name_de_variable(feature)
        feature['properties']['agg_stop'] = '1'
        amenity = value_empty(feature,'amenity')
        leisure = value_empty(feature,'leisure')
        landuse = value_empty(feature,'landuse')
        railway = value_empty(feature,'railway') 
        station = value_empty(feature,'station')
        sport = value_empty(feature,'sport')
        tourism = value_empty(feature,'tourism')
        information = value_empty(feature,'information')
        religion = value_empty(feature, 'religion')
        shop = value_empty(feature, 'shop')
        scl = select_value([amenity,leisure,landuse,railway,station,sport,tourism,
                                                         information,religion,shop])
        feature['properties']['subclass'] = scl
        cl = poi_class(scl,feature)
        feature['properties']['class'] = cl
        feature['properties']['rank'] = poi_class_rank(cl)
        return feature
        