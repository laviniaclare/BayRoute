// var systems=[{'lines': [{}], id: 'TriDelta'}, 
// {'lines': [{}], id: 'AB'}, 
// {'lines': [{}], 'id': 'AC Transit'}, 
// {'lines': [{}], 'id': 'AM'}, 
// {'lines': [{}], 'id': 'AT'}, 
// {'lines': [{}], 'id': 'AY'}, 
// {'lines': [{}], 'id': 'BART'}, 
// {'lines': [{}], 'id': 'BG'}, 
// {'lines': [{}], 'id': 'CC'}, 
// {'lines': [{}], 'id': 'CE'}, 
// {'lines': [{}], 'id': 'Caltrain'}, 
// {'lines': [{}], 'id': 'Dumbarton Express'}, 
// {'lines': [{}], 'id': 'EM'}, 
// {'lines': [{}], id: 'FS'}, 
// {'lines': [{}], 'id': 'GF'}, 
// {'lines': [{}], 'id': 'Golden Gate Transit'}, 
// {'lines': [{}], 'id': 'HF'}, 
// {'lines': [{}], 'id': 'Marin Transit'}, 
// {'lines': [{}], 'id': 'MS'}, 
// {'lines': [{}], 'id': 'PE'}, 
// {'lines': [{}], 'id': 'RV'}, 
// {'lines': [{}], 'id': 'SB'}, 
// {'lines': [{}], 'id': 'VTA'}, 
// {'lines': [{}], 'id': 'SF-MUNI'}, 
// {'lines': [{}], 'id': 'SamTrans'}, 
// {'lines': [{}], 'id': 'SO'}, 
// {'lines': [{}], 'id': 'SR'}, 
// {'lines': [{}], 'id': 'ST'}, 
// {'lines': [{}], 'id': 'UC'}, 
// {'lines': [{}], 'id': 'VC'}, 
// {'lines': [{}], 'id': 'Vine (Napa County)'}, 
// {'lines': [{}], 'id': 'WestCAT'}, 
// {'lines': [{}], 'id': 'WH'}, 
// {'lines': [{}], 'id': 'YV'}]


// var systemCheckboxTemplate=_.template("<input type='checkbox' name='system' id='<%=id%>' value='<%=id%>'/><label for='<%=id%>'><%=id%></label>")

// function renderSystemCheckboxes(systems){
// 	return _.map(systems, systemCheckboxTemplate)
	
// }

function unchecklines(agency_id){
	l=$("input."+agency_id+":checkbox" );
	l.prop('checked', false);
	console.log('I unchecked some boxes!');
};

function checklines(agency_id){
	l=$("input."+agency_id+":checkbox" );
	// console.log(l)
	l.prop('checked', true);
	console.log('I checked some boxes!');
};

function togglelines(e){
	// console.log("The next thing you see is e")
	// console.log(e)
	var target=$(e.target)
	// console.log('clicked: ' + this + ' val: ' + $(this).val() );
	agency_id=$(this).val()
	console.log("Agency ID: "+ agency_id)

	// var g=$('.'+agency_id).filter( ":checkbox[checked=checked]" );
	var g=$('.'+agency_id+':checked');
	console.log("These are the agency boxes that are checked: "+g.length)


	if($('.'+agency_id+':checked').length == $('.'+agency_id).length){
		unchecklines(agency_id);
	} else {
		checklines(agency_id);
	}
};

function main() {

	// var systemsContainer = $('div#systems')

	// var systemCheckboxesHtml=renderSystemCheckboxes(systems).join('')

	// systemsContainer.append(systemCheckboxesHtml)

	var s=$('input[name=agency]');
	
		s.on('change', togglelines);
};

$(main);