var sens;
function displayBatteryLevel(level) {
            // Ensure the battery level is between 0 and 100
            level = Math.max(0, Math.min(100, level));
            sens = level;
            // Calculate the height percentage
            var heightPercentage = level + '%';

            // Get the level element
            var levelElement = document.getElementById('level');

            // Set the height of the level element
            levelElement.style.height = heightPercentage;

            // Change the color based on the battery level
            if (level > 80) {
                levelElement.style.backgroundColor = '#090'; // Lime green
            } else if (level > 60) {
                levelElement.style.backgroundColor = '#0F0'; // Green
            } else if (level > 40) {
                levelElement.style.backgroundColor = '#FF0'; // Yellow
            } else if (level > 20) {
                levelElement.style.backgroundColor = '#FFA500'; // Orange
            } else if (level > 10) {
                levelElement.style.backgroundColor = '#FF4500'; // OrangeRed
            } else {
                levelElement.style.backgroundColor = '#F00'; // Red
            }
}

        // Set the battery level with your dynamic value
        var batteryLevel = sens; // Replace YOUR_DYNAMIC_VALUE with your actual value

        // Ensure the function is not called until the entire page is loaded
        window.onload = function() {
            displayBatteryLevel(batteryLevel);
}




$(document).ready(function() {
            $("#on").click(function() {
                $.ajax({
                    url: '/Turn_on/',  // Django view function url
                    type: 'get',  // or 'post'
                    success: function(response) {


                    // Change the text of the span element to response.Ultrasonic
                    $('#mysens').text("Sensor Value is : " + response.Ultrasonic);
                    // Change the image based on response.value
                    $('#myImage').attr('src', "/static/lamp-on.png");
                    $('#myledstatus').text("LED Status is : On");
                displayBatteryLevel(response.Ultrasonic);
                    
            }
        });
    });
});

$(document).ready(function() {
$("#off").click(function() {
    $.ajax({
        url: '/Turn_off/',  // Django view function url
        type: 'get',  // or 'post'
        success: function(response) {
            // Change the text of the span element to response.Ultrasonic

                    $('#mysens').text("Sensor Value is : " + response.Ultrasonic);
                    // Change the image based on response.value
                    $('#myImage').attr('src', "/static/lamp-off.png");
                    $('#myledstatus').text("LED Status is : Off");

            displayBatteryLevel(response.Ultrasonic);
             }
         });
});
});


    function getStatus() {
        $.ajax({
            url: '/sensor/',  // Django view function url
            type: 'GET',
            success: function(response) {
                // Change the text of the span element to response.Ultrasonic
                    $('#mysens').text("Sensor Value is : " + response.Ultrasonic);
                    $('#lvl').text(response.Ultrasonic + "%");
                    
                // Change the image based on response.value

                    if (response.value == 1) {
                        $('#myImage').attr('src', "/static/lamp-on.png");
                        $('#myledstatus').text("LED Status is : On");
                    };
                    if (response.value == 0) {
                        $('#myImage').attr('src', "/static/lamp-off.png");
                        $('#myledstatus').text("LED Status is : Off");
                        
                    };
                displayBatteryLevel(response.Ultrasonic);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log("AJAX call failed: " + textStatus + ", " + errorThrown);
            }
        });
}
    
$("#status").click(getStatus);


// Call the function every second
setInterval(getStatus, 1000);  // 1000 milliseconds = 1 second



