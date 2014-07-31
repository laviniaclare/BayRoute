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
	var l=$("input."+agency_id+":checkbox" );
	l.prop('checked', false);
	console.log('I unchecked some boxes!');
};

function checklines(agency_id){
	var l=$("input."+agency_id+":checkbox" );
	l.prop('checked', true);
	console.log('I checked some boxes!');
};

function togglelines(e){
	var target=$(e.target)
	var agency_id=$(this).val()
	console.log("Agency ID: "+ agency_id)

	var g=$('.'+agency_id+':checked');
	console.log("These are the agency boxes that are checked: "+g.length)


	if($('.'+agency_id+':checked').length == $('.'+agency_id).length){
		unchecklines(agency_id);
	} else {
		checklines(agency_id);
	}
};

function main() {


	var s=$('input[name=agency]');
	
		s.on('change', togglelines);

		$('.multiselect').multiselect({
			maxHeight:200,
			enableFiltering: true
		});

		$( "form" ).on( "submit", function( event ) {
			var form=$(this)
			var promise = $.ajax({
				url: form.attr('action'),
				method: form.attr('method'),
				data: form.serialize()
			})

			promise.done(function(response) {
				clearRoutes()
				displayRoutes(response.routes);
			})

			promise.fail(function(xhr, e) {
				console.log(arguments)
			})

		  event.preventDefault();

		  // console.log( $( this ).serialize() );
		});
};

$(main);