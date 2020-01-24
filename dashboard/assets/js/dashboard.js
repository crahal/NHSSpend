var csvdata = {};
var csvdatalist = [];
var csv_url = "";

var datestring = ""
var base_url = "https://s3.eu-west-3.amazonaws.com/www.digitalgendergaps.org/";

var sortAscending = false;
var mapName = 'map';

function createdatamap(id) {
	//TODO using a local var but should be able to access this.fills.defaultFill when its needed
	let defaultFill = '#F5F5F5';
    return new Datamap({
        element: document.getElementById(id),
        projection: 'equirectangular',
        responsive: true,
        //aspectRatio: 0.6785714285714286,
        //aspectRatio: 0.5625,
        aspectRatio: 0.5,
        // countries not listed in dataset will be painted with this color
        fills: {defaultFill: defaultFill},
        data: {},
        geographyConfig: {
            borderColor: '#DEDEDE',
            highlightBorderWidth: 2,
            // don't change color on mouse hover
            highlightFillColor: function (geo) {
            	if ((!geo) || (Object.keys(geo).length === 0) || !('numberOfThings' in geo) || isNaN(geo.numberOfThings) || (geo.numberOfThings === 0)) {
            		return defaultFill;
            	}
                return geo['fillColor'] || defaultFill;
            },
            // only change border
            highlightBorderColor: '#B7B7B7',
            // show desired information in tooltip
            popupTemplate: function (geo, data) {
                // don't show tooltip if country don't present in dataset
                if ((!data) || (Object.keys(data).length === 0) || !('numberOfThings' in data) || isNaN(data.numberOfThings) || (data.numberOfThings === 0)) {
                	return ['<div class="hoverinfo">',
                   	 geo.properties.name, '<br />',
                  	  'No data',,
                  	  '</div>'].join('');
                }
                // tooltip content
                return ['<div class="hoverinfo">',
                    '<strong>', geo.properties.name, '</strong>',
                    '<br>', '<strong>', (data.numberOfThings / 100).toFixed(3), '</strong>',
                    '</div>'].join('');
            }
        },
        done: function(datamap) {
            datamap.svg.selectAll('.datamaps-subunit').on('click', function(geography) {
                // alert(geography.properties.name);
                if (document.getElementById(geography.id)) {
                	window.location.href = "#" + geography.id;
                	anchorScroll(geography.id);
                }
            });
        }
    });
}

class DggMap {
	constructor(id_prefix) {
		this.id_prefix = id_prefix;
		this.datamap = createdatamap(this.id_prefix + '-chart-area');
		this.dataset = {};
		this.color_min_value = "#FF0000";
        this.color_max_value = "#00FF00";
	}

	clear() {
		this.dataset = {};
		this.datamap.options.data = {};
		this.map.updateChoropleth({}, {reset: true});
	}

	//TODO rewrite so that this expects key value pairs, trim the csv data to a single column elsewhere
	setData(column) {
		this.dataset = {};

		for (let key in csvdata) {
			let item = {};
			item['numberOfThings'] = csvdata[key][column] * 100;
			if (!isNaN(item['numberOfThings'])) {
				this.dataset[key] = item;
			}
		}
    }

	get minValue() {
		let range = Object.keys(this.dataset).map(key => this.dataset[key]['numberOfThings']);
		return Math.min.apply(null, range);
	}

	get maxValue() {
		let range = Object.keys(this.dataset).map(key => this.dataset[key]['numberOfThings']);
		return Math.max.apply(null, range);
	}

	get colour_min_value() {
		return this.color_min_value;
	}

	set colour_min_value(color) {
		this.color_min_value = color;
		this.updateColors();
    }

	get colour_max_value() {
		return this.color_max_value;
	}

    set colour_max_value(color) {
    	this.color_max_value = color;
		this.updateColors();
    }

	updateColors() {
		if (Object.keys(this.dataset).length === 0) {
			return;
		}
	//TODO save palettescale and recompute when colour min/max are changed via setters
		let paletteScale = d3.scale.linear()
			.domain([this.minValue, this.maxValue])
			.range([this.colour_min_value, this.colour_max_value]);

		// Datamaps expects data in format:
        // { "USA": { "fillColor": "#42a844", numberOfWhatever: 75},
        //   "FRA": { "fillColor": "#8dc386", numberOfWhatever: 43 } }
		for (let key in this.dataset) {
			if (isNaN(this.dataset[key]['numberOfThings']) || (this.dataset[key]['numberOfThings'] === 0)) {
				//get defaultFill from map
				this.dataset[key]['fillColor'] = this.map.options.fills.defaultFill;
			}
			else {
				this.dataset[key]['fillColor'] = paletteScale(this.dataset[key]['numberOfThings']);
			}
		}

		this.datamap.options.data = {};
		this.datamap.updateChoropleth(this.dataset, {reset: true});
		this.addLegend();
	}

	addLegend() {
		this.addVLegend();
		this.addHLegend();
		this.addColourPickers();
	}

	addVLegend() {
		let steps = d3.range(11).map(d => d3.format(".2f")((this.minValue + ((this.maxValue - this.minValue) * 0.1 * d))/100));
		steps.sort(d3.descending)

		d3.select('#' + this.id_prefix + '-v-legend-gradient')
			.attr('style', 'width: 15px; height: 95%; background: linear-gradient('
				+ this.colour_max_value + ', ' + this.colour_min_value + ')');

		d3.select('#' + this.id_prefix + '-v-legend-values').selectAll('div')
			.data(steps)
			.text(function(x) {
				if (x != "NaN") {
					return x;
				}
			});
	}

	addHLegend() {
		let steps = d3.range(11).map(d => d3.format(".2f")((this.minValue + ((this.maxValue - this.minValue) * 0.1 * d))/100));

		d3.select('#' + this.id_prefix + '-h-legend-gradient')
			.attr('style', 'width: 92.5%; height: 15px; background: linear-gradient(to right, '
				+ this.colour_min_value + ', ' + this.colour_max_value + ')');

		d3.select('#' + this.id_prefix + '-h-legend-values').selectAll('div')
			.data(steps)
			.text(function(x) {
				if (x != "NaN") {
					return x;
				}
			});
	}

	addColourPickers() {
		//TODO do we have a better option than declaring self to get at the object in the callback context?
		let self = this;
		d3.select('#' + this.id_prefix + '-color-min-input').attr('value', this.colour_min_value).on('change', function() {self.colour_min_value = this.value;})
		d3.select('#' + this.id_prefix + '-color-min-button').attr('style', 'background-color: ' + this.colour_min_value)
		d3.select('#' + this.id_prefix + '-color-min-link').attr('href', '/indicators#scale').text('Inequality')

		d3.select('#' + this.id_prefix + '-color-max-input').attr('value', this.colour_max_value).on('change', function() {self.colour_max_value = this.value;})
		d3.select('#' + this.id_prefix + '-color-max-button').attr('style', 'background-color: ' + this.colour_max_value)
		d3.select('#' + this.id_prefix + '-color-max-link').attr('href', '/indicators#scale').text('Equality')
	}
}

var dggmap = new DggMap(mapName);

d3.select(window).on('resize', function() {
	dggmap.datamap.resize();
});

d3.json(base_url + "data/models.json", function(model_index) {
	let picker = d3.select('#' + mapName + '-report-picker')
	picker.selectAll('option').remove()
	picker
		.selectAll('option')
		.data(Object.keys(model_index))
		.enter()
		.append('option')
		.text(function(x){return x;})
		.attr('value', function(x){return model_index[x];});
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

	fetch_csv();

	picker.on('change', change_report)
})

function change_report() {
	csv_url = base_url + this.value;

	csvdata = {};
	csvdatalist = [];
	dggmap.clear()

	fetch_csv();
}

function fetch_csv() {
    d3.queue()
        .defer(d3.csv, csv_url, function (d) {
            csvdata[d.ISO3Code] = d;
            csvdatalist.push(d);
        })
        .await(ready);
}

var tabulate = function (dict) {
function rowsort(d) {
	thead2.selectAll('th').attr('class',  function (d) { return 'header ' + class_dict[d] }).text(function (d) { return header_dict[d] });

	if (sortAscending) {
		if ((d === 'Country') || (d === 'ISO3Code')) {
			rows.sort(function(a, b) {return d3.ascending(a[d], b[d]);  });
		}
		else
		{
			rows.sort(function(a, b) {
				var ax = Number.parseFloat(a[d]);
				if (Number.isNaN(ax)) {
					ax = 0;
				}
				var bx = Number.parseFloat(b[d]);
                if (Number.isNaN(bx)) {
                	bx = 0;
                }
				return d3.ascending(ax, bx);
			});
		}
		sortAscending = false;
		this.className = 'ascending ' + class_dict[d];
		//this.textContent = header_dict[d] + ' \u21E7';
	} else {
		if ((d === 'Country') || (d === 'ISO3Code')) {
			rows.sort(function(a, b) {return d3.descending(a[d], b[d]);  });
		}
		else
		{
			rows.sort(function(a, b) {
				var ax = Number.parseFloat(a[d]);
				if (Number.isNaN(ax)) {
					ax = 0;
				}
				var bx = Number.parseFloat(b[d]);
                if (Number.isNaN(bx)) {
                	bx = 0;
                }
				return d3.descending(ax, bx);
			});
		}
		sortAscending = true;
		this.className = 'descending ' + class_dict[d];
		//this.textContent = header_dict[d] + ' \u21E9';
	}
}

	columns = []
	for (var key in dict[0]) {
		columns.push(key)
	}
	data = dict
	var table = d3.select('#' + mapName + '-modeltable');
	table.select('thead').remove();
	table.select('tbody').remove();
	var thead = table.append('thead')
	var tbody = table.append('tbody')

	var header_dict2 = {
		'': '',
		'Country': 'Country',
		'ISO3Code': 'alpha-3',
		'Ground Truth Internet GG': 'ITU Internet GG',
		'Internet online model prediction': 'Internet GG (Online Model Prediction)',
		'Internet Online-Offline model prediction': 'Internet GG (Online-Offline Prediction)',
		'Internet Offline model prediction': 'Internet GG (Offline Model Prediction)',
		'Mobile_GG': 'Mobile GG',
		'Mobile Online model prediction': 'Mobile GG (Online Model Prediction)',
		'Mobile Online-Offline model prediction': 'Mobile GG (Online-Offline Prediction)',
		'Mobile Offline model prediction': 'Mobile GG (Offline Model Prediction)',
	};
	var header_dict3 = {
		'': '#',
		'Country': 'Country',
		'ISO3Code': 'alpha-3',
		'Ground Truth Internet GG': 'Internet GG - ITU',
		'Internet online model prediction': 'Internet GG - Online',
		'Internet Online-Offline model prediction': 'Internet GG - Combined',
		'Internet Offline model prediction': 'Internet GG - Offline',
		'Mobile_GG': 'Mobile GG - GSMA',
		'Mobile Online model prediction': 'Mobile GG - Online',
		'Mobile Online-Offline model prediction': 'Mobile GG - Combined',
		'Mobile Offline model prediction': 'Mobile GG - Offline',
	};
	var header_dict = {
		'': '#',
		'Country': 'Country',
		'ISO3Code': 'alpha-3',
		'Ground Truth Internet GG': 'ITU',
		'Internet online model prediction': 'Online',
		'Internet Online-Offline model prediction': 'Combined',
		'Internet Offline model prediction': 'Offline',
		'Mobile_GG': 'GSMA',
		'Mobile Online model prediction': 'Online',
		'Mobile Online-Offline model prediction': 'Combined',
		'Mobile Offline model prediction': 'Offline',
	};
	var class_dict = {
		'': '',
		'Country': '',
		'ISO3Code': '',
		'Ground Truth Internet GG': 'table-primary',
		'Internet online model prediction': 'table-primary',
		'Internet Online-Offline model prediction': 'table-primary',
		'Internet Offline model prediction': 'table-primary',
		'Mobile_GG': 'table-info',
		'Mobile Online model prediction': 'table-info',
		'Mobile Online-Offline model prediction': 'table-info',
		'Mobile Offline model prediction': 'table-info',
	};
	var thead1 = thead.append('tr').attr('style', 'border-bottom: 0px;')
	thead1.append('th').attr('style', 'border-bottom: 0px;')
	thead1.append('th').attr('style', 'border-bottom: 0px;')
	thead1.append('th').attr('style', 'border-bottom: 0px;')
	var theadcell1 = thead1.append('th')
			.attr('colspan', '4')
			.attr('class', 'table-primary text-center')
			.attr('style', 'border-bottom: 0px;')
		theadcell1.append('a')
			.text('Internet GG')
			.attr('href', '/indicators#internet')
			.attr('class', 'mx-1')
		theadcell1.append('a')
			.text('?')
			.attr('class', 'badge badge-secondary')
			.attr('style', 'vertical-align: super;')
			.attr('href', '/indicators#internet')
	var theadcell2 = thead1.append('th')
			.attr('colspan', '4')
			.attr('class', 'table-info text-center')
			.attr('style', 'border-bottom: 0px;')
		theadcell2.append('a')
			.text('Mobile GG')
			.attr('href', '/indicators#mobile')
			.attr('class', 'mx-1')
		theadcell2.append('a')
			.text('?')
			.attr('class', 'badge badge-secondary')
			.attr('style', 'vertical-align: super;')
			.attr('href', '/indicators#mobile')
	var thead2 = thead.append('tr')
	thead2.selectAll('th')
		.data(columns)
		.enter()
		.append('th')
		.text(function (d) { return header_dict[d] })
		.attr('class', function (d) { if (d === '') { return 'ascending ' + class_dict[d] } else { return 'header ' + class_dict[d] }})
		.attr('style', 'border-top: 0px;')
		.on('click', rowsort)

		//.append('span').selectAll('span').data(d3.range(2)).enter()
		//.append('div').attr('class', 'col').attr('data-feather', function (d) { if (d) { return 'chevron-up' } else { return 'chevron-down'} })

	var rows = tbody.selectAll('tr')
		.data(data)
		.enter()
		.append('tr')
		.attr('id', function(row) { return row['ISO3Code']})
		//.attr('class', 'row-anchor');

	//rows.selectAll('tr').append('a')

	var cells = rows.selectAll('td')
		.data(function(row) {
			return columns.map(function (column) {
				return { column: column, value: row[column] }
			})
		})
		.enter()
		.append('td')
		.attr('data-th', function (d) {
        	return header_dict3[d.column];
        })
		.text(function (d) { return d.value })
		//.attr('id', function (d) { if (d.column == 'ISO3Code') return d.value })

	feather.replace()
	d3.select('#' + mapName + '-tableshade').attr('class', 'd-none')
	scrollToWindowHash()
	return table;
}

function ready(error, us) {
    if (error) throw error;
    // We need to colorize every country based on "numberOfWhatever"
    // colors should be uniq for every value.
    // For this purpose we create palette(using min/max series-value)
    //can we get the headers from the csv read func?
    var headers = [];
    //dataset.forEach(function(obj){ onlyValues.append(obj['numberOfThings']); });
    for (var key in csvdata[Object.keys(csvdata)[0]]) {
        if ((key !== "") && (key !== 'Country') && (key !== 'ISO3Code')) {
            headers.push(key);
        }
    }
    var selCol1 = document.getElementById(mapName + '-select-column');
    d3.select('#'+ mapName + '-select-column').selectAll('option').remove()

    for (var x in headers) {
		var header_dict5 = {
			'': '',
			'Country': 'Country',
			'ISO3Code': 'alpha-3',
			'Ground Truth Internet GG': 'Internet GG - ITU',
			'Internet online model prediction': 'Internet GG - Online',
			'Internet Online-Offline model prediction': 'Internet GG - Combined',
			'Internet Offline model prediction': 'Internet GG - Offline',
			'Mobile_GG': 'Mobile GG - GSMA',
			'Mobile Online model prediction': 'Mobile GG - Online',
			'Mobile Online-Offline model prediction': 'Mobile GG - Combined',
			'Mobile Offline model prediction': 'Mobile GG - Offline',
		};
        selCol1.options.add(new Option(header_dict5[headers[x]], headers[x]));
    }
    selCol1.value = headers[1];
    d3.select('#'+ mapName + '-select-column').on('change', changeColumn)

    dggmap.setData(selCol1.value);
    dggmap.updateColors();
    tabulate(csvdatalist);

    //TODO get the datestring cleanly
    var picker = document.getElementById(mapName + "-report-picker")
    var report_title = picker.options[picker.selectedIndex].text
    if (report_title == 'Latest') {
		report_title = picker.value.split('/')[1]
    }
    d3.select('#' + mapName + '-report-label').select('h2').text(report_title);
    d3.select('#' + mapName + '-report-label').select('span').attr('class', 'd-none');
    d3.select('#' + mapName + '-csvlink').on("click", function() {location.href=csv_url;});
    if (!window.location.search) {
		history.replaceState(null, '', '?report=' + report_title);
    }
	d3.select('#' + mapName + '-sharemail').on('click', function() {
		window.open("mailto:?to=&body=I'd%20like%20to%20share%20this%20Digital%20Gender%20Gaps%20report%20with%20you.%0A%0A" + window.location.href + "&subject=Digital%20Gender%20Gaps%20Report%20-%20" + report_title, '_blank');
	})
	addSearch()
	d3.select('#' + mapName + '-shade').attr('class', 'd-none')
}

function changeColumn() {
    dggmap.setData(this.value);
    dggmap.updateColors();
}

function addSearch() {
    d3.select('#' + mapName + '-search')
      .on("keyup", function() {
        var searched_data = csvdatalist,
            text = this.value.trim();

        var searchResults = searched_data.map(function(r) {
          var regex = new RegExp("^" + text + ".*", "i");
          if (regex.test(r.Country)) {
            return regex.exec(r.Country)[0];
          }
        })

        searchResults = searchResults.filter(function(r){
          return r != undefined;
        })

        searched_data = searchResults.map(function(r) {
           return csvdatalist.filter(function(p) {
            return p.Country.indexOf(r) != -1;
          })
        })

		searched_data = [].concat.apply([], searched_data)

		tabulate(searched_data)
		})
}
