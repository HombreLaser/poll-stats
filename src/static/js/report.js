Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

export function main(endpoint) {
    get_report(endpoint).then((report) => {
	draw(report);
	document.getElementById("report-card-content").innerHTML = report.conclusion;
    });
}

async function get_report(endpoint) {
    const response = await fetch(endpoint, {
	method: "GET",
	mode: "same-origin",
	credentials: "same-origin"
    });

    return response.json();
}

function draw(report) {
    var ctx = document.getElementById("report-pie-chart");
    var myPieChart = new Chart(ctx, {
	type: 'pie',
	data: {
	    labels: ["Nulo", "Bajo", "Medio", "Alto"],
	    datasets: [{
		data: [report.qty_of_responses_of_each_risk['0.0'],
		       report.qty_of_responses_of_each_risk['0.3'],
		       report.qty_of_responses_of_each_risk['0.6'],
		       report.qty_of_responses_of_each_risk['1.0']],
		backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745'],
	    }],
	},
    });
}
