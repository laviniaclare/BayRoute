import model
import csv
import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

# import sqlalchemy.dialects.postgresql.json as json


Systems_short_to_long={
'3D':'Tridelta Transit',
'AB':'AirBART',
'AC':'AC Transit',
'AM':'Capitol Corridor',
'AT':'Angel Island Ferry',
'AY':'American Canyon Transit (Vine Transit)',
'BA':'BART',
'BG':'Blue and Gold Fleet',
'CC':'County Connection',
'CE':'Ace Rail',
'CT':'CalTrain',
'DE':'Dumbarton Express',
'EM':'Emerygoround',
'FS':'FAST Transit',
'GF':'Golden Gate Ferry',
'GG':'Golden Gate Transit',
'HF':'Alcatraz Cruises',
'MA':'Marin Transit',
'MS':'Marguerite Shuttle (Stanford)',
'PE':'Petaluma Transit',
'RV':'Delta Breeze Transit (Rio Vista City)',
'SB':'San Francisco Bay Ferry',
'SC':'Vally Transportation Authority',
'SF':'SFMTA (Muni)',
'SM':'SamTrans',
'SO':'Sonoma County Transit',
'SR':'CityBus (Santa Rosa)',
'ST':'Soltrans',
'UC':'Union City Transit',
'VC':'City Coach',
'VN':'The Vine',
'WC':'WestCat',
'WH':'Wheels Bus',
'YV':'Yountville Trolley (Vine Transit)'
}

# def fix_lingnames():
# 	names=model.session.query(model.Agency).all()
# 	for route_name in gtfs_agency:
# 		if name in Systems_shortname_to_longname:
# 			name=Systems_shortname_to_longname[name]



# def make_tree():
# 	tree=[]
# 	agencies=model.get_all_agencies()
# 	for agency in agencies:
# 		agency_dict={}
# 		agency_dict['agency_id']=agency.agency_id
# 		agency_dict['routes']=[]
# 		routes=model.get_agency_routes(agency.agency_id)
# 		for route in routes:
# 			route_dict={}
# 			route_dict['route_id']=route.route_id
# 			route_dict['route_name']=route.route_long_name
# 			route_dict['route_type']=route.route_type
# 			agency_dict['routes'].append(route_dict)
# 		tree.append(agency_dict)
# 	print tree


def make_tree():
	tree={}
	agencies=model.get_all_agencies()
	for agency in agencies:
		agency_id=agency.agency_id
		tree[agency_id]={}
		routes=model.get_agency_routes(agency_id)
		route_dict=tree[agency_id]
		for route in routes:
			route_id=route.route_id
			route_dict[route_id]={}
			route_info=route_dict[route_id]
			route_info['name']=route.route_long_name
			route_info['type']=route.route_type
			route_info['id']=route.route_id
			route_info['route_trips']={}
			trips=model.get_route_trips(route.route_id)
			trip_dict=route_info['route_trips']
			for trip in trips:
				trip_id=trip.trip_id
				trip_dict[trip_id]={}
				trip_info=trip_dict[trip_id]

				trip_info['route_id']=route_id
				trip_info['service_id']=trip.service_id
				trip_info['trip_headsign']=trip.trip_headsign
				# stops=model.get_trip_stops(trip_id)
			# 	for stop in stops:
			# 		stops_dict['sequence']=stop.stop_sequence
			# 		stops_dict['stop_id']=stop.stop_id

			# 		stop=model.get_stop_by_id(stop.stop_id)
			# 		stops_dict['stop_name']=stop.stop_name
			# 		lat_long=model.get_stop_lat_long(stop.stop_id)
			# 		stops_dict['lat_long']=lat_long
	print tree


#make_tree()

def agency_routes_dict():
	output={}
	agencies=model.get_all_agencies()
	for agency in agencies:
		agency_id=agency.agency_id
		output[agency_id]={}
		routes=model.get_agency_routes(agency_id)
		route_dict=output[agency_id]
		for route in routes:
			route_id=route.route_id
			route_dict[route_id]={}
			route_info=route_dict[route_id]
			route_info['name']=route.route_long_name
			route_info['id']=route.route_id
	print output

agency_routes_dict()