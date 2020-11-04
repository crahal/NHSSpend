let csvdata = {};
let csvdatalist = [];

let datestring = ""
let data_url = "/assets/nhs/";
//`/assets/data/excess/${datafile}`

let sortAscending = false;
let mapName = 'map';
let barchart1;
let barchart2;
let pounds = new Intl.NumberFormat('en-GB', { style: 'currency', currency: 'GBP', minimumFractionDigits: 0 })

let ccg_config = {
	id: 'ccg',
	label: 'CCG',
	filename: 'ccg_table.csv',
	bar_cols: ['Value to VCS (%)', 'Count to VCS (%)', 'Value of Payments (m)'],
	bar_col: 'Value to VCS (%)',
	search_col: 'ccg19nm',
	headers: {
		'anchorkey': 'ccg19cd',
		'desckey': 'ccg19nm',
		'NHS Abrev': {label: 'NHS Abrev', type: 'String'},
		'ccg19cd': {label: 'ccg19cd', type: 'String'},
		'Number of Payments': {label: 'Number of Payments', type: 'Number'},
		'Value of Payments (m)': {label: 'Value of Payments (m)', type: 'Number', formatter: pounds},
		'Number of Datasets': {label:'Number of Datasets', type: 'Number'},
		'Value to VCS (%)': {label:'Value to VCS (%)', type: 'Number'},
		'Count to VCS (%)': {label:'Count to VCS (%)', type: 'Number'},
		'Highest Value Charity Recipient': {label:'Highest Value Charity Recipient', type: 'String'},
		'Number Payments to VCS': {label:'Number Payments to VCS', type: 'Number'},
		'Number of Charity Suppliers': {label:'Number of Charity Suppliers', type: 'Number'},
		'ccg19nm': {label: 'ccg19nm', type: 'String'},
	}
}

let trust_config = {
	id: 'trust',
	label: 'Trust',
	filename:'trust_table.csv',
	bar_cols: ['Value to VCS (%)', 'Count to VCS (%)', 'Value of Payments (m)'],
	bar_col: 'Value to VCS (%)',
	search_col: 'trust name',
	headers: {
		'anchorkey': 'trust name',
		'desckey': 'trust name',
		'NHS Abrev': {label: 'NHS Abrev', type: 'String'},
		'trust name': {label: 'trust name', type: 'String'},
		'Latitude': {label: 'Latitude', type: 'Number'},
		'Longitude': {label: 'Longitude', type: 'Number'},
		'Number of Payments': {label:'Number of Payments', type: 'Number'},
		'Value of Payments (m)': {label:'Value of Payments (m)', type: 'Number', formatter: pounds},
		'Number of Datasets': {label:'Number of Datasets', type: 'Number'},
		'Value to VCS (%)': {label:'Value to VCS (%)', type: 'Number'},
		'Count to VCS (%)': {label:'Count to VCS (%)', type: 'Number'},
		'Highest Value Charity Recipient': {label:'Highest Value Charity Recipient', type: 'String'},
		'Number Payments to VCS': {label:'Number Payments to VCS', type: 'Number'},
		'Number of Charity Suppliers': {label:'Number of Charity Suppliers', type: 'Number'},
    }
}

headers_charities = {
	anchorkey: 'Charity Name',
	desckey: 'Charity Name',
	cols: ['Number of Payments (%)','Value of Payments (%)'],
	'Charity Name': {label: 'Charity Name', type: 'String'},
	'Number of Payments (%)': {label: 'Number of Payments (%)', type: 'Number'},
	'Value of Payments (%)': {label: 'Value of Payments (%)', type: 'Number'},
	'Registration Number': {label: 'Registration Number', type: 'Number'},
	'Registration Date': {label:'Registration Date', type: 'String'},
	'Rank': {label:'Rank', type: 'Number'},
	'Year': {label:'Year', type: 'String'},
}

headers_companies = {
	anchorkey: 'NHS Abrev',
	desckey: 'NHS CCG',
	cols: ['Charity Value (£)','Count to VCS (%)', 'Value to VCS (%)'],
	'NHS Abrev': {label: 'NHS Abrev', type: 'String'},
	'Charity Value (£)': {label: 'Charity Value (£)', type: 'Number', formatter: pounds},
	'Charity Count': {label: 'Charity Count', type: 'Number'},
	'Count to VCS (%)': {label: 'Count to VCS (%)', type: 'Number'},
	'Value to VCS (%)': {label:'Value to VCS (%)', type: 'Number'},
	'Rank': {label:'Rank', type: 'Number'},
	'Year': {label:'Year', type: 'String'},
	'NHS CCG': {label:'NHS CCG', type: 'String'},
}

//d3.json(data_url + "data/models.json").then(function(model_index) {
//	let picker = d3.select('#' + mapName + '-report-picker')
//	picker.selectAll('option').remove()
//	picker
//		.selectAll('option')
//		.data(Object.keys(model_index))
//		.enter()
//		.append('option')
//		.text(x => x)
//		.attr('value', x => model_index[x]);
//	picker.select('option').attr('value', model_index['latest'])
//	picker.select('option').text('Latest')
//	//var formData = new FormData(document.querySelector('form'))
//	var formDict = JSON.parse(document.getElementById('chart-setup').innerHTML);
//	//for(var pair of formData.entries()) {
//	//	formDict[pair[0]] = pair[1]
//	//}
//	if (('report' in formDict) && (formDict['report'] in model_index))
//	{
//		picker.property('value', model_index[formDict['report']])
//		csv_url = data_url + model_index[formDict['report']];
//	} else {
//		picker.property('value', model_index['latest'])
//		csv_url = data_url + model_index['latest'];
//	}

//	//override url for now
//	csv_url = data_url + 'csv1_tab2.csv';
//   let selCol = document.getElementById('tab1' + '-select-tab');
//   selCol.value = selCol[0].value;

//	fetch_csv();

//	picker.on('change', change_report)
//	d3.select('#' + 'tab1' + '-select-tab').on('change', change_report)
//)

let tab = 'tab1'
let config = ccg_config
change_config(document.getElementById(`${tab}-select-tab`).value)
d3.select(`#${tab}-select-tab`).on('change', change_config_callback)

function change_config_callback() {
	change_config(this.value)
}

function change_config(config_string) {
	if (config_string === 'ccg') {
		config = ccg_config;
	} else {
		config = trust_config;
	}

	csvdata = {};
	csvdatalist = [];
	//dggmap.clear()

	fetch_csv();
}

function ccg_geo_map(col) {
	let coords = [-1.30, 53.22]
	// The svg
	let svg = d3.select("#ccg_map");
	let width = $("#ccg_map").width();
	let height = $("#ccg_map").height();
	svg.attr("viewBox", [0, 0, width, height]);
	//svg.attr("width", width)
	//svg.attr("height", height)

	// Map and projection
	let ukproj = d3.geoAlbers()
		//.center([0, 55.4])
		.center([-2.25, 53])
		.rotate([4.4, 0])
		.parallels([50, 60])
		.scale(width * 11)
		//.translate([width / 2, height / 2]);
	let projection = d3.geoTransverseMercator()
	  //.scale(height / Math.PI)
	  .scale(5000)
	  .center([-2.25, 53])
	  //.scale(100)
	  .translate([width / 2, height / 2]);
	let ppath = d3.geoPath()
              .projection(ukproj);
	function scale (scaleFactor,width,height,offsetX,offsetY) {
	  return d3.geoTransform({
		point: function(x, y) {
		  this.stream.point( (x - width/2) * scaleFactor + width/2 - offsetX , - (y - height/2) * scaleFactor + height/2 + offsetY);
		}
	  });
	}
	let path = d3.geoPath().projection(scale(0.001,width,height,1500,1000))

	// Data and color scale
	//let data = d3.map();

	// Load external data and boot
	//d3.queue()
	//  .defer(d3.json, base_url + 'data/Clinical_Commissioning_Groups_April_2019_Ultra_Generalised_Clipped_Boundaries_England.geojson')
	  //.defer(d3.csv, "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world_population.csv", function(d) { data.set(d.code, +d.pop); })
	//  .await(ready);

    //d3.csv(data_url + 'ccg_table.csv', function (d) {
	//	data.set(d.ccg19nm, +d['Value to VCS (%)']);
    //}).then(function (cols)  {

	d3.json(data_url + 'output.json').then(function(topo) {
		let datadomain = csvdatalist.map(x => parseFloat(x[col]))
		let max = d3.max(datadomain)
		let step = max / 8
		let colours = d3.schemeBlues[9]
		if (col === 'Count to VCS (%)') {
			colours = d3.schemeOranges[9]
		} else if (col === 'Value of Payments (m)') {
			colours = d3.schemeGreens[9]
		}
		let colorScale = d3.scaleThreshold()
		  .domain(d3.range(0, max, step))
		  //.domain(d3.range(0, 3, 0.5))
		  .range(colours);

		let x = d3.scaleLinear()
			.domain([0, max])
			//.domain([0, 3])
			.rangeRound([0, width - 40]);

		let y = d3.scaleLinear()
			.domain([0, max])
			//.domain([0, 3])
			.rangeRound([30, 2*height/3]);

		let radscale = d3.scaleLinear()
			.domain([0, max])
			//.domain([0, 3])
			.rangeRound([10, 20]);

		d3.select('#svg-map-legend').remove()
		let g = svg.append("g")
			.attr("id", "svg-map-legend")
			.attr("class", "key")
			.attr("transform", `translate(${20}, ${20})`);

		g.selectAll("rect")
		  .data(colorScale.range().map(function(d) {
			  d = colorScale.invertExtent(d);
			  if (d[0] == null) d[0] = y.domain()[0];
			  if (d[1] == null) d[1] = y.domain()[1];
			  return d;
			}))
		  //.enter().append("rect")
			//.attr("height", 8)
			//.attr("x", function(d) { return x(d[0]); })
			//.attr("width", function(d) { return x(d[1]) - x(d[0]); })
			//.attr("fill", function(d) { return colorScale(d[0]); });
		  .enter().append("rect")
			.attr("height", function(d) { return y(d[1]) - y(d[0]); })
			.attr("y", function(d) { return y(d[0]); })
			.attr("width", 8)
			.attr("fill", function(d) { return colorScale(d[0]); });

		g.append("text")
			.attr("class", "caption")
			.attr("x", -6)
			//.attr("y", y.range()[0])
			.attr("y", 10)
			.attr("fill", "#000")
			.attr("text-anchor", "start")
			.attr("font-weight", "bold")
			.text(col);

		let unitString = col === 'Value of Payments (m)' ? "£" : "%"
		g.call(d3.axisRight(y)
			.tickSize(13)
			.tickFormat(function(n, i) { return i ? n.toFixed(2) : ((unitString === "£") ? `${unitString}${n}`: `${n} ${unitString}`); })
			.tickValues(colorScale.domain()))
		  .select(".domain")
			.remove();

		// Draw the map
		d3.select("#svg-map-topo").remove()
		let mapgroup = svg.append("g").attr("id", "svg-map-topo");
			//.attr("transform", `translate(${-(width / 1.5)}, ${+(height / 5)})`)
			//.attr("transform", `translate(${margin.left},0)`)
			//.attr("transform", function() {
             //   return d3.svg.transform()
            //        .translate(-d3.select(this).attr("width")/2, -d3.select(this).attr("height")/2)();
            //})
            //.transform([width / 2, height / 2])
		mapgroup.selectAll("path")
			.data(topojson.feature(topo,topo.objects.Clinical_Commissioning_Group_CCG_IMD_2019_OSGB1936).features)
			.join("path")
				// draw each country
				.attr("d", ppath)
				// set the color of each country
				.attr("fill", function (d) {
					if (config.id === 'trust') {
						d.total = 0
						return 0;
					} else {
						d.total = 0
						if (d.properties[config.headers.anchorkey] in csvdata) {
							d.total = parseFloat(csvdata[d.properties[config.headers.anchorkey]][col]);
						}
						return colorScale(d.total);
					}
				})
				//.attr("fill", colorScale(d.total))
				//.style("stroke","#333")
				.attr("stroke","#333")
			.append("title")
                  .text(function(d) { return d.properties.ccg19nm + "\n" + ((unitString === "£") ? `${unitString}${d.total}`: `${d.total.toFixed(3)} ${unitString}`); });
		if (config.id === 'trust') {
			mapgroup.selectAll("circle")
				.data(csvdatalist)
				.join("circle")
					//cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />
					.attr("cx", d => ukproj([parseFloat(d.Longitude), parseFloat(d.Latitude)])[0])
					.attr("cy", d => ukproj([parseFloat(d.Longitude), parseFloat(d.Latitude)])[1])
					.attr("stroke", "black")
					.attr("stroke-width", "2")
					.attr("fill", function (d) {
						return colorScale(parseFloat(d[col]));
					})
					.attr("r", d => radscale(parseFloat(d[col])))
				.append("title")
					  .text(function(d) { return d[config.headers.desckey] + "\n" + ((unitString === "£") ? `${unitString}${parseFloat(d[col])}`: `${parseFloat(d[col]).toFixed(3)} ${unitString}`); });
        }
		bbox = mapgroup.node().getBoundingClientRect();
		svgbbox = svg.node().getBoundingClientRect();
		mapgroup.attr("transform", `translate(${-(bbox.left - svgbbox.left)}, ${-(bbox.top - svgbbox.top) + 50})`)
		d3.select(`#${mapName}-shade`).attr('class', 'd-none')
		console.log(ukproj([parseFloat(csvdatalist[0].Longitude), parseFloat(csvdatalist[0].Latitude)]))
	})
}

function ccg_map() {
	//53° 22' 0" N / 1° 30' 0" W
	let coords = [-1.30, 53.22]
    var map = new Datamap({
        element: document.getElementById(`#${mapName}-chart-area`),
        geographyConfig: {
            dataUrl: data_url + 'output.json',
        },
        scope: 'custom',
        setProjection: function(element, options) {
           var projection, path;
            projection = d3.geoAlbers()
                .center(coords)
                .scale(element.offsetWidth)
                .translate([element.offsetWidth / 2, element.offsetHeight / 2]);
            path = d3.geoPath()
                .projection( projection );

            return {path: path, projection: projection};
        }

        //setProjection: function (element) {
        //    var projection = d3.geoEquirectangular()
        //            .center(coords) // always in [East Latitude, North Longitude]
        //            .scale(1000);
        //    var path = d3.geoPath().projection(projection);
        //    return { path: path, projection: projection };
        //}
    });
    d3.select(`#${mapName}-shade`).attr('class', 'd-none')
}


function parseFloatForNumberSort(x) {
	let y = Number.parseFloat(x)
	return y ? y : 0
}

let tabulate = function (dict, header_dict) {
function rowsort(d) {
	theadr.selectAll('th').attr('class',  'header').text(d => header_dict ? header_dict[d].label : d);

	if (sortAscending) {
		if ((header_dict) && (header_dict[d].type == 'Number')) {
			rows.sort((a, b) => d3.ascending(parseFloatForNumberSort(a[d]), parseFloatForNumberSort(b[d])));
		}
		else
		{
			rows.sort((a, b) => d3.ascending(a[d], b[d]));
		}
		sortAscending = false;
		this.className = 'ascending';
		//this.textContent = header_dict[d] + ' \u21E7';
	} else {
		if ((header_dict) && (header_dict[d].type == 'Number')) {
			rows.sort((a, b) => d3.descending(parseFloatForNumberSort(a[d]), parseFloatForNumberSort(b[d])));
		}
		else
		{
			rows.sort((a, b) => d3.descending(a[d], b[d]));
		}
		sortAscending = true;
		this.className = 'descending';
		//this.textContent = header_dict[d] + ' \u21E9';
	}
}

	let columns = []
	for (let key in dict[0]) {
		columns.push(key)
	}
	data = dict
	let table = d3.select(`#${mapName}-table`);
	table.select('thead').remove();
	table.select('tbody').remove();
	let theadr = table.append('thead').append('tr')
	let tbody = table.append('tbody')
	let anchorkey = header_dict ? header_dict.anchorkey : 0

	theadr.selectAll('th')
		.data(columns)
		.enter()
		.append('th')
		.text((d) => header_dict ? header_dict[d] ? header_dict[d].label : d : d)
		.attr('class', (d) => (d === '') ? 'ascending' : 'header')
		.attr('style', 'border-top: 0px;')
		.on('click', rowsort)

		//.append('span').selectAll('span').data(d3.range(2)).enter()
		//.append('div').attr('class', 'col').attr('data-feather', function (d) { if (d) { return 'chevron-up' } else { return 'chevron-down'} })

	var rows = tbody.selectAll('tr')
		.data(data)
		.enter()
		.append('tr')
		.attr('id', row => row[anchorkey])
		//.attr('class', 'row-anchor');

	//rows.selectAll('tr').append('a')
	var cells = rows.selectAll('td')
		.data((row) => columns.map((column) => ({ 'column': column, value: row[column] })))
		.enter()
		.append('td')
		.attr('data-th', (d => header_dict ? header_dict[d.column] ? header_dict[d.column].label : d.column : d.column))
		.text(d => header_dict[d.column].formatter ? header_dict[d.column].formatter.format(d.value) : d.value)
		//.attr('id', function (d) { if (d.column == 'ISO3Code') return d.value })

	feather.replace()
	d3.select(`#${mapName}-table-shade`).attr('class', 'd-none')
	//scrollToWindowHash()
}

function fetch_csv() {
	let csv_url = data_url + config.filename;
    d3.csv(csv_url, function (d) {
            csvdata[d[config.headers.anchorkey]] = d;
            csvdatalist.push(d);
    }).then(ready);
    let select = document.getElementById("year-picker");
    d3.csv(`${data_url}${config.id}_top10_charities.csv`).then(data => charities(data, select.value));
    d3.csv(`${data_url}${config.id}_top10_orgs.csv`).then(data => orgs(data, select.value));

	d3.select(`#${tab}-csvlink`).on("click", function() {location.href=csv_url;});
}

let charities_data
function charities(data, year) {
    //dggmap.updateColors();
    charities_data = data
	let select = document.getElementById("year-picker");
	//select.onchange = function(d) {this.labels[0].textContent = this.value; charities(charities_data, this.value); orgs(orgs_data, this.value)}
	//select.labels[0].textContent = select.value
	select.onchange = function(d) {charities(charities_data, this.value); orgs(orgs_data, this.value)}
    let charitiesbarcol = 'Rank'
    let bardata = data.filter(x => !isNaN(x[charitiesbarcol])).filter(x => x['Year'] === year);
    bardata = bardata.sort((a, b) => a['Rank'] - b['Rank']);
    let chart_id = 'bar'
    barchart1 = c3bar(chart_id, bardata.slice(0, 10), headers_charities.anchorkey, headers_charities.cols);
    d3.select(`#${chart_id}-chart-caption`).text(`${config.label} top 10 Procurers from VCS in ${year}`)
}

let orgs_data
function orgs(data, year) {
    //dggmap.updateColors();
    orgs_data = data
    let companiesbarcol = 'Rank'
    let bardata = data.filter(x => !isNaN(x[companiesbarcol])).filter(x => x['Year'] === year);
    bardata = bardata.sort((a, b) => a['Rank'] - b['Rank']);
    //barchart2 = c3bar('bar2', bardata.slice(0, 10), headers_companies.anchorkey, ['Charity Value (£)', 'Charity Count','Count to VCS (%)', 'Value to VCS (%)']);
    let chart_id = 'bar2'
    barchart2 = c3bar(chart_id, bardata.slice(0, 10), headers_companies.anchorkey, headers_companies.cols);
    d3.select(`#${chart_id}-chart-caption`).text(`${config.label} top 10 VCS Suppliers in ${year}`)
}

function ready(error, us) {
    // We need to colorize every country based on "numberOfWhatever"
    // colors should be uniq for every value.
    // For this purpose we create palette(using min/max series-value)
    //can we get the headers from the csv read func?
    //dataset.forEach(function(obj){ onlyValues.append(obj['numberOfThings']); });
    //for (var key in csvdata[Object.keys(csvdata)[0]]) {
    //    if ((key !== "") && (key !== 'Country') && (key !== 'ISO3Code')) {
    //        headers.push(key);
    //    }
    //}
    let selCol1 = document.getElementById(`${tab}-select-column`);
    //d3.select('#'+ mapName + '-select-column').selectAll('option').remove()

    //dggmap.setData(selCol1.value);
    //dggmap.updateColors();
    let bardata = csvdatalist.filter(x => !isNaN(x[config.bar_col]))
        bardata = bardata.sort((a, b) => b[config.bar_col] - a[config.bar_col]);
    //barchart1 = c3bar('bar', bardata.slice(0, 10), headers.anchorkey, barcols);
    //d3.select('#'+ 'bar' + '-chart-caption').text('Top 10 CCGs by Company payments')
    //donut('Number_Payments_to_Companies', 'CCG_ABREV');

    //barchart2 = c3bar('bar2', bardata.slice(-10), headers.anchorkey, barcols);
    //d3.select('#'+ 'bar2' + '-chart-caption').text('Bottom 10 CCGs by Company payments')

    tabulate(csvdatalist, config.headers);

    //TODO get the datestring cleanly
    //var picker = document.getElementById('tab1' + "-report-picker")
    //var report_title = picker.options[picker.selectedIndex].text
    //if (report_title == 'Latest') {
	//	report_title = picker.value.split('/')[1]
    //}
    //d3.select('#' + mapName + '-report-label').select('h2').text(report_title);
    //d3.select('#' + mapName + '-report-label').select('span').attr('class', 'd-none');

    //if (!window.location.search) {
	//	history.replaceState(null, '', '?report=' + report_title);
    //}
	d3.select(`#${tab}-sharemail`).on('click', function() {
		//window.open("mailto:?to=&body=I'd%20like%20to%20share%20this%20Digital%20Gender%20Gaps%20report%20with%20you.%0A%0A" + window.location.href + "&subject=Digital%20Gender%20Gaps%20Report%20-%20" + report_title, '_blank');
	})
	addSearch('map')
	ccg_geo_map(config.bar_col)
	d3.select(`#${tab}-select-column`).on('change', changeColumn)
}

function changeColumn() {
    update(this.value, this.options[this.selectedIndex].label);
}

function update(col, colname) {
    //let bardata = csvdatalist.filter(x => !isNaN(x[col]))
    //    bardata = bardata.sort((a, b) => b[col] - a[col]);
    //barchart1.load({
    	//unload: true,
    //	json: bardata.slice(0, 10),
   // 	keys: { x: headers_charities.anchorkey, value: headers_charities.cols},
   // })
   // barchart2.load({
    	//unload: true,
   // 	json: bardata.slice(-10),
    //	keys: { x: headers_companies.anchorkey, value: headers_companies.cols},
   // })
    ccg_geo_map(col)
   // let year = getElementById('year-picker').value
    //let chart_id = 'bar'
    //d3.select(`#${chart_id}-chart-caption`).text(`Top 10 Procurers from VCS in ${year} by ${colname}`)
    //chart_id = 'bar2'
    //d3.select(`#${chart_id}-chart-caption`).text(`Top 10 VCS Suppliers in ${year} by ${colname}`)
}


var g;
function drawbar(col, catcol) {
var bardata = csvdatalist.filter(x => !isNaN(x[col]))
bardata = bardata.sort(function(a, b) {
	return b[col] - a[col];
});
bardata.splice(10)

var margin = ({top: 20, right: 0, bottom: 30, left: 40})

var height = 500;
var width = 500;

var yAxis = g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y))
    .call(g => g.select(".domain").remove())

var xAxis = g => g
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).tickSizeOuter(0))

var y = d3.scaleLinear()
    .domain([0, d3.max(bardata, d => d[col] * 100)]).nice()
    .range([height - margin.bottom, margin.top])

var x = d3.scaleBand()
    .domain(bardata.map(d => d[catcol]))
    .range([margin.left, width - margin.right])
    .padding(0.1)

  const svg =  d3.select('#' + 'bar' + '-chart-area').append("svg")
      .attr("viewBox", [0, 0, width, height]);

  g = svg.append("g")
      .attr("fill", "steelblue")

  g.selectAll("rect")
    .data(bardata)
    .join("rect")
      .attr("x", d => x(d[catcol]))
      .attr("y", d => y(d[col] * 100))
      .attr("height", d => y(0) - y(d[col] * 100))
      .attr("width", x.bandwidth());

  svg.append("g")
      .call(xAxis);

  svg.append("g")
      .call(yAxis);
}

function zupdate(col, catcol) {
	var bardata = csvdatalist.filter(x => !isNaN(x[col]))
  // DATA JOIN
  // Join new data with old elements, if any.
  //var bars = g.selectAll("text")
  //  .data(data);

  // UPDATE
  // Update old elements as needed.
  //bars.attr("class", "update");

  // ENTER
  // Create new elements as needed.
  //
  // ENTER + UPDATE
  // After merging the entered elements with the update selection,
  // apply operations to both.
 // bars.enter().append("text")
  //    .attr("class", "enter")
  //    .attr("x", function(d, i) { return i * 32; })
  //    .attr("dy", ".35em")
  //  .merge(text)
  //    .text(function(d) { return d; });

  g.selectAll("rect")
    .data(bardata)
    .join("rect")
      .attr("x", d => x(d[catcol]))
      .attr("y", d => y(d[col] * 100))
      .attr("height", d => y(0) - y(d[col] * 100))
      .attr("width", x.bandwidth());

  // EXIT
  // Remove old elements as needed.
  //bars.exit().remove();
}

function round(value, decimals) {
  return Number(Math.round(value+'e'+decimals)+'e-'+decimals);
}

function c3bar(id, data, catcol, cols) {
	let chart = c3.generate({
		padding: {
		  bottom: 10
		},
		bindto: `#${id}-chart-area`,
        data: {
			json: data,
			keys: { x: catcol, value: cols},
            type: 'bar',
            axes: {
            	'Value to VCS (%)': 'y2',
            	'Count to VCS (%)': 'y2',
            	'Value of Payments (m)': 'y',
            	'Number of Payments (%)': 'y2',
            	'Value of Payments (%)': 'y2',
            	'Rank': 'y2',
            	'Charity Value (£)': 'y',
            	'Charity Count': 'y2',
            },
            names : {
            	'Value to VCS (%)': 'Value to VCS (%)',
            	'Count to VCS (%)': 'Count to VCS (%)',
            	'Value of Payments (m)': 'Value of Payments (m)',
            	'Number of Payments (%)': 'Number of Payments (%)',
            	'Value of Payments (%)': 'Value of Payments (%)',
            	'Rank': 'Rank',
            	'Charity Value (£)': 'Charity Value (£)',
                'Charity Count': 'Charity Count',
            },
			//onclick: function (d, i) { console.log("onclick", d, i); },
			//onmouseover: function (d, i) { console.log("onmouseover", d, i); },
			//onmouseout: function (d, i) { console.log("onmouseout", d, i); }
        },
        bar: {
            width: {
                ratio: 0.5 // this makes bar width 50% of length between ticks
            }
            // or
            //width: 100 // this makes bar width 100px
        },
		axis: {
			rotated: true,
			x: {
				type: 'category',
			},
			y: {
				label: 'Amount paid (millions)',
				tick: {
					format: d => pounds.format(d)
				},
				show: false,
			},
			y2: {
				label: {
				  text: '% to VCS',
				  position: 'outer-right'
				},
				show: true,
			},
		},
		tooltip: {
          format: {
            title: (x, index) => data[x][config.headers.desckey]
          }
        }
    });

	d3.select(`#${id}-shade`).attr('class', 'd-none')
	return chart;
}

function addSearch(id) {
	d3.select(`#${id}-table-filter`).on("keyup", function() {
		var searched_data = csvdatalist;
		let text = this.value.trim();

		if (text.length > 1) {
			var searchResults = searched_data.map(function(r) {
				var regex = new RegExp(text, 'i');
				let test_data = r[config.search_col]
				if (regex.test(test_data)) {
					return regex.exec(test_data)[0];
				}
			})

			searchResults = searchResults.filter(function(r) {
				return r != undefined;
			})

			searched_data = searchResults.map(function(r) {
				return csvdatalist.filter(function(p) {
					return p[config.search_col].indexOf(r) != -1;
				})
			})

			searched_data = [].concat.apply([], searched_data)

			tabulate(searched_data, config.headers)
		} else {
			tabulate(csvdatalist, config.headers)
		}
	})
}
