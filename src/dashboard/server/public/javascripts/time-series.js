  //  year: new Date(+d.Year, 0, 1), // convert "Year" column to Date
  //  make: d.Make,
  //  model: d.Model,
  //  length: +d.Length // convert "Length" column to number
let mapName = 'timeseries';
let chart;
let ymin = 0;
let ymax = 2;
let chart_data;

let timeseriesfile = 'time_series_criminal_database.json'
let picker = d3.select(`#${mapName}-report-picker`)
picker.on('change', change_report)

fetch_json();

function change_report() {
	timeseriesfile = this.value;

	fetch_json();
}

function fetch_json() {
	d3.select(`#${mapName}-data-link`).attr('href', `/assets/data/${timeseriesfile}`)
	d3.select(`#${mapName}-shade`).attr('class', 'shade shade-on background-color-sea')
	d3.json(`/assets/data/${timeseriesfile}`).then(timeseries);
}

let from = ''
let to = ''
let selectedvalues = []

function reload_chart(data) {
	let fromdate = parseInt(from, 10);
	let todate = parseInt(to, 10);
	let daterangefilter = data.data.filter(x => (parseInt(x.year, 10) >= fromdate) && (parseInt(x.year, 10) <= todate))

	chart.load({
		json: daterangefilter,
		keys: { x: 'year', value: selectedvalues }
	})
}

function timeseries(data) {
	let rows = data.data.map(row => row.year);
	let frompicker = d3.select(`#${mapName}-select-date-from`);
	frompicker.selectAll('option').remove();
	frompicker
		.selectAll('option')
		.data(rows)
		.enter()
		.append('option')
		.text(x => x)
		.attr('value', x => x);
	from = rows[0];
	let fromdate = parseInt(from, 10);
	frompicker.value = from;
	document.getElementById(`${mapName}-select-date-from`).value = from;
	frompicker.on('change', function() { from = this.value; reload_chart(data); })

	let picker = d3.select(`#${mapName}-select-date-to`);
	picker.selectAll('option').remove();
	picker
		.selectAll('option')
		.data(rows)
		.enter()
		.append('option')
		.text(x => x)
		.attr('value', x => x);
	to = rows[rows.length - 1];
	let todate = parseInt(to, 10);
	let time_format = '%Y'
	let axis_type = 'category'

	picker.value = to;
	document.getElementById(`${mapName}-select-date-to`).value = to;
	picker.on('change', function() { to = this.value; reload_chart(data); })

	let daterangefilter = data.data.filter(x => (parseInt(x.year, 10) >= fromdate) && (parseInt(x.year, 10) <= todate))

	if (data.values.length > 20) {
		selectedvalues = data.values.slice(0, 10)
		chart = c3.generate({
			bindto: `#${mapName}-chart-area`,
			data: {
				json: daterangefilter,
				keys: {
					x: 'year',
					value: selectedvalues
				}
			},
			axis: {
				x: {
					type: axis_type,
					tick: {
						format: time_format
					}
				},
				y: {
					//min: ymin,
					//max: ymax
				}
			},
			zoom: {
			  enabled: false
			},
			legend: {
				show: true,
				padding: 5,
			  item: {
				onclick: legendclick
			  }
			},
			padding: {
              bottom: 60
            },
		});

		chart.load({ columns: data.values.map(x => [x]) });
		chart.hide();
		chart.load({json: daterangefilter,
							keys: {
								x: 'year',
								value: selectedvalues
								//value: data.values
							}})
		chart.show(selectedvalues, {withLegend: true});
	} else {
		//chart.load({json: data.data, keys: { x: 'date', value: data.values}});
		selectedvalues = data.values
		chart = c3.generate({
			bindto: `#${mapName}-chart-area`,
			data: {
				json: daterangefilter,
				keys: {
					x: 'year',
					value: selectedvalues
				}
			},
			axis: {
				x: {
					type: 'category',
					tick: {
						format: '%Y'
					}
				},
			},
			zoom: {
				enabled: false
			},
			legend: {
				padding: 5,
			},
			padding: {
              bottom: 30
            },
		});
	}
	d3.select(`#${mapName}-shade`).attr('class', 'shade shade-off background-color-sea')
	d3.select('#yminup').on('click', function() {
		ymin = ymin + 0.1;
		chart.axis.min(ymin);
	})
	d3.select('#ymindown').on('click', function() {
		ymin = ymin - 0.1;
		chart.axis.min(ymin);
		//chart.axis.min(chart.axis.min - 0.1);
	})
	d3.select('#ymaxup').on('click', function() {
		ymax = ymax + 0.1;
		chart.axis.max(ymax);
	})
	d3.select('#ymaxdown').on('click', function() {
		ymax = ymax - 0.1;
		chart.axis.max(ymax);
	})

	d3.select(window).on('resize', function() {
		chart.resize();
	});

	chart_data = data
}

function legendclick(id) {
	let fromdate = parseInt(from, 10);
	let todate = parseInt(to, 10);
	let daterangefilter = chart_data.data.filter(x => (parseInt(x.year, 10) >= fromdate) && (parseInt(x.year, 10) <= todate))
	if (selectedvalues.includes(id)) {
		let index = selectedvalues.indexOf(id);
		if (index > -1) {
			selectedvalues.splice(index, 1);
		}
		chart.unload({json: daterangefilter, keys: { x: 'year', value: [id]}});
		chart.hide(id);
	} else {
		selectedvalues.push(id);
		chart.load({json: daterangefilter, keys: { x: 'year', value: [id]}});
		chart.show(id);
	}
}
