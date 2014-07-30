from flask import Flask, render_template, redirect, request, Response, session, url_for, jsonify
from sqlalchemy.ext.declarative import DeclarativeMeta
import model
import json

app = Flask(__name__)
app.secret_key = '\xdd$j\x8dX\x19\xe69\x08"t/\'K\x1c\x1di"\'C\x8d*(\xd2'

####Routes and stuff go here (@app.route())####
@app.route('/', methods=['GET'])
def load_options():
	agencies_list=model.get_all_agencies()
	agency_names=model.get_agency_name_dict()
	agency_routes=model.agency_to_routes_dict()
	return render_template('options-page.html', agencies_list=agencies_list, agency_names=agency_names, agency_routes=agency_routes)


@app.route('/api/routes', methods=['GET'])
def prepare_routes_for_display():
	routes_to_display=json.dumps(request.values.getlist('routes'))
	output={}
	output['routes']=get_routes_by_id(routes_to_display)
	return jsonify(output)


@app.route('/', methods=['POST'])
def load_map():
	routes=request.form.getlist('routes')
	return redirect(url_for('.show_map', routes=json.dumps(routes)))

@app.route('/map')
def show_map():
	routes_to_display=request.args['routes']
	routes_trips_to_latlongs_dict=get_routes_by_id(routes_to_display)

	return render_template('map.html', routes_trips_to_latlongs_dict=json.dumps(routes_trips_to_latlongs_dict))

def get_routes_by_id(route_ids):
	routes_to_display=json.loads(route_ids)
	routes_trips_to_latlongs_dict=[]
	for route in routes_to_display:
		route_lat_longs=model.get_all_stops_on_route(route)
		routes_trips_to_latlongs_dict.append(route_lat_longs)

	return routes_trips_to_latlongs_dict


if __name__ == '__main__':
	app.run(debug=True)