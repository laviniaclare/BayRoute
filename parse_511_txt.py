import os
import sys

def generate_agency_list():
	system_names=[]
	system_dict={}
	transit_data=os.path.join('useful-docs/','GTFSTdata/')

	for root, dirs, files in os.walk(transit_data):
	    for name in files:
	        path=os.path.join(root, name)
	        if 'agency.txt' in path:
		        agency_data=open(path)
		        agency=agency_data.readlines()
		        agency_name=agency[1].split(',')[1]
		        system_names.append(agency_name)

	for system in system_names:
		system_dict[system]={}

	print system_dict


		      
		       


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

generate_agency_list()
