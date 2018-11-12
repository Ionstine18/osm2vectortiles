import pandas as pd
import numpy
import json
from abc import ABCMeta, abstractmethod
import re

def value_empty(feature, var):
    if var in feature['properties'].keys():
        return feature['properties'][var]
    else:
        return ""

def name_variable(feature):
    if 'name' in feature['properties'].keys():
        return feature['properties']['name']
    else:
        return ""

def name_en_variable(feature):
    if 'name:en' in feature['properties'].keys():
        return feature['properties']['name:en']
    else:
        return name_variable(feature)

def name_de_variable(feature):
    if 'name:de' in feature['properties'].keys():
        return feature['properties']['name:de']
    elif 'name' in feature['properties'].keys():
        return feature['properties']['name']
    else:
        return name_variable(feature)
    
def combined_keys(feature, var_list):
    con = False
    for var in var_list:
        if var in feature['properties'].keys():
            con = True
    return con
    
def normalize_capital_level(feature):
    tmp = value_empty(feature, 'capital')
    capital = ""
    if tmp in ['yes','2']:
        capital = '2'
    elif tmp in ['4']:
        capital = '4'
    return capital

def select_value(values):
    for item in values:
        if item != '':
            return item
    return ''

def poi_condition(feature):
    def_poi_mapping_aerialway = ['station']
    def_poi_mapping_amenity = ['arts_centre','bank','bar','bbq','bicycle_rental','biergarten','bus_station',
                               'cafe','cinema','clinic','college','community_centre','courthouse','dentist',
                               'doctors','embassy','fast_food','ferry_terminal','fire_station','food_court',
                               'fuel','grave_yard','hospital','ice_cream','kindergarten','library',
                               'marketplace','nightclub','nursing_home','pharmacy','place_of_worship',
                               'police','post_box','post_office','prison','pub','public_building','recycling',
                               'restaurant','school','shelter','swimming_pool','taxi','telephone','theatre',
                               'toilets','townhall','university','veterinary','waste_basket','fountain']
    def_poi_mapping_barrier = ['bollard','border_control','cycle_barrier','gate','lift_gate','sally_port',
                               'stile','toll_booth']
    def_poi_mapping_highway = ['bus_stop']
    def_poi_mapping_historic = ['monument','castle','ruins','memorial']
    def_poi_mapping_landuse = ['basin','brownfield','cemetery','reservoir']
    def_poi_mapping_leisure = ['dog_park','escape_game','garden','golf_course','ice_rink','hackerspace','marina',
                               'miniature_golf','park','pitch','playground','sports_centre','stadium',
                               'swimming_area','swimming_pool','water_park']
    def_poi_mapping_railway = ['halt','station','subway_entrance','train_station_entrance','tram_stop']
    def_poi_mapping_shop = ['accessories','alcohol','antiques','art','bag','bakery','beauty','bed',
                            'beverages','bicycle','books','boutique','butcher','camera','car','car_repair',
                            'carpet','charity','chemist','chocolate','clothes','coffee','computer',
                            'confectionery','convenience','copyshop','cosmetics','deli','delicatessen',
                            'department_store','doityourself','dry_cleaning','electronics','erotic','fabric',
                            'florist','frozen_food','furniture','garden_centre','general','gift','greengrocer',
                            'hairdresser','hardware','hearing_aids','hifi','ice_cream','interior_decoration',
                            'jewelry','kiosk','lamps','laundry','mall','massage','mobile_phone','motorcycle',
                            'music','musical_instrument','newsagent','optician','outdoor','perfume',
                            'perfumery','pet','photo','second_hand','shoes','sports','stationery','supermarket',
                            'tailor','tattoo','ticket','tobacco','toys','travel_agency','video','video_games',
                            'watches','weapons','wholesale','wine']
    def_poi_mapping_sport = ['american_football','archery','athletics','australian_football','badminton',
                             'baseball','basketball','beachvolleyball','billiards','bmx','boules','bowls',
                             'boxing','canadian_football','canoe','chess','climbing','climbing_adventure',
                             'cricket','cricket_nets','croquet','curling','cycling','disc_golf','diving',
                             'dog_racing','equestrian','fatsal','field_hockey','free_flying','gaelic_games',
                             'golf','gymnastics','handball','hockey','horse_racing','horseshoes','ice_hockey',
                             'ice_stock','judo','karting','korfball','long_jump','model_aerodrome','motocross',
                             'motor','multi','netball','orienteering','paddle_tennis','paintball','paragliding',
                             'pelota','racquet','rc_car','rowing','rugby','rugby_league','rugby_union',
                             'running','sailing','scuba_diving','shooting','shooting_range','skateboard',
                             'skating','skiing','soccer','surfing','swimming','table_soccer','table_tennis',
                             'team_handball','tennis','toboggan','volleyball','water_ski','yoga']
    def_poi_mapping_tourism = ['alpine_hut','aquarium','artwork','attraction','bed_and_breakfast','camp_site',
                               'caravan_site','chalet','gallery','guest_house','hostel','hotel','information',
                               'motel','museum','picnic_site','theme_park','viewpoint','zoo']
    def_poi_mapping_waterway = ['dock']
    full_condition = [{'var':'aerialway','values':def_poi_mapping_aerialway},
                     {'var':'amenity','values':def_poi_mapping_amenity},
                     {'var':'barrier','values':def_poi_mapping_barrier},
                     {'var':'highway','values':def_poi_mapping_highway},
                     {'var':'historic','values':def_poi_mapping_historic},
                     {'var':'landuse','values':def_poi_mapping_landuse},
                     {'var':'leisure','values':def_poi_mapping_leisure},
                     {'var':'railway','values':def_poi_mapping_railway},
                     {'var':'shop','values':def_poi_mapping_shop},
                     {'var':'sport','values':def_poi_mapping_sport},
                     {'var':'tourism','values':def_poi_mapping_tourism},
                     {'var':'waterway','values':def_poi_mapping_waterway}]
    for item in full_condition:
        tmp = value_empty(feature, item['var'])
        if tmp in item['values']:
            return True
    return False
    
        

def poi_class(scl, feature):
    railway = value_empty(feature, 'railway')
    cl = scl
    if scl in ['accessories','antiques','beauty','bed','boutique','camera','carpet','charity','chemist',
               'chocolate','coffee','computer','confectionery','convenience','copyshop','cosmetics',
               'garden_centre','doityourself','erotic','electronics','fabric','florist','frozen_food',
               'furniture','video_games','video','general','gift','hardware','hearing_aids','hifi',
               'ice_cream','interior_decoration','jewelry','kiosk','lamps','mall','massage','motorcycle',
               'mobile_phone','newsagent','optician','outdoor','perfumery','perfume','pet','photo',
               'second_hand','shoes','sports','stationery','tailor','tattoo','ticket','tobacco','toys',
               'travel_agency','watches','weapons','wholesale']:
        cl = 'shop'
    elif scl in ['townhall','public_building','courthouse','community_centre']:
        cl ='town_hall'
    elif scl in ['golf','golf_course','miniature_golf']:
        cl ='golf'
    elif scl in ['fast_food','food_court']:
        cl = 'fast_food'
    elif scl in ['park','bbq']:
        cl = 'park'
    elif scl in ['bus_stop','bus_station']:
        cl = 'bus'
    elif (scl =='station' and railway == 'station') or scl in ['halt', 'tram_stop', 'subway']:
        cl = 'railway'
    elif scl in ['subway_entrance','train_station_entrance']:
        cl = 'entrance'
    elif scl in ['camp_site','caravan_site']:
        cl = 'campsite'
    elif scl in ['laundry','dry_cleaning']:
        cl = 'laundry'
    elif scl in ['supermarket','deli','delicatessen','department_store','greengrocer','marketplace']:
        cl = 'grocery'
    elif scl in ['books','library']:
        cl = 'library'
    elif scl in ['university','college']:
        cl = 'college'
    elif scl in ['hotel','motel','bed_and_breakfast','guest_house','hostel','chalet','alpine_hut','camp_site']:
        cl = 'lodging'
    elif scl in ['chocolate','confectionery']:
        cl = 'ice_cream'
    elif scl in ['post_box','post_office']:
        cl = 'post'
    elif scl in ['cafe']:
        cl = 'cafe'
    elif scl in ['school','kindergarten']:
        cl = 'school'
    elif scl in ['alcohol','beverages','wine']:
        cl = 'alcohol_shop'
    elif scl in ['bar','nightclub']:
        cl = 'bar'
    elif scl in ['marina','dock']:
        cl = 'harbor'
    elif scl in ['car','car_repair','taxi']:
        cl = 'car'
    elif scl in ['hospital','nursing_home', 'clinic']:
        cl = 'hospital'
    elif scl in ['grave_yard','cemetery']:
        cl = 'cemetery'
    elif scl in ['attraction','viewpoint']:
        cl = 'attraction'
    elif scl in ['biergarten','pub']:
        cl = 'beer'
    elif scl in ['music','musical_instrument']:
        cl = 'music'
    elif scl in ['american_football','stadium','soccer','pitch']:
        cl = 'stadium'
    elif scl in ['art','artwork','gallery','arts_centre']:
        cl = 'art_gallery'
    elif scl in ['bag','clothes']:
        cl = 'clothing_store'
    elif scl in ['swimming_area','swimming']:
        cl = 'swimming'
    elif scl in ['castle','ruins']:
        cl = 'castle'
    return cl

def poi_class_rank(cl):
    rank = 1000
    if cl == 'hospital': 
        rank = 20
    elif cl == 'railway': 
        rank = 40
    elif cl ==  'bus': 
        rank = 50
    elif cl ==  'attraction': 
        rank = 70
    elif cl ==  'harbor': 
        rank = 75
    elif cl ==  'college': 
        rank = 80
    elif cl ==  'school': 
        rank = 85
    elif cl ==  'stadium': 
        rank = 90
    elif cl ==  'zoo': 
        rank = 95
    elif cl ==  'town_hall': 
        rank = 100
    elif cl ==  'campsite': 
        rank = 110
    elif cl ==  'cemetery': 
        rank = 115
    elif cl ==  'park': 
        rank = 120
    elif cl ==  'library': 
        rank = 130
    elif cl ==  'police': 
        rank = 135
    elif cl ==  'post': 
        rank = 140
    elif cl ==  'golf': 
        rank = 150
    elif cl ==  'shop': 
        rank = 400
    elif cl ==  'grocery': 
        rank = 500
    elif cl ==  'fast_food': 
        rank = 600
    elif cl ==  'clothing_store': 
        rank = 700
    elif cl ==  'bar': 
        rank = 800
    else:
        rank= 1000
    return rank

def brunnel(feature):
    bridge = value_empty(feature, 'bridge')
    tunnel = value_empty(feature, 'tunnel')
    ford = value_empty(feature,'ford')
    man_made = value_empty(feature,'man_made')
    if bridge not in ["",'No','NO'] or man_made == "bridge":
        return "bridge"
    elif tunnel not in ["",'No','NO']:
        return "tunnel"
    elif ford not in ["",'No','NO']:
        return "ford"
    else:
        return ""

def highway_class(feature):
    highway = value_empty(feature,'highway')
    public_transport = value_empty(feature,'public_transport')
    cl = ""
    if highway in ['motorway', 'motorway_link']:
        cl = 'motorway'
    elif highway in ['trunk', 'trunk_link']:
        cl = 'trunk'
    elif highway in ['primary', 'primary_link']:
        cl = 'primary'
    elif highway in ['secondary', 'secondary_link']:
        cl = 'secondary'
    elif highway in ['tertiary', 'tertiary_link']:
        cl = 'tertiary'     
    elif highway in ['unclassified', 'residential', 'living_street', 'road']:
        cl = 'minor'
    elif highway in ['service', 'track']:
        cl = highway
    elif highway in ['pedestrian', 'path', 'footway', 'cycleway', 'steps', 'bridleway', 'corridor'] or public_transport in ['platform']:
        cl = 'path'
    elif highway == 'raceway':
        cl = 'raceway'
    else:
        cl = ""
    return cl
            
def railway_class(feature):
    railway = value_empty(feature,'railway')
    cl =""
    if railway in ['rail', 'narrow_gauge', 'preserved', 'funicular']:
        cl = 'rail'
    elif railway in ['subway', 'light_rail', 'monorail', 'tram']:
        cl = 'transit'
    else:
        cl = ""
    return cl

def service_value(feature):
    service = value_empty(feature,'service')
    re = service if service in ['spur', 'yard', 'siding', 'crossover', 'driveway', 'alley', 'parking_aisle'] else "" 
    return re

def highway_is_link(feature):
    highway = value_empty(feature,'highway')
    if re.match("_link",highway) is not None:
        return True
    else:
        return False
    
def is_ramp(feature):
    ramp = value_empty(feature, 'ramp')
    if ramp not in ['','no','No','none']:
        return True
    return False
    
def water_class(feature):
    waterway = value_empty(feature,'waterway')
    lake = value_empty(feature,'lake')
    if waterway =='':
        return 'lake'
    else:
        return 'river'

