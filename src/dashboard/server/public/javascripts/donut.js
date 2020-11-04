  //  year: new Date(+d.Year, 0, 1), // convert "Year" column to Date
  //  make: d.Make,
  //  model: d.Model,
  //  length: +d.Length // convert "Length" column to number
let mapName = 'donut';
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
let selectedcat = ''

function reload_chart(data) {
	let fromdate = parseInt(from, 10);
	let todate = parseInt(to, 10);
	let daterangefilter = data.data.filter(x => (parseInt(x.year, 10) >= fromdate) && (parseInt(x.year, 10) <= todate))

	let emptycols = data.values.reduce((accumulator, col) => {accumulator[col] = 0; return accumulator}, {})
	let categorycounts = daterangefilter.reduce((accumulator, currentValue) => {
		for (key in currentValue) {
			if (!isNaN(parseInt(currentValue[key], 10))) {
				accumulator[key] = accumulator[key] + parseInt(currentValue[key], 10)
			}
		};
		return accumulator
	}, emptycols);
	delete categorycounts.year
	let categorys = Object.keys(data.cols[Object.keys(data.cols)[0]])

	let filtercounts = categorys.reduce((accumulator, col) => {accumulator[col] = {}; return accumulator}, {})
	for (col in categorycounts) {
		for (key in data.cols[col]) {
			if (filtercounts[key][data.cols[col][key]]) {
				filtercounts[key][data.cols[col][key]] = filtercounts[key][data.cols[col][key]] + categorycounts[col]
			} else {
				filtercounts[key][data.cols[col][key]] = categorycounts[col]
			}
		}
	}

	let selecteddata = [(selectedcat) ? filtercounts[selectedcat] : categorycounts]
	selectedvalues = Object.keys(selecteddata[0])

	chart.load({
		unload: true,
		json: selecteddata,
		keys: {
			//x: 'year',
			value: selectedvalues
		}
	})
}

function pie(data) {

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

	//chart.load({json: data.data, keys: { x: 'date', value: data.values}});
	let emptycols = data.values.reduce((accumulator, col) => {accumulator[col] = 0; return accumulator}, {})
	let categorycounts = daterangefilter.reduce((accumulator, currentValue) => {
		for (key in currentValue) {
			if (!isNaN(parseInt(currentValue[key], 10))) {
				accumulator[key] = accumulator[key] + parseInt(currentValue[key], 10)
			}
		};
		return accumulator
	}, emptycols);
	delete categorycounts.year
	let categorys = (data.cols) ? Object.keys(data.cols[Object.keys(data.cols)[0]]) : []
	categorys.unshift("")

	let catpicker = d3.select(`#${mapName}-select-category`);
    catpicker.selectAll('option').remove();
    catpicker
    	.selectAll('option')
    	.data(categorys)
    	.enter()
    	.append('option')
    	.text(x => x)
    	.attr('value', x => x);
    catpicker.on('change', function() { selectedcat = this.value; reload_chart(data); })

	let filtercounts = categorys.reduce((accumulator, col) => {accumulator[col] = {}; return accumulator}, {})
	if (data.cols) {
		for (col in categorycounts) {
			for (key in data.cols[col]) {
				if (filtercounts[key][data.cols[col][key]]) {
					filtercounts[key][data.cols[col][key]] = filtercounts[key][data.cols[col][key]] + categorycounts[col]
				} else {
					filtercounts[key][data.cols[col][key]] = categorycounts[col]
				}
			}
		}
	}

	let selecteddata = [(selectedcat) ? filtercounts[selectedcat] : ((categorycounts) ? categorycounts : daterangefilter)]
	selectedvalues = Object.keys(selecteddata[0])
	chart = c3.generate({
		bindto: `#${mapName}-chart-area`,
		data: {
			json: selecteddata,
			keys: {
				//x: 'year',
				value: selectedvalues,
			},
			type: 'donut',
		},
		donut: {
			label: {
				format: (value, percent, cat) => `${value}\n${percent.toLocaleString("en", {style: "percent"})}`
			}
		}
	});
	d3.select(`#${mapName}-shade`).attr('class', 'shade shade-off background-color-sea')

	d3.select(window).on('resize', function() {
		chart.resize();
	});

	chart_data = data
}
