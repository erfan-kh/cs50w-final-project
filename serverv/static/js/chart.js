// Declare the chart, labels, and dataset variables outside the function so they can be accessed elsewhere
var chart, labels, dataset;

// Define a function named 'chart' that takes in several parameters
function chart(years, months, days, hours, minutes, seconds, sensorValues) {  
    // Format your data for Chart.js:
    // Create an array of Date objects using the provided date components
    labels = years.map(function(_, i) {
        return new Date(years[i], months[i] - 1, days[i], hours[i] + 3, minutes[i] + 30, seconds[i]);
    });
    // Assign the sensorValues array to the 'dataset' variable
    dataset = sensorValues;
    
    // Create your chart:
    // Get the 2D rendering context for the HTML canvas element with id 'myChart'
    var ctx = document.getElementById('myChart').getContext('2d');
    // Create a new Chart.js line chart on the canvas
    chart = new Chart(ctx, {
        type: 'line',  // Specify the chart type
        data: {  // Specify the data for the chart
            labels: labels,  // Use the 'labels' array for the x-axis labels
            datasets: [{  // Define a single dataset for the chart
                label: 'Sensor Value',  // Label for the dataset
                data: dataset,  // Data for the dataset
                fill: true,  // Don't fill the area under the line
                borderColor: 'rgb(75, 192, 192)',  // Color of the line
                tension: 0.1  // Bezier curve tension for the line
            }]
        },
        options: {  // Specify options for the chart
            scales: {  // Define scales for the chart
                x: {  // Options for the x-axis
                    type: 'time',  // Use a time scale for the x-axis
                    time: {  // Options for the time scale
                        unit: document.getElementById('timeUnit').value  // Use the selected time unit
                    },
                }
            }
        }
    });
}

// Function to update the chart based on a specific day
function updateChart() {
    var specificDay = document.getElementById('specificDay').value;
    if (isValidDate(specificDay)) {
        chart.options.scales.x.time.unit = document.getElementById('timeUnit').value;
        var filteredData = filterBySpecificDay(specificDay);
        chart.data.labels = filteredData.labels;
        chart.data.datasets[0].data = filteredData.dataset;
        chart.update();
    } else {
        alert("Please enter a valid date in the format mm/dd/yyyy");
    }
}

// Function to update the width of the div
function updateDivWidth() {
    document.getElementById('chartDiv').style.width = document.getElementById('divWidth').value;            
}

// Define a function to validate the date format
function isValidDate(dateString) {
    var regEx = /^\d{2}\/\d{2}\/\d{4}$/;
    if(!dateString.match(regEx)) return false;  // Invalid format
    var parts = dateString.split("/");
    var month = parseInt(parts[0], 10);
    var day = parseInt(parts[1], 10);
    var year = parseInt(parts[2], 10);
    if(year < 1000 || year > 3000 || month == 0 || month > 12) return false;
    var monthLength = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ];
    if(year%400 == 0 || (year%100 != 0 && year%4 == 0)) monthLength[1] = 29;
    return day > 0 && day <= monthLength[month - 1];
}

// Initialize the datepicker for the 'specificDay' input field when the document is ready
$(document).ready(function() {
    $("#specificDay").datepicker({
        dateFormat: "mm/dd/yy"
    });
});

// Define a function to filter the chart data by a specific day
function filterBySpecificDay(specificDay) {
    // Check if labels is defined
    if (typeof labels === 'undefined') {
        return { labels: [], dataset: [] };
    }

    // Convert the specificDay string to a Date object
    var specificDate = new Date(specificDay);

    // Filter your labels array by the selected day
    var filteredLabels = labels.filter(function(label, index) {
        return label.getFullYear() === specificDate.getFullYear() &&
               label.getMonth() === specificDate.getMonth() &&
               label.getDate() === specificDate.getDate();
    });

    // Filter your dataset array the same way
    var filteredDataset = dataset.filter(function(data, index) {
        var label = labels[index];
        return label.getFullYear() === specificDate.getFullYear() &&
               label.getMonth() === specificDate.getMonth() &&
               label.getDate() === specificDate.getDate();
    });

    return { labels: filteredLabels, dataset: filteredDataset };
}