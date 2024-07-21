from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from datetime import datetime, date, time


# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Transport(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Trip(models.Model):
    start = models.ForeignKey(
        Location, related_name='trips_starting', on_delete=models.CASCADE)
    end = models.ForeignKey(
        Location, related_name='trips_ending', on_delete=models.CASCADE)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    fare = models.IntegerField(validators=[MinValueValidator(1)])
    date = models.DateField()
    time = models.TimeField()
    admin = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='admin', default=None)

    def is_future_datetime(self):
        now = timezone.now()
        trip_datetime = timezone.make_aware(
            datetime.combine(self.date, self.time))
        return trip_datetime > now

    def save(self, *args, **kwargs):
        if not isinstance(self.date, date):
            self.date = datetime.strptime(self.date, '%Y-%m-%d').date()

        if not isinstance(self.time, time):
            self.time = datetime.strptime(self.time, '%H:%M').time()

        if not self.is_future_datetime():
            raise ValueError("Trip date and time must be in the future.")

        if self.admin is None:
            self.admin = self.created_by
        super().save(*args, **kwargs)

    def assign_admin(self, new_admin):
        self.admin = new_admin
        self.save()

    def __str__(self):
        return '-'.join([self.start.name, self.end.name, str(self.time)])


class Participant(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Request(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
