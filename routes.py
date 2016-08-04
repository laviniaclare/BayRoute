from flask import Flask, render_template, request, jsonify
import json

import model
from model import Agency, Route

app = Flask(__name__)

######  ROUTES  ######

@app.route('/', methods=['GET'])
def load_options():
    agencies_list = Agency.get_all_agencies()
    agency_names = Agency.get_agency_name_dict()
    agency_routes = model.agency_to_routes_dict()
    return render_template('map.html', agencies_list=agencies_list, agency_names=agency_names, agency_routes=agency_routes)


@app.route('/api/routes', methods=['GET'])
def prepare_routes_for_display():
    routes_to_display = json.dumps(request.values.getlist('routes'))
    output = {}
    output['routes'] = get_routes_by_id(routes_to_display)
    return jsonify(output)


#######   HELPER FUNCTION   #######

def get_routes_by_id(route_ids):
    """
    Takes in a string representing a list of route_ids and returns a list of
    dictionaries mapping each route to the lat/longs of each stop on that route
    """
    # print "\nroute_ids!! ", route_ids, "\n"
    routes_to_display = json.loads(route_ids)
    # Will be a list of dictionaries
    routes_trips_to_latlongs_dicts = []

    for route in routes_to_display:
        route_lat_longs = Route.get_all_stops_on_route(route)
        routes_trips_to_latlongs_dicts.append(route_lat_longs)
    # print routes_trips_to_latlongs_dicts
    return routes_trips_to_latlongs_dicts


if __name__ == '__main__':
    app.run(debug=True)
