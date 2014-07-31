// Need to make this work wiht a list of lines that are fed to this page via the form selections
var map = L.mapbox.map('map', 'laviniaclare.ina498lm');

function displayRoutes(routes){
	for (var i =0; i < routes.length; i++) {
		var route_trips=routes[i]
		displayTrips(route_trips)

	}
}

function displayTrips(route_trips){
	for (var key in route_trips) {
		if (route_trips.hasOwnProperty(key)){
			displayLines(route_trips[key])

		}
	}

}

function displayLines(routes_lat_longs){	
	var polyline_options = {
  		color: '#F00'
	};
	var polyline = L.polyline(routes_lat_longs, polyline_options).addTo(map);
	
}

function clearRoutes(){
	
}

// var map = L.mapbox.map('map', 'laviniaclare.ina498lm');

// var line_points = [[37.8137326, -122.2398803], [37.8128786, -122.2410485], [37.8117096, -122.2422004], [37.8102088, -122.2459549], [37.8099102, -122.2487946], [37.8099102, -122.2487946], [37.8099102, -122.2487946], [37.8099102, -122.2487946], [37.8099102, -122.2487946], [37.8099102, -122.2487946], [37.8099102, -122.2487946], [37.8099102, -122.2487946], [37.8099102, -122.2487946], [37.8099102, -122.2487946], [37.8092622, -122.2475112], [37.8073255, -122.2497335], [37.8049677, -122.2507631], [37.8023712, -122.2542531], [37.8007308, -122.2545037], [37.798959, -122.2569687], [37.801271, -122.263183], [37.8022012, -122.2654866], [37.802933, -122.267375], [37.8038709, -122.2697415], [37.8047472, -122.2720121], [37.80552, -122.2739084], [37.8062221, -122.2758028], [37.8074637, -122.2789681], [37.8086002, -122.2813535], [37.808968, -122.282787], [37.8096257, -122.2859598], [37.810341, -122.2890567], [37.810698, -122.2905885], [37.8113955, -122.2937178], [37.8126786, -122.2964003], [37.8120275, -122.2989402], [37.8079104, -122.302168], [37.8063094, -122.2999058], [37.8059595, -122.2984696], [37.8050299, -122.2938296], [37.8041597, -122.2901818], [37.8042348, -122.2879637], [37.8065076, -122.2871498], [37.8093089, -122.2861275], [37.8109034, -122.2855524], [37.8120851, -122.2851177], [37.8153401, -122.2839486], [37.8170724, -122.2833222], [37.8186022, -122.2827703], [37.8201768, -122.2821915], [37.8219055, -122.281569], [37.8236388, -122.2809454], [37.8268626, -122.2797998], [37.8312559, -122.2793366], [37.8308023, -122.2815694], [37.8304827, -122.2831232], [37.8300574, -122.2851836], [37.8294947, -122.2879624], [37.8339879, -122.2932929], [37.8384365, -122.2931203], [37.8101431, -122.2455742], [37.8111074, -122.2427191], [37.811737, -122.2418657], [37.8126241, -122.2410156], [37.8139276, -122.2392558], [37.8148537, -122.2382078], [37.81571, -122.2371128], [37.8160062, -122.2350852], [37.815907, -122.2328363], [37.814525, -122.2321053], [37.8145943, -122.2328978], [37.8145579, -122.234959], [37.8150003, -122.2377917], [37.8099102, -122.2487946], [37.8099102, -122.2487946], [37.8099102, -122.2487946], [37.8099102, -122.2487946], [37.8099102, -122.2487946], [37.8099102, -122.2487946], [37.8431591, -122.2955043], [37.8412745, -122.2931214], [37.8333482, -122.2936413], [37.829439, -122.2872673], [37.8299006, -122.2848815], [37.8301886, -122.2834458], [37.830607, -122.2813223], [37.8311344, -122.2787876], [37.8270336, -122.2800661], [37.8235707, -122.2811857], [37.8221276, -122.2817167], [37.8200721, -122.2824598], [37.8188527, -122.2829057], [37.8173309, -122.2834659], [37.8157897, -122.2840182], [37.8125302, -122.2851892], [37.81123, -122.2856502], [37.8098322, -122.286166], [37.8064353, -122.2873877], [37.8040883, -122.2885118], [37.804536, -122.290796], [37.8046577, -122.2951104], [37.8061143, -122.297942], [37.8068258, -122.3011504], [37.8082239, -122.3017935], [37.811723, -122.2989927], [37.8124423, -122.2962944], [37.8109956, -122.2927139], [37.8105938, -122.2910108], [37.8100819, -122.2890561], [37.8093557, -122.2858639], [37.8087472, -122.2831026], [37.808164, -122.2811547], [37.8073203, -122.2792488], [37.8061951, -122.2761605], [37.8050901, -122.2733525], [37.804447, -122.271746], [37.8038323, -122.2701931], [37.8029564, -122.2679187], [37.8019849, -122.2654393], [37.801061, -122.2630844], [37.7990607, -122.2565121], [37.8000177, -122.2548018], [37.8027138, -122.2537118], [37.805025, -122.2505141], [37.8074189, -122.2494604], [37.8094057, -122.2468584], [37.810381, -122.2469298]];

// var polyline_options = {
//     color: '#F00'
// };

// var polyline = L.polyline(line_points, polyline_options).addTo(map);



// map.fitBounds(polyline.getBounds()); 