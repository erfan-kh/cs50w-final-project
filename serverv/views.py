# Import necessary libraries
from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from .models import User, sensor_data
from django.http import JsonResponse
import requests


# Define constants for LED and sensor URLs
# These are the URLs to control the LED and send sensor data
LED_ON = 'http://192.168.1.100/LED=ON'
LED_OFF = 'http://192.168.1.100/LED=OFF'
SEND_VALUE = 'http://192.168.1.100/send'

# define height of water tank to calibrate Ultrasonic Sensor
MAX = 2
MIN = 13

Ultrasonic = 0
# Define the index view
# This view simply renders the "tmp.html" template


def index(request):

    return render(request, "tmp.html")

# Define the chart view
# This view gets the sensor data for a specific user and prepares it for rendering in a chart


def chart(request, user_id):
    # Get the user and their sensor data
    user = User.objects.get(pk=user_id)
    allPost = sensor_data.objects.filter(user=user).order_by("id").reverse()

    # Initialize lists to hold data
    years, months, days, hours, minutes, seconds, values = [], [], [], [], [], [], []
    for post in allPost:
        # Append data to lists
        years.append(post.date.year)
        months.append(post.date.month)
        days.append(post.date.day)
        hours.append(post.date.hour)
        minutes.append(post.date.minute)
        seconds.append(post.date.second)
        values.append(post.content)

    # Render the chart with the data
    return render(request, "chart.html", {
        "years": years,
        "months": months,
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
        "sensorValues": values,
    })

# Define the Turn_on view
# This view redirects to the LED_ON URL, effectively turning the LED on


def Turn_on(request):

    try:
        response = requests.get(LED_ON)
        if response.status_code == 200:
            # Extract the 'value' from the response text
            value = response.text.split("Value: ")[1]
            value = value.replace("</html>", "")
            value = value[:-20]

            Ultrasonic = response.text.split("Ultrasonic: ")[1]
            Ultrasonic = Ultrasonic.replace("</html>", "")
            Ultrasonic = Ultrasonic[:-3]

            Ultrasonic = int(Ultrasonic)

            Ultrasonic = int(((MIN - Ultrasonic) / (MIN - MAX)) * 100)

            if Ultrasonic > 100:
                Ultrasonic = 100
            if Ultrasonic < 0:
                Ultrasonic = 0

            user = User.objects.get(pk=request.user.id)
            post = sensor_data(content=Ultrasonic, user=user)
            post.save()

            return JsonResponse({'status': 'success', 'value': value, 'Ultrasonic': Ultrasonic})
        else:
            return JsonResponse({'status': 'failed', 'error': 'Could not reach Arduino'})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'status': 'failed', 'error': str(e)})

# Define the Turn_off view
# This view redirects to the LED_OFF URL, effectively turning the LED off


def Turn_off(request):
    try:
        response = requests.get(LED_OFF)
        if response.status_code == 200:
            # Extract the 'value' from the response text
            value = response.text.split("Value: ")[1]
            value = value.replace("</html>", "")
            value = value[:-20]

            Ultrasonic = response.text.split("Ultrasonic: ")[1]
            Ultrasonic = Ultrasonic.replace("</html>", "")
            Ultrasonic = Ultrasonic[:-3]

            Ultrasonic = int(Ultrasonic)

            Ultrasonic = int(((MIN - Ultrasonic) / (MIN - MAX)) * 100)

            if Ultrasonic > 100:
                Ultrasonic = 100
            if Ultrasonic < 0:
                Ultrasonic = 0

            user = User.objects.get(pk=request.user.id)
            post = sensor_data(content=Ultrasonic, user=user)
            post.save()

            return JsonResponse({'status': 'success', 'value': value, 'Ultrasonic': Ultrasonic})
        else:
            return JsonResponse({'status': 'failed', 'error': 'Could not reach Arduino'})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'status': 'failed', 'error': str(e)})


# Define the sensor view
# This view redirects to the SEND_VALUE URL, effectively sending the sensor value
def sensor(request):

    try:
        response = requests.get(SEND_VALUE)

        if response.status_code == 200:

            Ultrasonic = response.text.split("Ultrasonic: ")[1]
            Ultrasonic = Ultrasonic.replace("</html>", "")
            Ultrasonic = Ultrasonic[:-3]

            Ultrasonic = int(Ultrasonic)

            # Extract the 'value' from the response text
            value = response.text.split("Value: ")[1]
            value = value.replace("</html>", "")
            if Ultrasonic > 9:
                value = value[:-20]
            else:
                value = value[:-19]

            Ultrasonic = int(((MIN - Ultrasonic) / (MIN - MAX)) * 100)

            if Ultrasonic > 100:
                Ultrasonic = 100
            if Ultrasonic < 0:
                Ultrasonic = 0

            user = User.objects.get(pk=request.user.id)
            post = sensor_data(content=Ultrasonic, user=user)
            post.save()

            return JsonResponse({'status': 'success', 'value': value, 'Ultrasonic': Ultrasonic})
        else:

            return JsonResponse({'status': 'failed', 'error': 'Could not reach Arduino'})
    except requests.exceptions.RequestException as e:

        return JsonResponse({'status': 'failed', 'error': str(e)})


# Define the send_value view
# This view gets the values from the request, saves the sensor data, and renders the "tmp.html" template with the data
def send_value(request):
    # Get the values from the request
    value = request.GET.get('value', '')
    valuee = request.GET.get('valuee', '')
    status = "ON" if value == "1" else "OFF"

    # Get the user and save the sensor data
    user = User.objects.get(pk=request.user.id)
    post = sensor_data(content=Ultrasonic, user=user)
    post.save()

    # Render the template with the data
    return render(request, "tmp.html", {
        "value": valuee,
        "user": user,
        "status": status,
    })

# Define the profile view
# This view gets the sensor data for a specific user, paginates it, and renders the "profile.html" template with the data


def profile(request, user_id):

    # Get the user and their sensor data
    user = User.objects.get(pk=user_id)
    allPost = sensor_data.objects.filter(user=user).order_by("id").reverse()
    counter = allPost.count()

    # Initialize the paginator
    paginator = Paginator(allPost, 10)
    page_number = request.GET.get('page')

    if page_number == None:
        page_number = 1
    posts_of_the_page = paginator.get_page(page_number)

    # Get the total number of pages
    total_pages = paginator.num_pages

    # Render the profile with the data
    return render(request, "profile.html", {
        "allPosts": allPost,
        "posts_of_the_page": posts_of_the_page,
        "username": user.username,
        "user_profile": user,
        "counter": counter,
        "page_number": page_number,
        "total_pages": total_pages,
    })

# Define the login_view
# This view handles both the GET and POST requests for the login page


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return render(request, "tmp.html")
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")

# Define the logout_view
# This view logs the user out and redirects them to the index page


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Define the register view
# This view handles both the GET and POST requests for the registration page
def register(request):
    # If the request method is POST, then the user is trying to register
    if request.method == "POST":
        # Get the username, email, password, and confirmation from the request
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Ensure password matches confirmation
        # If the password and confirmation do not match, render the registration page with an error message
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        # If the username is already taken, render the registration page with an error message
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })

        # If the user was successfully created, log them in and render the "tmp.html" template
        login(request, user)
        return render(request, "tmp.html")
    # If the request method is not POST, then the user is trying to access the registration page
    else:
        return render(request, "register.html")
