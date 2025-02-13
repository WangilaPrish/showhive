from django.contrib import admin
from .models import Movie, Theater, Schedule, Booking, Payment

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'release_date')
    search_fields = ('title', 'genre')

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'seating_capacity')
    search_fields = ('name', 'location')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('movie', 'theater', 'date', 'show_time')
    list_filter = ('date', 'theater')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'schedule', 'number_of_tickets', 'total_cost', 'booking_date')
    list_filter = ('booking_date',)
    search_fields = ('user__username',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'payment_method', 'status', 'payment_date')
    list_filter = ('status', 'payment_date')
