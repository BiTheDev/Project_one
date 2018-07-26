
function graph(){
	var chart = new CanvasJS.Chart("chartContainer", {
		title: {
			text: "Financial Data"
		},
		axisX: {
			valueFormatString: "MMM YYYY"
		},
		axisY2: {
			title: "Profit",
			prefix: "$",
		},
		toolTip: {
			shared: true
		},
		legend: {
			cursor: "pointer",
			verticalAlign: "top",
			horizontalAlign: "center",
			dockInsidePlotArea: true,
			itemclick: toogleDataSeries
		},
		data: [{
			type:"line",
			axisYType: "secondary",
			name:"{{user.nickname|safe}}",
			showInLegend: true,
			markerSize: 0,
			yValueFormatString: "$###,###,###",
			dataPoints: [		
				{ x: new Date(2014, 00, 01), y: 100000000 },
				{ x: new Date(2014, 01, 01), y: 889 },
				{ x: new Date(2014, 02, 01), y: 890 },
				{ x: new Date(2014, 03, 01), y: 899 },
				{ x: new Date(2014, 04, 01), y: 903 },
				{ x: new Date(2014, 05, 01), y: 925 },
				{ x: new Date(2014, 06, 01), y: 899 },
				{ x: new Date(2014, 07, 01), y: 875 },
				{ x: new Date(2014, 08, 01), y: 927 },
			]
		}],
	});

chart.render();

function toogleDataSeries(e){
	if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
		e.dataSeries.visible = false;
	} else{
		e.dataSeries.visible = true;
	}
	chart.render();
}
}