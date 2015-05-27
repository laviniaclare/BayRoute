
// var systemCheckboxTemplate=_.template("<input type='checkbox' name='system' id='<%=id%>' value='<%=id%>'/><label for='<%=id%>'><%=id%></label>")

// function renderSystemCheckboxes(systems){
// return _.map(systems, systemCheckboxTemplate)
	
// }

function unchecklines(agency_id){
	var l=$("input."+agency_id+":checkbox" );
	l.prop('checked', false);
	console.log('I unchecked some boxes!');
}

function checklines(agency_id){
	var l=$("input."+agency_id+":checkbox" );
	l.prop('checked', true);
	console.log('I checked some boxes!');
}

function togglelines(e){
	var target=$(e.target);
	var agency_id=$(this).val();
	console.log("Agency ID: "+ agency_id);

	var g=$('.'+agency_id+':checked');
	console.log("These are the agency boxes that are checked: "+g.length);


	if($('.'+agency_id+':checked').length == $('.'+agency_id).length){
		unchecklines(agency_id);
	} else {
		checklines(agency_id);
	}

}

//function uncheckAll(){
//		console.log('clicked uncheck');
//		var l=$('option');
//		l.prop('checked', false);
//		console.log('unchecked all!');
// }

function main() {

	// var uncheck=$('option[name=uncheck');
	// uncheck.on('click', uncheckAll);

	var s=$('input[name=agency]');
	
		s.on('change', togglelines);

		$('.multiselect').multiselect({
			maxHeight:400,
			enableCaseInsensitiveFiltering: true,
			filterPlaceholder: 'Type a route number or agency name'
		});

		$( "form" ).on( "submit", function( event ) {
			var form=$(this);
			var promise = $.ajax({
				url: form.attr('action'),
				method: form.attr('method'),
				data: form.serialize()
			});

			promise.done(function(response) {
				clearRoutes();
				displayRoutes(response.routes);
			});

			promise.fail(function(xhr, e) {
				console.log(arguments);
			});

			event.preventDefault();

		});
}

$(main);
