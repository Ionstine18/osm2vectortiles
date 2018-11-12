import pandas as pd
import numpy
import json
from abc import ABCMeta, abstractmethod
import re

### import all layers
from .layers.layer_aerialway_linestring import *
from .layers.layer_aerodome import *
from .layers.layer_aeroway import *
from .layers.layer_boundary import *
from .layers.layer_building_polygon import *
from .layers.layer_highway_linestring import *
from .layers.layer_highway_polygon import *
from .layers.layer_housenumber import *
from .layers.layer_landcover import *
from .layers.layer_landuse import *
from .layers.layer_mountain_peak import *
from .layers.layer_park_polygon import *
from .layers.layer_parking_polygon import *
from .layers.layer_place import *
from .layers.layer_poi_point import *
from .layers.layer_poi_polygon import *
from .layers.layer_railway_linestring import *
from .layers.layer_shipway_linestring import *
from .layers.layer_water_polygon import *
from .layers.layer_waterway_linestring import *

### convert osm data in json form to different layers 
###### input: fullmap - geojson of osm data
###### output: dictionary of geojson of different layers
###

def osm2layers(fullmap):
    ### define all layers
    all_layers_class = [layer_aerialway_linestring,layer_aerodrome,layer_aeroway,layer_boundary,
    layer_building_polygon,layer_highway_linestring,layer_highway_polygon,
    layer_housenumber,layer_landcover,layer_landuse,layer_mountain_peak,
    layer_park_polygon,layer_place,layer_poi_point,layer_poi_polygon,
    layer_railway_linestring,layer_shipway_linestring,layer_water_polygon,
    layer_waterway_linestring, layer_parking_polygon]
    all_layers = []
    for item in all_layers_class:
        all_layers.append(item())

    feature_layers = [[] for itr in range(len(all_layers))]
    for feature in fullmap['features']:
        for itr in range(len(all_layers)):
            if all_layers[itr].condition(feature):
                feature_layers[itr].append(all_layers[itr].update_feature(feature))

    feature_sets = {}
    for item in feature_layers:
        if len(item) > 0:
            feature_sets[item[0]['tippecanoe']['layer']] = {'type':'FeatureColletion','features':item}

    return feature_sets
    