var systems=[{
				id:'ACTransit',
				lines:[{
					id:1,
					name:'blah'
				}]
			}]

var systemCheckboxTemplate=_.template("<input type='checkbox' name='system' id='<%=id%>' value='<%=id%>'/><label for='<%=id%>'><%=id%></label>")

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