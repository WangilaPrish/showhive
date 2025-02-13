from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from movieapp.forms import CustomAuthenticationForm
from .models import Movie, Theater, Schedule, Booking, Payment
from django.contrib.auth import get_user_model

User = get_user_model() 

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
          
            messages.success(request, f'Account created for {email}! Please log in.')
            return redirect('login')  # Redirect to the login page
    else:
        form = UserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    authentication_form = CustomAuthenticationForm
    model = get_user_model()

    def form_invalid(self, form):
        # Check if the email exists in the database
        email = form.data.get('username')  # The email entered by the user
        if not User.objects.filter(username=email).exists():
            messages.error(self.request, "Email not found. Please register.")
        else:
            messages.error(self.request, "Incorrect password. Please try again.")
        return super().form_invalid(form)
        


def index(request):
    # Fetch featured movies (e.g., first 5 movies)
    featured_movies = Movie.objects.all()[:5]  # First 5 featured movies
    movies = Movie.objects.all()
    top_rated_movies = Movie.objects.order_by('-rating')[:8]  # Top 8 rated movies

    genres = Movie.objects.values_list('genre', flat=True).distinct()

    context = {
        'featured_movies': featured_movies,
        'movies': movies,
        'top_rated_movies': top_rated_movies,
        'genres': genres,
    }
    
    return render(request, 'movie_booking/index.html', context)

# --- Movie Views ---
class MovieListView(ListView):
    model = Movie
    template_name = 'movie_booking/movie_list.html'
    context_object_name = 'movies'


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie_booking/movie_detail.html'
    context_object_name = 'movie'


# --- Theater Views ---
class TheaterListView(ListView):
    model = Theater
    template_name = 'movie_booking/theater_list.html'
    context_object_name = 'theaters'


# --- Schedule Views ---
class ScheduleListView(ListView):
    model = Schedule
    template_name = 'movie_booking/schedule_list.html'
    context_object_name = 'schedules'


# --- Booking Views ---
@login_required
def book_movie(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    theater_capacity = schedule.theater.seating_capacity
    booked_seats = schedule.get_booked_seats()
    available_seats = [f"R{row}C{col}" for row in range(1, 6) for col in range(1, theater_capacity // 5 + 1)]
    available_seats = list(set(available_seats) - set(booked_seats))  # Filter out booked seats

    if request.method == "POST":
        selected_seats = request.POST.getlist('seats')
        number_of_tickets = len(selected_seats)
        if not selected_seats:
            messages.error(request, "Please select at least one seat.")
            return redirect('book_movie', schedule_id=schedule_id)
        
        # Create booking
        booking = Booking.objects.create(
            user=request.user,
            schedule=schedule,
            number_of_tickets=number_of_tickets,
            seat_numbers=selected_seats,
            total_cost=number_of_tickets * 10.00  # Example ticket price
        )
        messages.success(request, "Booking successful!")
        return redirect('booking_detail', booking_id=booking.id)

    return render(request, 'movie_booking/book_movie.html', {
        'schedule': schedule,
        'available_seats': available_seats,
        'booked_seats': booked_seats,
    })


class BookingDetailView(DetailView):
    model = Booking
    template_name = 'movie_booking/booking_detail.html'
    context_object_name = 'booking'

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'movie_booking/booking_list.html', {'bookings': bookings})


# --- Payment Views ---
class PaymentCreateView(CreateView):
    model = Payment
    template_name = 'movie_booking/payment_form.html'
    fields = ['amount', 'payment_method', 'status']
    success_url = reverse_lazy('payment_success')


def payment_success(request):
    return render(request, 'movie_booking/payment_success.html', {
        'message': "Your payment was successful!",
    })