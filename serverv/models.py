# Import the required modules
from django.db import models  # Django's database models module
from django.contrib.auth.models import AbstractUser  # Django's built-in user model
from django.utils import timezone  # Django's timezone utilities

# Define your models here

# User model that extends Django's built-in AbstractUser model


class User(AbstractUser):
    # The 'pass' keyword is used when you do not want to add any other properties or methods to the class.
    pass

# Sensor data model


class sensor_data(models.Model):
    # The content field stores the sensor data as a string. The maximum length of the string is 140 characters.
    content = models.CharField(max_length=140)

    # The user field is a foreign key to the User model. This creates a many-to-one relationship from sensor_data to User.
    # The related_name option allows you to access the sensor data of a user using 'author'.
    # The on_delete option specifies that when the referenced user is deleted, also delete the sensor data (CASCADE).
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author")

    # The date field stores the date and time of the sensor data. The default value is the current date and time.
    date = models.DateTimeField(default=timezone.now)

    # The __str__ method returns a string representation of the sensor data model.
    # It includes the id, user, and date of the sensor data.
    def __str__(self):
        return f"Post {self.id} made by {self.user} on {self.date.strftime('%d %b %Y %H:%M:%S')}"
