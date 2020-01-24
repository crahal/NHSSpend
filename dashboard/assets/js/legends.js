  // Plugin to add a simple map legend
function addLegend0(layer, data, options) {
	data = data || {};
	if ( !this.options.fills ) {
		return;
	}

	var contain = document.getElementById('map-legend');
	var html = '<dl>';
	var label = '';
	if ( data.legendTitle ) {
		html = '<h2>' + data.legendTitle + '</h2>' + html;
	}
	for ( var fillKey in this.options.fills ) {

		if ( fillKey === 'defaultFill') {
			if (! data.defaultFillName ) {
	 			continue;
	 		}
	 		label = data.defaultFillName;
		} else {
			if (data.labels && data.labels[fillKey]) {
				label = data.labels[fillKey];
			} else {
				label= fillKey + ': ';
			}
		}
		html += '<dt>' + label + '</dt>';
		//html += '<dd style="background-color:' +  this.options.fills[fillKey] + '">&nbsp;</dd>';
		html += '<div style="background: linear-gradient(' + colour_min_value + ', ' + colour_max_value + ')"></div>';

	}
	html += '</dl>';

	var hoverover = d3.select( '#map-legend' ).html(html);//.append('div')
		//.attr('class', 'datamaps-legend')
		//.html(html);
}

function addLegend2(layer, data, options) {
	data = data || {};
	if ( !this.options.fills ) {
		return;
	}

	var contain = document.getElementById('map-legend');
	var html = '';

	html += '<div style="background: linear-gradient(' + colour_min_value + ', ' + colour_max_value + ')"></div>';

	//var steps = d3.range(minValue, maxValue, (maxValue - minValue) * 0.1)
	var steps = d3.range(11).map(function(d) { return d3.format(".3f")((minValue + ((maxValue - minValue) * 0.1 * d))/100); });
	var paletteScale = d3.scale.linear()
       .domain([minValue, maxValue])
       .range([colour_min_value, colour_max_value]);
	d3.select( '#map-legend' ).selectAll('div').remove()
	rows = d3.select( '#map-legend' )
		//.append('div')
		.append('div').attr('class', 'container h-100 p-0').append('div').attr('class', 'row h-100 equal')
		//.attr('class', 'datamaps-legend')
		//.attr('class', 'w-100 h-100 p-3')
		//.html(html);
		.selectAll('div')
        .data(steps)
        .enter()
        .append('div').attr('class', 'col-12').append('div').attr('class', 'row h-100 equal');

	columns = d3.range(2)
     rows.selectAll('div')
             .data(function(row) {
                 return columns.map(function (column) {
                     return { column: column, value: row }
                 })
             })
     .enter()
     .append('div').attr('style', function(x) {
     	if (x.column ==0) {
     		return 'background: ' + paletteScale(x.value * 100)
     	}
     }).attr('class', function(x) {
        if (x.column ==0) {
     	return 'col-6 h-100 m-0'
     	}
     	else
     	{
     	return 'col-6 text-center my-auto font-weight-bold'
     	}
     })
     .text(function(x) {
     	if ((x.column==1) && (x.value!="NaN")) {
     	return x.value
     	}
     });
}

function addLegend3(layer, data, options) {
	data = data || {};
	if ( !this.options.fills ) {
		return;
	}

	var contain = document.getElementById('map-legend');
	var html = '';

	html += '<div style="background: linear-gradient(' + colour_min_value + ', ' + colour_max_value + ')"></div>';

	//var steps = d3.range(minValue, maxValue, (maxValue - minValue) * 0.1)
	var steps = d3.range(11).map(function(d) { return d3.format(".3f")((minValue + ((maxValue - minValue) * 0.1 * d))/100); });
	var paletteScale = d3.scale.linear()
       .domain([minValue, maxValue])
       .range([colour_min_value, colour_max_value]);
	d3.select( '#map-legend' ).selectAll('div').remove()
	d3.select( '#map-legend' )
		//.append('div')
		.append('div').attr('class', 'container h-100 p-0').append('div').attr('class', 'row h-100')
		//.attr('class', 'datamaps-legend')
		//.attr('class', 'w-100 h-100 p-3')
		//.html(html);
		.selectAll('div')
        .data(steps)
        .enter()
        .append('div').attr('style', function(row) { return 'background: ' + paletteScale(row * 100) }).attr('class', 'col-12 text-center my-auto font-weight-bold').text(function(row) { return row });
}

function addLegend4(layer, data, options) {
	data = data || {};
	if ( !this.options.fills ) {
		return;
	}

	var contain = document.getElementById('map-legend');
	var html = '';

	html += '<div style="background: linear-gradient(' + colour_min_value + ', ' + colour_max_value + ')"></div>';

	//var steps = d3.range(minValue, maxValue, (maxValue - minValue) * 0.1)
	var steps = d3.range(11).map(function(d) { return d3.format(".3f")((minValue + ((maxValue - minValue) * 0.1 * d))/100); });
	d3.select( '#map-legend' ).selectAll('div').remove()
	d3.select( '#map-legend' )
		//.append('div')
		.attr('style', 'background: linear-gradient(' + colour_min_value + ', ' + colour_max_value + ')').append('div').attr('class', 'container h-100 p-0').append('div').attr('class', 'row h-100')
		//.attr('class', 'datamaps-legend')
		//.attr('class', 'w-100 h-100 p-3')
		//.html(html);
		.selectAll('div')
        .data(steps)
        .enter()
        .append('div').attr('class', 'col-12 text-center my-auto font-weight-bold').text(function(row) { return row });
}
