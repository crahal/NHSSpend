let csvdata = {};
let csvdatalist = [];
let csv_url = "";

let datestring = ""
let base_url = "http://localhost/wordpress/wp-content/themes/nhsdash/";

let sortAscending = false;
let mapName = 'map';
let barchart1;
let barchart2;
let pounds = new Intl.NumberFormat('en-GB', { style: 'currency', currency: 'GBP', minimumFractionDigits: 0 })

let headers1 = {
	anchorkey: 'CCG_ABREV',
	id: {label: '#', type: 'Number'},
	CCG_fullname: {label: 'Name', type: 'String'},
	CCG_ABREV: {label: 'Code', type: 'String'},
	'Nuts Regions': {label: 'Nuts Regions', type: 'String'},
	Number_Payments_to_Companies: {label:'Company payments', type: 'Number'},
	Number_Payments_to_Charites: {label:'Charity payments', type: 'Number'},
	Value_Payments_to_Companies: {label:'Amount paid to companies', type: 'Number', formatter: pounds},
	Value_Payments_to_Charites: {label:'Amount paid to charities', type: 'Number', formatter: pounds},
}

let headers2 = {
	anchorkey: 'Entity',
	id: {label: '#', type: 'Number'},
	'Nuts Regions': {label: 'Nuts Regions', type: 'String'},
	'Type': {label: 'Type', type: 'String'},
	'Entity': {label: 'Entity', type: 'String'},
	Value_Payments: {label:'Payments amount', type: 'Number', formatter: pounds},
	Number_Payments: {label:'Payments', type: 'Number'},
}

let barcols1 = ['Number_Payments_to_Companies', 'Value_Payments_to_Companies', 'Number_Payments_to_Charites', 'Value_Payments_to_Charites'];
let barcols2 = ['Value_Payments', 'Number_Payments'];

let headers = headers1;
let barcols = barcols1;

let barcol1 = 'Number_Payments_to_Companies'
let barcol2 = 'Value_Payments'
let barcol = barcol1

d3.json(base_url + "data/models.json").then(function(model_index) {
	let picker = d3.select('#' + mapName + '-report-picker')
	picker.selectAll('option').remove()
	picker
		.selectAll('option')
		.data(Object.keys(model_index))
		.enter()
		.append('option')
		.text(x => x)
		.attr('value', x => model_index[x]);
	picker.select('option').attr('value', model_index['latest'])
	picker.select('option').text('Latest')
	//var formData = new FormData(document.querySelector('form'))
	var formDict = JSON.parse(document.getElementById('chart-setup').innerHTML);
	//for(var pair of formData.entries()) {
	//	formDict[pair[0]] = pair[1]
	//}
	if (('report' in formDict) && (formDict['report'] in model_index))
	{
		picker.property('value', model_index[formDict['report']])
		csv_url = base_url + model_index[formDict['report']];
	} else {
		picker.property('value', model_index['latest'])
		csv_url = base_url + model_index['latest'];
	}

	//override url for now
	csv_url = base_url + 'data/csv1_tab2.csv';
    let selCol = document.getElementById('tab1' + '-select-tab');
    selCol.value = selCol[0].value;

	fetch_csv();

	picker.on('change', change_report)
	d3.select('#' + 'tab1' + '-select-tab').on('change', change_report)
})

function change_report() {
	csv_url = base_url + this.value;
	if (this.value === 'data/csv1_tab2.csv') {
		headers = headers1;
		barcols = barcols1;
		barcol = barcol1;
	} else {
		headers = headers2;
		barcols = barcols2;
		barcol = barcol2;
	}

	csvdata = {};
	csvdatalist = [];
	//dggmap.clear()

	fetch_csv();
}

function ccg_geo_map() {
	let coords = [-1.30, 53.22]
	// The svg
	let svg = d3.select("#ccg_map"),
	  width = +svg.attr("width"),
	  height = +svg.attr("height");
	//svg.attr("viewBox", [0, 0, 1000, 1000]);

	// Map and projection
	let ukproj = d3.geoAlbers()
		.center([0, 55.4])
		.rotate([4.4, 0])
		.parallels([50, 60])
		.scale(6000)
		.translate([width / 2, height / 2]);
	let projection = d3.geoTransverseMercator()
	  .scale(height / Math.PI)
	  .center(coords)
	  //.scale(100)
	  .translate([width / 2, height / 2]);
	let ppath = d3.geoPath()
              .projection(projection);
	function scale (scaleFactor,width,height,offsetX,offsetY) {
	  return d3.geoTransform({
		point: function(x, y) {
		  this.stream.point( (x - width/2) * scaleFactor + width/2 - offsetX , - (y - height/2) * scaleFactor + height/2 + offsetY);
		}
	  });
	}
	let path = d3.geoPath().projection(scale(0.001,width,height,1500,1000))

	// Data and color scale
	let data = d3.map();
	let colorScale = d3.scaleThreshold()
	  .domain([100000, 1000000, 10000000, 30000000, 100000000, 500000000])
	  .range(d3.schemeBlues[7]);

	// Load external data and boot
	//d3.queue()
	//  .defer(d3.json, base_url + 'data/Clinical_Commissioning_Groups_April_2019_Ultra_Generalised_Clipped_Boundaries_England.geojson')
	  //.defer(d3.csv, "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world_population.csv", function(d) { data.set(d.code, +d.pop); })
	//  .await(ready);

    d3.csv(base_url + 'data/Clinical_Commissioning_Groups_April_2018_Names_and_Codes_in_England_.csv', function (d) {
		data.set(d.CCG18CD, +d.FID);
    }).then(function (cols)  {
		d3.json(base_url + 'data/Clinical_Commissioning_Groups_April_2019_Ultra_Generalised_Clipped_Boundaries_England_wgs84.json').then(function(topo) {
			// Draw the map
			svg.append("g")
				.selectAll("path")
				.data(topojson.feature(topo,topo.objects.Clinical_Commissioning_Groups_April_2019_Ultra_Generalised_Clipped_Boundaries_England).features)
				.join("path")
					// draw each country
					.attr("d", ppath)
					// set the color of each country
					.attr("fill", function (d) {
						d.total = data.get(d.properties.ccg19cd) || 0;
						return colorScale(d.total);
					})
					//.attr("fill", colorScale(d.total))
					//.style("stroke","#333")
					.attr("stroke","#333")
			d3.select('#' + mapName + '-shade').attr('class', 'd-none')
		})
	});

}

function ccg_map() {
	//53° 22' 0" N / 1° 30' 0" W
	let coords = [-1.30, 53.22]
    var map = new Datamap({
        element: document.getElementById('map-chart-area'),
        geographyConfig: {
            dataUrl: base_url + 'data/Clinical_Commissioning_Groups_April_2019_Ultra_Generalised_Clipped_Boundaries_England.json',
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
    d3.select('#' + mapName + '-shade').attr('class', 'd-none')
}

function fetch_csv() {
//    d3.queue()
//        .defer(d3.csv, csv_url, function (d) {
//            csvdata[d.ISO3Code] = d;
//            csvdatalist.push(d);
//        })
//       .await(ready);
    d3.csv(csv_url, function (d) {
            csvdata[d.CCG_ABREV] = d;
            csvdatalist.push(d);
    }).then(ready);
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
	let table = d3.select('#' + mapName + '-table');
	table.select('thead').remove();
	table.select('tbody').remove();
	let theadr = table.append('thead').append('tr')
	let tbody = table.append('tbody')
	let anchorkey = header_dict ? header_dict.anchorkey : 0

	theadr.selectAll('th')
		.data(columns)
		.enter()
		.append('th')
		.text((d) => header_dict ? header_dict[d].label : d)
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
		.attr('data-th', (d => header_dict ? header_dict[d.column].label : d.column))
		.text(d => header_dict[d.column].formatter ? header_dict[d.column].formatter.format(d.value) : d.value)
		//.attr('id', function (d) { if (d.column == 'ISO3Code') return d.value })

	feather.replace()
	d3.select('#' + mapName + '-table-shade').attr('class', 'd-none')
	scrollToWindowHash()
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
    let selCol1 = document.getElementById('tab1' + '-select-column');
    //d3.select('#'+ mapName + '-select-column').selectAll('option').remove()

    selCol1.value = selCol1[0].value;

    //dggmap.setData(selCol1.value);
    //dggmap.updateColors();
    let bardata = csvdatalist.filter(x => !isNaN(x[barcol]))
        bardata = bardata.sort((a, b) => b[barcol] - a[barcol]);
    barchart1 = c3bar('bar', bardata.slice(0, 10), headers.anchorkey, barcols);
    d3.select('#'+ 'bar' + '-chart-caption').text('Top 10 CCGs by Company payments')
    //donut('Number_Payments_to_Companies', 'CCG_ABREV');

    barchart2 = c3bar('bar2', bardata.slice(-10), headers.anchorkey, barcols);
    d3.select('#'+ 'bar2' + '-chart-caption').text('Bottom 10 CCGs by Company payments')

    tabulate(csvdatalist, headers);

    //TODO get the datestring cleanly
    var picker = document.getElementById('tab1' + "-report-picker")
    var report_title = picker.options[picker.selectedIndex].text
    if (report_title == 'Latest') {
		report_title = picker.value.split('/')[1]
    }
    //d3.select('#' + mapName + '-report-label').select('h2').text(report_title);
    //d3.select('#' + mapName + '-report-label').select('span').attr('class', 'd-none');
    d3.select('#' + 'tab1' + '-csvlink').on("click", function() {location.href=csv_url;});
    if (!window.location.search) {
		history.replaceState(null, '', '?report=' + report_title);
    }
	d3.select('#' + 'tab1' + '-sharemail').on('click', function() {
		window.open("mailto:?to=&body=I'd%20like%20to%20share%20this%20Digital%20Gender%20Gaps%20report%20with%20you.%0A%0A" + window.location.href + "&subject=Digital%20Gender%20Gaps%20Report%20-%20" + report_title, '_blank');
	})
	//addSearch()
	d3.select('#'+ 'tab1' + '-select-column').on('change', changeColumn)
	ccg_geo_map()
}

function changeColumn() {
    update(this.value, this.options[this.selectedIndex].label);
}

function update(col, colname) {
    let bardata = csvdatalist.filter(x => !isNaN(x[col]))
        bardata = bardata.sort((a, b) => b[col] - a[col]);
    barchart1.load({
    	//unload: true,
    	json: bardata.slice(0, 10),
    	keys: { x: headers.anchorkey, value: barcols},
    })
    barchart2.load({
    	//unload: true,
    	json: bardata.slice(-10),
    	keys: { x: headers.anchorkey, value: barcols},
    })
    d3.select('#'+ 'bar' + '-chart-caption').text('Top 10 CCGs by ' + colname)
    d3.select('#'+ 'bar2' + '-chart-caption').text('Bottom 10 CCGs by ' + colname)
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

function donut(col, catcol) {
var donut_data = csvdatalist.slice();
donut_data = donut_data.map(x => {
x[col] = round(x[col], 1);
return x;
});
donut_data = donut_data.sort(function(a, b) {
	return b[col] - a[col];
});


var chart = c3.generate({
	bindto: '#donut-chart-area',
    data: {
        json: donut_data,
        keys: { value: [col, catcol]},
        type : 'donut',
        onclick: function (d, i) { console.log("onclick", d, i); },
        onmouseover: function (d, i) { console.log("onmouseover", d, i); },
        onmouseout: function (d, i) { console.log("onmouseout", d, i); }
    },
    donut: {
        title: "Cats"
    }
});

d3.select('#' + 'donut' + '-shade').attr('class', 'd-none')
}

function c3bar(id, data, catcol, cols) {
	let chart = c3.generate({
		padding: {
		  bottom: 10
		},
		bindto: '#' + id + '-chart-area',
        data: {
			json: data,
			keys: { x: catcol, value: cols},
            type: 'bar',
            axes: {
            	Number_Payments_to_Companies: 'y2',
            	Number_Payments_to_Charites: 'y2',
            	Value_Payments_to_Companies: 'y',
            	Value_Payments_to_Charites: 'y',
            	Value_Payments: 'y',
            	Number_Payments: 'y2',
            },
            names : {
            	Number_Payments_to_Companies: 'Company payments',
            	Number_Payments_to_Charites: 'Charity payments',
            	Value_Payments_to_Companies: 'Amount paid to companies',
            	Value_Payments_to_Charites: 'Amount paid to charities',
            	Value_Payments: 'Amount paid',
            	Number_Payments: 'Payments',
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
			x: {
				type: 'category',
			},
			y: {
				label: 'Amount paid',
				tick: {
					format: d => pounds.format(d)
				}
			},
			y2: {
				label: 'Number of payments',
				show: true,
			},
		}
    });

	d3.select('#' + id + '-shade').attr('class', 'd-none')
	return chart;
}
