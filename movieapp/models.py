from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Add custom fields here if needed
    pass

# Movie Model
class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=100)
    duration = models.DurationField()  # For storing time in HH:MM:SS format
    release_date = models.DateField()
    image = models.ImageField(upload_to='movies/images/')  # Requires Pillow library
    trailer_link = models.URLField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    def __str__(self):
        return self.title

# Theater Model
class Theater(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    seating_capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

# Schedule Model
class Schedule(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='schedules')
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='schedules')
    show_time = models.TimeField()
    date = models.DateField()

    def get_booked_seats(self):
        # Aggregate all seat numbers from bookings for this schedule
        booked_seats = Booking.objects.filter(schedule=self).values_list('seat_numbers', flat=True)
        all_booked_seats = [seat for seats in booked_seats for seat in seats]  # Flatten list
        return all_booked_seats


# Booking Model
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='bookings')
    number_of_tickets = models.PositiveIntegerField()
    seat_numbers = models.JSONField()  # Store seat numbers as a list (requires PostgreSQL or Django 3.1+)
    booking_date = models.DateTimeField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.schedule}"

# Payment Model
class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('PayPal', 'PayPal'),
        ('Mobile Money', 'Mobile Money'),
    ])
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ])
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Booking ID {self.booking.id} - {self.status}"