import os
import re
import sys


def generate_agency_list():
    '''Generates dictionary containing data from GTFSTdata directory'''
    system_names = []
    system_dicts_list = []
    transit_data = os.path.join('useful-docs/', 'GTFSTdata/')

    for root, dirs, files in os.walk(transit_data):
        for name in files:
            path = os.path.join(root, name)
            if 'agency.txt' in path:
                agency_dict = {}
                agency_data = open(path)
                agency = agency_data.readlines()
                agency_name = agency[1].split(',')[1]

                system_names.append(agency_name)
                agency_dict['lines'] = [{}]
                agency_dict['id'] = agency_name
                system_dicts_list.append(agency_dict)

    return system_dicts_list


def get_agency_files_sqlite():
    '''Prints out command that creates tables in SQLite transit db
    and loads data from GTFSTdata directory'''

    transit_data = os.path.join('useful-docs/', 'GTFSTdata/')

    print "cat gtfs_SQL_importer/src/gtfs_tables.sqlite \\"
    for root, dirs, files in os.walk(transit_data):
        for name in dirs:
            path = os.path.join(root, name)
            m = re.search('GTFSTransitData_([A-Z0-9]{2})_.*', name)
            agency_name = m.group(1)
            agency_query = '<(python gtfs_SQL_importer/src/import_gtfs_to_sql.py %s nocopy %s) \\' % (path, agency_name)
            print agency_query

    print "| sqlite3 Test.db"


def get_agency_files_psql():
    '''Prints out command that creates tables in PostgreSQL transit db
     and loads data from GTFSTdata directory'''

    transit_data = os.path.join('useful-docs/', 'GTFSTdata/')

    print "cat gtfs_SQL_importer/src/gtfs_tables.sql \\"
    for root, dirs, files in os.walk(transit_data):
        for name in dirs:
            path = os.path.join(root, name)
            m = re.search('GTFSTransitData_([A-Z0-9]{2})_.*', name)
            agency_name = m.group(1)
            agency_query = '<(python gtfs_SQL_importer/src/import_gtfs_to_sql.py %s %s) \\' % (path, agency_name)
            print agency_query
    print "gtfs_SQL_importer/src/gtfs_tables_makeindexes.sql \\gtfs_SQL_importer/src/vacuumer.sql \\"
    print "| psql transit"


get_agency_files_psql()
