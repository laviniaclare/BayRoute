import os
import sys
import re

def generate_agency_list():
	system_names=[]
	system_dicts_list=[]
	transit_data=os.path.join('useful-docs/','GTFSTdata/')

	for root, dirs, files in os.walk(transit_data):
	    for name in files:
	        path=os.path.join(root, name)
	        if 'agency.txt' in path:
	        	agency_dict={}
		        agency_data=open(path)
		        agency=agency_data.readlines()
		        agency_name=agency[1].split(',')[1]
		        
		        system_names.append(agency_name)
		        agency_dict['lines']=[{}]
		        agency_dict['id']=agency_name
		        system_dicts_list.append(agency_dict)



	return system_dicts_list


def get_agency_files():
	system_names=[]
	system_dicts_list=[]
	transit_data=os.path.join('useful-docs/','GTFSTdata/')

	print "cat gtfs_SQL_importer/src/gtfs_tables.sqlite \\"
	for root, dirs, files in os.walk(transit_data):
	    for name in dirs:
	    	path=os.path.join(root, name)
	        m = re.search('GTFSTransitData_([A-Z0-9]{2})_.*', name)
	        agency_name = m.group(1)
	        agency_query =  '<(python gtfs_SQL_importer/src/import_gtfs_to_sql.py %s nocopy %s) \\' % (path, agency_name)
	        print agency_query
        
	print "| sqlite3 Test.db"

Systems_shortname_to_longname={
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

		      
		       


	# for thing in transit_data:
	# 	print'trying to open the second bit'
	# 	agency_data=os.path.join(thing,'/agency.txt')
	# 	print agency_data
	# 	agency_data=open('agency.txt')
	# 	agency=agency.readlines()
	# 	print 'done'

	# 	for line in agency:
	# 			print row[1]



# def make_file():
	# transit_data=os.path.join('useful-docs/','DataExport_1132')
	# print transit_data
	# for thing in transit_data:
	# 	print'trying to open the second bit'
	# 	agency_data=os.path.join(thing,'/AGENCY.csv')
	# 	agency=open('AGENCY.CSV')
	# 	agency=agency.readlines()
	# 	print 'done'

	# 	for line in agency:
	# 			print row[1]

	# 	for page in system_dat:
	# 		print 'trying to get routes, etc.'
	# 		agency=open('AGENCY.CSV')
	# 		routes=open('ROUTE.CSV')
	# 		stops=open('STOP.CSV')
	# 		trips=open('TRIP.CSV')

	# 		agency=agency.readlines()
	# 		routes=routes.readlines()
	# 		stops=stops.readlines()
	# 		trips=trips.readlines()

	# 		print 'okay, guess that worked'

	# 		for line in agency:
	# 			print row[1]


