// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

export function main(endpoint) {
    const translated_months = {
	Jan: "Enero",
	Feb: "Febrero",
	Mar: "Marzo",
	Apr: "Abril",
	May: "Mayo",
	Jun: "Junio",
	Jul: "Julio",
	Aug: "Agosto",
	Sep: "Septiembre",
	Oct: "Octubre",
	Nov: "Noviembre",
	Dec: "Diciembre"
    };

    get_counts(endpoint).then((counts) => {
	const labels = Object.keys(counts).map((month) => translated_months[month]);
	draw(labels, Object.values(counts));
    });
}

async function get_counts(endpoint) {
    const response = await fetch(`${endpoint}?type=yearly`, {
	mehtod: "GET",
	mode: "same-origin",
	credentials: "same-origin"
    });

    return response.json();
}

function draw(labels, data) {
    var ctx = document.getElementById("myBarChart");
    var myLineChart = new Chart(ctx, {
	type: 'bar',
	data: {
	    labels: labels,
	    datasets: [{
		label: "Revenue",
		backgroundColor: "rgba(2,117,216,1)",
		borderColor: "rgba(2,117,216,1)",
		data: data
	    }],
	},
	options: {
	    scales: {
		xAxes: [{
		    time: {
			unit: 'month'
		    },
		    gridLines: {
			display: false
		    },
		    ticks: {
			maxTicksLimit: 6
		    }
		}],
		yAxes: [{
		    ticks: {
			min: 0,
			max: Math.max.apply(null, data) + 3,
			maxTicksLimit: 5
		    },
		    gridLines: {
			display: true
		    }
		}],
	    },
	    legend: {
		display: false
	    }
	}
    });
}
