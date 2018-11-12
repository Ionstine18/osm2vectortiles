import numpy
import json
from abc import ABCMeta, abstractmethod
import re

from .layers import *
from .functions import *

class layer_building_polygon(layers):
    def __init__(self):
        self.layer_type = "building_polygon"
        self.data_source = ['osm']
        self.fields = ['render_min_height','render_height']
    def condition(self, feature):
        flag = False
        if feature['geometry']['type'] not in ['Polygon','MultiPolygon']:
            return flag
        if "building" in feature['properties'].keys():
            flag = True
            bu = value_empty(feature,'building')
            if bu in ['no','No','none']:
                flag = False
                return flag
        if "buidling:part" in feature['properties'].keys():
            flag = True
            bu = value_empty(feature,'building:part')
            if bu in ['no','No','none']:
                flag = False
                return flag
        if "man_made" in feature['properties'].keys():
            mm = value_empty(feature, 'man_made')
            if mm == 'bridge':
                flag = False
                return flag
        return flag
    def update_feature(self, feature):
        feature = feature.copy()
        feature["tippecanoe"] = {"layer" : "building_polygon" }
        tmp = value_empty(feature,'height')
        height = tmp if tmp != "" else value_empty(feature,"building:height")
        tmp = value_empty(feature,'levels')
        levels = tmp if tmp != "" else value_empty(feature,"building:levels")
        feature['properties']['render_height'] = height 
        if height == "" and levels != "":
            feature['properties']['render_height'] = str(float(levels.replace("+",""))*3.66)
        tmp = value_empty(feature,'min_height')
        height = tmp if tmp != "" else value_empty(feature,"building:min_height")
        tmp = value_empty(feature,'min_level')
        levels = tmp if tmp != "" else value_empty(feature,"building:min_level")
        feature['properties']['render_min_height'] = height 
        if height == "" and levels != "":
            feature['properties']['render_min_height'] = str(float(levels)*3.66)
        return feature
        