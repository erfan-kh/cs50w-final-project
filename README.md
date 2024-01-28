Distinctiveness and Complexity :

about 2 years ago I started CS50 Courses to learn computer science and programming so I could connect my electronic circuits and processors to computers and switch heavy processes to them!
In this way, I don't need to buy and config professional processors, displays, storage, etc to manage and handle my projects, because I already have them on smartphones and laptops.
now I just need a simple processor and additional sensors, that's it, every sensor's data will be sent to a server that is running on a laptop or PC and doing heavy processes on those data and giving back a simple response to the processor!
In this project, I'm building a real-time water tank level monitoring, I put an ultrasonic sensor inside my water tank, and this sensor will get the distance between itself and water and send data to the processor, it's a NodeMCU ESP8266, this will doing a simple process on sensor's data and convert it to distance ( centimeter ), and make it online and waiting to requests from Django server.
now, Django sends requests to the processor and gives back the sensor's data and the processor's built-in LED status. The user can change the LED Built-in Status.
Users can see those data on the main page, also the data of each user will be saved separately in the database and they can have access to data on their own profile page, also users can get charts of those data day by day or full days. simplified of what I wrote is: "IOT ( internet of things )"
To develop it we can add more ultrasonic sensors to add more water tanks, so each user can visit only their own water tanks or add an operator to control all of the water tanks,  and add temperature sensors to those water tanks, so we can set another operator to get temperature of that water tanks to control them and so on!
to run it you just need to assign your ssid + password of WiFi to NodeMCU ESP8266 and give it +5V then running Django project.
---------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------
1_ ESP Code Folder : 
You can find my codes to config my NodeMCU ESP8266 and ultrasonic sensor, The programming language is "C"
---------------------------------------------------------------------------------------------------------------------------------
Along these lines I'm setting up my network :
```c
const char* ssid = "Barana";
const char* password = "91001398";
WiFiServer server(80); 
Serial.begin(115200);
IPAddress ip(192, 168, 1, 100); 
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);
WiFi.config(ip, gateway, subnet);
WiFi.begin(ssid, password);
```
---------------------------------------------------------------------------------------------------------------------------------
at this line I'm setting up my ultrasonic sensor :
```c
#define MAX_DISTANCE 400
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);
Ultrasonic = sonar.ping_cm();
```
---------------------------------------------------------------------------------------------------------------------------------
then we start a loop, at this loop, we are waiting for a client to connect esp8266 as a server :
```c
  while(!client.available()){
    delay(1);
  }
```
---------------------------------------------------------------------------------------------------------------------------------
then we check the client request, according to a user request, we give back the response:
```c
String request = client.readStringUntil('\r');
client.flush();
 if (request.indexOf("/LED=OFF") != -1)  {
//response
}
 if (request.indexOf("/LED=ON") != -1)  {
//response
}
 if (request.indexOf("/send") != -1)  
{
//response
}
```
---------------------------------------------------------------------------------------------------------------------------------
at this line, we are responding to client requests by standard HTPP requests format :
```c
client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println(""); 
    client.println("<!DOCTYPE HTML>");
    client.println("<html>");
    client.println("LED OFF");
    client.println("Value: " + String(value)); 
    client.println("Ultrasonic: " + String(Ultrasonic));
    client.println("</html>");
```
---------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------
2_ serverv Folder :
there are Django files, at views.py we are setting up NodeMCU ESP8266 IP addresses by these lines :
```python
LED_ON = 'http://192.168.1.100/LED=ON'
LED_OFF = 'http://192.168.1.100/LED=OFF'
SEND_VALUE = 'http://192.168.1.100/send'
```
---------------------------------------------------------------------------------------------------------------------------------
by this function we are rendering the home page, there is a Javascript AJAX function to send requests to NodeMCU ESP8266 and get responses, this AJAX is calling every second ( you can find it at serverv -> static -> js -> main.js ):
```python
def index(request):
    return render(request, "tmp.html")

    function getStatus() {
        $.ajax({
            url: '/sensor/',
            type: 'GET',
            success: function(response) {
                    $('#mysens').text("Sensor Value is : " + response.Ultrasonic);
                    $('#lvl').text(response.Ultrasonic + "%");
                    if (response.value == 1) {
                        $('#myImage').attr('src', "/static/lamp-on.png");                      $('#myledstatus').text("LED Status is : On");
                    } else {
                        $('#myImage').attr('src', "/static/lamp-off.png");                       $('#myledstatus').text("LED Status is : Off");       
                }             displayBatteryLevel(response.Ultrasonic);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log("AJAX call failed: " + textStatus + ", " + errorThrown);
            }
        });
}   
$("#status").click(getStatus);
setInterval(getStatus, 1000); 
```
---------------------------------------------------------------------------------------------------------------------------------
then we have a `chart` function who doing a query to the database and gives back the user's  data, making arrays of those data and sending them to an HTML page, there is a javascript function that takes this data and draws charts by them ( you can find Javascript function at serverv -> static -> js -> chart.js ) :
```python
def chart(request, user_id):
    user = User.objects.get(pk=user_id)
    allPost = sensor_data.objects.filter(user=user).order_by("id").reverse()
    years, months, days, hours, minutes, seconds, values = [], [], [], [], [], [], []
    for post in allPost:
        years.append(post.date.year)
        months.append(post.date.month)
        days.append(post.date.day)
        hours.append(post.date.hour)
        minutes.append(post.date.minute)
        seconds.append(post.date.second)
        values.append(post.content)
    return render(request, "chart.html", {
        "years": years,
        "months": months,
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
        "sensorValues": values,
    })
function chart(years, months, days, hours, minutes, seconds, sensorValues) {  
    labels = years.map(function(_, i) {
        return new Date(years[i], months[i] - 1, days[i], hours[i] + 3, minutes[i] + 30, seconds[i]);
    });
    dataset = sensorValues;
     the HTML canvas element with id 'myChart'
    var ctx = document.getElementById('myChart').getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Sensor Value',
                data: dataset,
                fill: true,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: document.getElementById('timeUnit').value
                    },
                }
            }
        }
    });
}
```
---------------------------------------------------------------------------------------------------------------------------------
then you can see the `Turn_on` Function, at this function, we send HTTP requests to NodeMCU ESP8266 and analyze responses, after we clean up the response, we save it to the database  :
```python
def Turn_on(request):
    try:
        response = requests.get(LED_ON)
        if response.status_code == 200:
            value = response.text.split("Value: ")[1]
            value = value.replace("</html>", "")
            value = value[:-20]
            Ultrasonic = response.text.split("Ultrasonic: ")[1]
            Ultrasonic = Ultrasonic.replace("</html>", "")
            Ultrasonic = Ultrasonic[:-3]
            user = User.objects.get(pk=request.user.id)
            post = sensor_data(content=Ultrasonic, user=user)
            post.save()
            return JsonResponse({'status': 'success', 'value': value, 'Ultrasonic': Ultrasonic})
        else:
            return JsonResponse({'status': 'failed', 'error': 'Could not reach Arduino'})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'status': 'failed', 'error': str(e)})
```
---------------------------------------------------------------------------------------------------------------------------------
now you can see `Turn_off`, `sensor` and `send_value` functions, we are doin same as we did at `Turn_on` Function.
at the `profile` function, we are doing a query to the database and getting back the user's data to show them, finally, you can see the `login`, `log out`, and `register` functions.
---------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------
3_serverv ->  static -> js Folder :
There are 2 JavaScript files, chart.js is for drawing charts, as we explained before. main.js has a `displayBatteryLevel` function, function draws a battery shape at the main HTML page to show the water tank level :
```javascript
function displayBatteryLevel(level) {
            level = Math.max(0, Math.min(100, level));
            sens = level;

            var heightPercentage = level + '%';

            var levelElement = document.getElementById('level');

            levelElement.style.height = heightPercentage;
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

        var batteryLevel = sens; // Replace YOUR_DYNAMIC_VALUE with your actual value

        window.onload = function() {
            displayBatteryLevel(batteryLevel);
}
```
---------------------------------------------------------------------------------------------------------------------------------
you can see two AJAX functions for changing LED Built-in status to On and Off :
```javascript
$(document).ready(function() {
            $("#on").click(function() {
                $.ajax({
                    url: '/Turn_on/',
                    type: 'get', 
                    success: function(response) {
                        displayBatteryLevel(response.Ultrasonic);
response.Ultrasonic
                    $('#mysens').text("Sensor Value is : " + response.Ultrasonic);
                    $('#myImage').attr('src', "/static/lamp-on.png");
                    $('#myledstatus').text("LED Status is : On");
                    
            }
        });
    });
});

$(document).ready(function() {
$("#off").click(function() {
    $.ajax({
        url: '/Turn_off/', 
        type: 'get',  
        success: function(response) {
                    $('#mysens').text("Sensor Value is : " + response.Ultrasonic);
                    $('#myImage').attr('src', "/static/lamp-off.png");
                    $('#myledstatus').text("LED Status is : Off");

            displayBatteryLevel(response.Ultrasonic);
             }
         });
    });
});
```
---------------------------------------------------------------------------------------------------------------------------------
at chart.js we have an `updateChart` function to set a filter on the chart based on dates, this function is getting help from `isValidDate`, and `filterBySpecificDay` functions :
```javascript
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

function isValidDate(dateString) {
    var regEx = /^\d{2}\/\d{2}\/\d{4}$/;
    if(!dateString.match(regEx)) return false;  
    var parts = dateString.split("/");
    var month = parseInt(parts[0], 10);
    var day = parseInt(parts[1], 10);
    var year = parseInt(parts[2], 10);
    if(year < 1000 || year > 3000 || month == 0 || month > 12) return false;
    var monthLength = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ];
    if(year%400 == 0 || (year%100 != 0 && year%4 == 0)) monthLength[1] = 29;
    return day > 0 && day <= monthLength[month - 1];
}

$(document).ready(function() {
    $("#specificDay").datepicker({
        dateFormat: "mm/dd/yy"
    });
});
data by a specific day
function filterBySpecificDay(specificDay) {
    if (typeof labels === 'undefined') {
        return { labels: [], dataset: [] };
    }

    var specificDate = new Date(specificDay);

    var filteredLabels = labels.filter(function(label, index) {
        return label.getFullYear() === specificDate.getFullYear() &&
               label.getMonth() === specificDate.getMonth() &&
               label.getDate() === specificDate.getDate();
    });

    var filteredDataset = dataset.filter(function(data, index) {
        var label = labels[index];
        return label.getFullYear() === specificDate.getFullYear() &&
               label.getMonth() === specificDate.getMonth() &&
               label.getDate() === specificDate.getDate();
    });

    return { labels: filteredLabels, dataset: filteredDataset };
}
```
---------------------------------------------------------------------------------------------------------------------------------