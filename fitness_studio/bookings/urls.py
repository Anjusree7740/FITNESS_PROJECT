from django.urls import path
from . import views

urlpatterns = [
    path('classes/', views.FitnessClassListView.as_view(), name='classes-list'),
    path('book/', views.create_booking, name='create-booking'),
    path('bookings/', views.get_bookings_by_email, name='bookings-by-email'),
    path('bookings/<int:booking_id>/', views.get_booking_detail, name='booking-detail'),
]