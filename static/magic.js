var systems=[{'lines': [{}], id: 'TriDelta'}, 
{'lines': [{}], id: 'AB'}, 
{'lines': [{}], 'id': 'AC Transit'}, 
{'lines': [{}], 'id': 'AM'}, 
{'lines': [{}], 'id': 'AT'}, 
{'lines': [{}], 'id': 'AY'}, 
{'lines': [{}], 'id': 'BART'}, 
{'lines': [{}], 'id': 'BG'}, 
{'lines': [{}], 'id': 'CC'}, 
{'lines': [{}], 'id': 'CE'}, 
{'lines': [{}], 'id': 'Caltrain'}, 
{'lines': [{}], 'id': 'Dumbarton Express'}, 
{'lines': [{}], 'id': 'EM'}, 
{'lines': [{}], id: 'FS'}, 
{'lines': [{}], 'id': 'GF'}, 
{'lines': [{}], 'id': 'Golden Gate Transit'}, 
{'lines': [{}], 'id': 'HF'}, 
{'lines': [{}], 'id': 'Marin Transit'}, 
{'lines': [{}], 'id': 'MS'}, 
{'lines': [{}], 'id': 'PE'}, 
{'lines': [{}], 'id': 'RV'}, 
{'lines': [{}], 'id': 'SB'}, 
{'lines': [{}], 'id': 'VTA'}, 
{'lines': [{}], 'id': 'SF-MUNI'}, 
{'lines': [{}], 'id': 'SamTrans'}, 
{'lines': [{}], 'id': 'SO'}, 
{'lines': [{}], 'id': 'SR'}, 
{'lines': [{}], 'id': 'ST'}, 
{'lines': [{}], 'id': 'UC'}, 
{'lines': [{}], 'id': 'VC'}, 
{'lines': [{}], 'id': 'Vine (Napa County)'}, 
{'lines': [{}], 'id': 'WestCAT'}, 
{'lines': [{}], 'id': 'WH'}, 
{'lines': [{}], 'id': 'YV'}]



var systemSortNametoLongNameDict={
'3D':'Tridelta Transit'
'AB':'BART'
'AC':'AC Transit'
AM|http://www.capitolcorridor.org
AT|http://www.angelislandferry.com
AY|http://www.ridethevine.com/american-canyon-transit
BA|http://www.bart.gov
BG|http://www.blueandgoldfleet.com/
CC|http://www.cccta.org/
CE|http://www.acerail.com/
CT|http://www.caltrain.com/
DE|http://www.dumbartonexpress.com
EM|http://www.emerygoround.com
FS|http://www.fasttransit.org
GF|http://www.goldengateferry.org
GG|http://www.goldengatetransit.org
HF|http://www.alcatrazcruises.com/index.aspx
MA|http://www.marintransit.org/
MS|http://transportation.stanford.edu/marguerite/
PE|http://cityofpetaluma.net/pubworks/transit-sub.html
RV|http://www.riovistacity.com/transit/
SB|http://www.sanfranciscobayferry.com
SC|http://www.vta.org
SF|http://www.sfmta.com/
SM|http://www.samtrans.com
SO|http://www.sctransit.com
SR|http://ci.santa-rosa.ca.us/departments/transit/CityBus/Pages/default.aspx
ST|http://www.soltransride.com
UC|http://www.ci.union-city.ca.us/transit.html
VC|http://www.citycoach.com/index.cfm?page=cat&caid=16&cid=159
VN|http://www.ridethevine.com/vine
WC|http://www.westcat.org
WH|http://www.wheelsbus.com
YV|http://www.ridethevine.com/yountville-trolley

}




// [{
// 	id:'ACTransit',
// 	lines:[{
// 		id:1,
// 		name:'blah'
// 	}]
// }]

var systemCheckboxTemplate=_.template("<input type='checkbox' name='system' id='<%=id%>' value='<%=id%>'/>
										<label for='<%=id%>'><%=id%></label>")

function renderSystemCheckboxes(systems){
	return _.map(systems, systemCheckboxTemplate)
	
}

function unchecklines(){
	l=$( "input[class='ACT']" );
	l.prop('checked', false);
	console.log('I unchecked some boxes!');
}

function checklines(){
	l=$( "input[class='ACT']" );
	l.prop('checked', true);
	console.log('I checked some boxes!');
};

function togglelines(e){
	console.log(e)
	var $target=$(e.target)
	var g=$( ".ACT" ).filter( ":checkbox[checked=checked]" );
	if($('.ACT:checked').length == $('.ACT').length){
		unchecklines();
	} else {
		checklines();
	}
};

function main() {

	var systemsContainer = $('div#systems')

	var systemCheckboxesHtml=renderSystemCheckboxes(systems).join('')

	systemsContainer.append(systemCheckboxesHtml)

	var s=$('input[name=system]');
	
		s.on('change', togglelines);
};

$(main);