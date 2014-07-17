// Need to make this work wiht a list of lines that are fed to this page via the form selections



var map = L.mapbox.map('map', 'laviniaclare.ina498lm')



var line_points = [
[37.949567,-121.77547],
[37.9659107811,-121.7803346251],
[37.9712226353,-121.7822448981],
[37.9732077121,-121.7840526324],
[37.9774933792,-121.7864122872],
[37.9808273092,-121.7842575048],
[37.9836490024,-121.7843723462],
[37.9869479704,-121.7857328967],
[37.9948513694,-121.7847741094],
[37.9977459665,-121.7862418365],
];


var polyline_options = {
    color: '#F00'
};

var polyline = L.polyline(line_points, polyline_options).addTo(map);

map.fitBounds(polyline.getBounds()); 