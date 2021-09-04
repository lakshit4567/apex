$(".pagination").addClass("justify-content-center");
var f_q = JSON.parse(document.getElementById("f_q").textContent);
var f_s = JSON.parse(document.getElementById("f_s").textContent);
var es_s = JSON.parse(document.getElementById("es_s").textContent);
var es_u = JSON.parse(document.getElementById("es_u").textContent);

var empty_f_q = JSON.stringify(f_q)
var empty_f_s = JSON.stringify(f_s)
var empty_es_s = JSON.stringify(es_s)
var empty_es_u = JSON.stringify(es_u)

if( empty_es_s == '{}' && empty_es_u == '{}'){
	document.getElementById("no_data_es_o").innerHTML = "<br><div class='alert alert-light lead'><strong>Note:</strong> No Data Available</div>";
}
else{

// Essential Stock Flow chart
var stkflow = document.getElementById("myBar");
var myChart = new Chart(stkflow, {
	type: 'bar',
	data: {
		        labels: ["Cylinder", "Belt", "Fevil", "Cutting Oil", "Cutter", "Polish Wheel", "Matt Wheel", "Buff", "Plastic Roll", "Conjunction Rod", "Powder Box", "Big Carton", "Small Plastic"],
		datasets: [{
			label: 'Stock',
			backgroundColor: "rgba(29, 53, 87)",
			data: [es_s['Cylinder'],es_s['Belt'],es_s['Fevil'],es_s['Cutting Oil'],
					es_s['Cutter'],es_s['Polish Wheel'],es_s['Matt Wheel'],es_s['Buff'],
					es_s['Plastic Roll'],es_s['Conjunction Rod'],es_s['Powder Box'],
					es_s['Big Carton'], es_s['Small Plastic']],
		}, {
			label: 'Usage',
			backgroundColor: "rgba(230, 57, 70)",
			data: [-es_u['Cylinder'],-es_u['Belt'],-es_u['Fevil'],-es_u['Cutting Oil'],
					-es_u['Cutter'],-es_u['Polish Wheel'],-es_u['Matt Wheel'],-es_u['Buff'],
					-es_u['Plastic Roll'],-es_u['Conjunction Rod'],-es_u['Powder Box'],
					-es_u['Big Carton'], -es_u['Small Plastic']],
		}],
	},
	options: {
		indexAxis: 'y',
		plugins: {
			title: {
				display: false,
				text: 'Chart'
			},
		},
		responsive: true,
		scales: {
			x: {
				stacked: true,
			},
			y: {
				stacked: true,
			}
		}
	},
});
}
	// options: {
	// 	tooltips: {
	// 	displayColors: true,
	// 	callbacks:{
	// 		mode: 'x',
	// 	},
	// 	},
	// 	scales: {
	// 		xAxes: {
	// 			stacked: true,
	// 			gridLines: {
	// 			display: false,
	// 			}
	// 		},
	// 		yAxes: {
	// 			stacked: true,
	// 			ticks: {
	// 			beginAtZero: true,
	// 			},
	// 			type: 'linear',
	// 		}
	// 	},
	// 	responsive: true,
	// 	maintainAspectRatio: true,
	// 	legend: { position: 'bottom' },
	// 	}
	// });

// FM Made and Sell chart
if( empty_f_s == '{}' && empty_f_q == '{}'){
	document.getElementById("no_data_fmf_o").innerHTML = "<br><div class='alert alert-light lead'><strong>Note:</strong> No Data Available</div>";
}
var speedCanvas = document.getElementById("myMixChart");

var dataFirst = {
    label: "Quantity Produced",
	data: [f_q['01'],f_q['02'],f_q['03'],f_q['04'],f_q['05'],f_q['06'],f_q['07'],f_q['08'],f_q['09'],f_q['10'],f_q['11'],f_q['12']],
    fill: true,
    backgroundColor: "rgba(230, 57, 70)",
    borderColor: 'red',
    order: 1,
    type: 'bar'
};

var dataSecond = {
    label: "Quantity Sale",
	data: [f_s['01'],f_s['02'],f_s['03'],f_s['04'],f_s['05'],f_s['06'],f_s['07'],f_s['08'],f_s['09'],f_s['10'],f_s['11'],f_s['12']],
    lineTension: 0,
    fill: false,
    borderColor: "rgba(29, 53, 87)",
    order: 0,
    type: 'line'
};

var speedData = {
labels: ["Jan", "Feb", "March", "April", "May", "June", "July","Aug","Sep","Oct","Nov","Dec"],
datasets: [dataFirst, dataSecond]
};

var chartOptions = {
legend: {
    display: true,
    position: 'top',
    labels: {
    boxWidth: 80,
    fontColor: 'black'
    }
}
};

var lineChart = new Chart(speedCanvas, {
data: speedData,
options: chartOptions
});

// FM Made and Sell chart
