from flask import Flask, render_template, redirect, request
import model

app = Flask(__name__)
app.secret_key = '\xdd$j\x8dX\x19\xe69\x08"t/\'K\x1c\x1di"\'C\x8d*(\xd2'

####Routes and stuff go here (@app.route())####
@app.route('/', methods=['GET'])
def load_options():
	agencies_list=model.get_all_agencies()
	agency_names=model.get_agency_name_dict()
	agency_routes=model.agency_to_routes_dict()
	return render_template('options-page.html', agencies_list=agencies_list, agency_names=agency_names, agency_routes=agency_routes)


@app.route('/', methods=['POST'])
def load_map():
	agencies=request.form.getlist('agency')
	routes=request.form.getlist('route')
	time=request.form.getlist('time')
	print time
	print agencies
	print routes
	return redirect('/map')

@app.route('/map')
def show_map():
	return render_template('map.html')



if __name__ == '__main__':
	app.run(debug=True)