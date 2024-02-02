from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    RIDER = 'rider'
    DRIVER = 'driver'
    USER_TYPE_CHOICES = [
        (RIDER, 'Rider'),
        (DRIVER, 'Driver'),
    ]

    user = models.CharField(max_length=255)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    dob = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username



class Ride(models.Model):
    REQUESTED = 'requested'
    STARTED = 'started'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    ACCEPTED = 'accepted'
    STATUS_CHOICES = [
        (REQUESTED, 'Requested'),
        (STARTED, 'Started'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
        (ACCEPTED, 'accepted'),
    ]
    current_location = models.TextField(blank=True, null=True)

    rider = models.ForeignKey(User, related_name='rides_as_rider', on_delete=models.CASCADE)
    driver = models.ForeignKey(User, related_name='rides_as_driver', null=True, blank=True, on_delete=models.SET_NULL)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=REQUESTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Ride {self.id} - {self.status}"
