import os
import sys

print "This should print at the very least"

def generate_agency_list():
	transit_data=os.path.join('useful-docs/','GTFSTdata/')
	print transit_data

	for root, dirs, files in os.walk(transit_data):
	    for name in files:
	        path=os.path.join(root, name)
	        print path
	        if 'agency.txt' in path:
	        	print path
		        agency_data=open(path)
		        for line in agency_data:
		        	agency=agency_data.readline().split()
		        	print agency
		        #for line in agency:
				#	print line


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
