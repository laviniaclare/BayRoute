from flask import Flask, render_template, request, jsonify
import model
import json

app = Flask(__name__)
app.secret_key = '\xdd$j\x8dX\x19\xe69\x08"t/\'K\x1c\x1di"\'C\x8d*(\xd2'


@app.route('/', methods=['GET'])
def load_options():
	agencies_list=model.get_all_agencies()
	agency_names=model.get_agency_name_dict()
	agency_routes=model.agency_to_routes_dict()
	return render_template('map.html', agencies_list=agencies_list, agency_names=agency_names, agency_routes=agency_routes)


@app.route('/api/routes', methods=['GET'])
def prepare_routes_for_display():
	routes_to_display=json.dumps(request.values.getlist('routes'))
	output={}
	output['routes']=get_routes_by_id(routes_to_display)
	return jsonify(output)



def get_routes_by_id(route_ids):
	routes_to_display=json.loads(route_ids)
	routes_trips_to_latlongs_dict=[]
	for route in routes_to_display:
		route_lat_longs=model.get_all_stops_on_route(route)
		routes_trips_to_latlongs_dict.append(route_lat_longs)

	return routes_trips_to_latlongs_dict


if __name__ == '__main__':
	app.run(debug=True)