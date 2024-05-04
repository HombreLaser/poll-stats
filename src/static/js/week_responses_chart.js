// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

export function main(endpoint) {
    const translated_days = {
	Mon: 'Lunes',
	Tue: 'Martes',
	Wed: 'Miércoles',
	Thu: 'Jueves',
	Fri: 'Viernes',
	Sat: 'Sábado',
	Sun: 'Domingo'
    }
    
    get_counts(endpoint).then((counts) => {
	const labels = Object.keys(counts).map((day) => translated_days[day]);
	
	draw(labels, Object.values(counts));
    });
}

async function get_counts(endpoint) {
    const response = await fetch(endpoint, {
        method: "GET",
        mode: "same-origin",
        credentials: "same-origin"
    });

    return response.json();
}

function draw(labels, data) {
    var ctx = document.getElementById("myAreaChart");
    var myLineChart = new Chart(ctx, {
	type: 'line',
	data: {
	    labels: labels,
	    datasets: [{
		label: "Respuestas",
		lineTension: 0.3,
		backgroundColor: "rgba(2,117,216,0.2)",
		borderColor: "rgba(2,117,216,1)",
		pointRadius: 5,
		pointBackgroundColor: "rgba(2,117,216,1)",
		pointBorderColor: "rgba(255,255,255,0.8)",
		pointHoverRadius: 5,
		pointHoverBackgroundColor: "rgba(2,117,216,1)",
		pointHitRadius: 50,
		pointBorderWidth: 2,
		data: data,
	    }],
	},
	options: {
	    scales: {
		xAxes: [{
		    time: {
			unit: 'date'
		    },
		    gridLines: {
			display: false
		    },
		    ticks: {
			maxTicksLimit: 7
		    }
		}],
		yAxes: [{
		    ticks: {
			min: 0,
			max: Math.max.apply(null, data) + 3,
			maxTicksLimit: 5
		    },
		    gridLines: {
			color: "rgba(0, 0, 0, .125)",
		    }
		}],
	    },
	    legend: {
		display: false
	    }
	}
    });
}
    
