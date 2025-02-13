from django.contrib import admin
from django.urls import path
from movieapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),

   # User authentication URLs
    path('register/', views.register, name='register'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='authentication/logout.html'), name='logout'),


    # Movie URLs
    path('movies/', views.MovieListView.as_view(), name='movie_list'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    
    # Theater URLs
    path('theaters/', views.TheaterListView.as_view(), name='theater_list'),
    
    # Schedule URLs
    path('schedules/', views.ScheduleListView.as_view(), name='schedule_list'),
    
    # Booking URLs
    path('book/<int:schedule_id>/', views.book_movie, name='book_movie'),
    path('booking/<int:pk>/', views.BookingDetailView.as_view(), name='booking_detail'),
    path('bookings/', views.booking_list, name='booking_list'), 
    
    # Payment URLs
    path('payment/', views.PaymentCreateView.as_view(), name='payment_create'),
]

