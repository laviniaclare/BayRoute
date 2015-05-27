
var map = L.mapbox.map('map', 'laviniaclare.ina498lm');

function displayRoutes(routes){
	for (var i = 0; i < routes.length; i++) {
		var route_trips=routes[i];
		displayTrips(route_trips);

	}
}

function displayTrips(route_trips){
	lineColor='#'+Math.floor(Math.random()*16777215).toString(16);
	for (var key in route_trips) {
		if (route_trips.hasOwnProperty(key)){
			displayLines(route_trips[key], lineColor);

		}
	}

}

function displayLines(routes_lat_longs, lineColor){
	var polyline_options = {
		color: lineColor,
		opacity: 80
	};
	var polyline = L.polyline(routes_lat_longs, polyline_options).addTo(map);
}

function clearRoutes(){

}
