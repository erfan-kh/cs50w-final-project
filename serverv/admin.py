# Import the required modules
from django.contrib import admin  # Django's admin module
# The User and sensor_data models from the current app
from .models import User, sensor_data

# Register your models here

# Register the User model with the admin site
# This allows you to manage User objects in the Django admin site
admin.site.register(User)

# Register the sensor_data model with the admin site
# This allows you to manage sensor_data objects in the Django admin site
admin.site.register(sensor_data)
