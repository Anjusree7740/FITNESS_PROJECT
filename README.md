Fitness Studio Booking API A simple REST API for booking fitness classes built with Django. This project allows clients to view available classes, make bookings, and check their reservations. What This API Does

View all upcoming fitness classes (Yoga, Zumba, HIIT, etc.) Book a spot in any available class Check your bookings using your email Prevents overbooking and validates all inputs Handles timezone properly (all times shown in IST)

What You Need

Python 3.8 or higher

Getting Started

Download and extract the project cd fitness_studio

Create a virtual environment python -m venv fitness_env source fitness_env/bin/activate

Install dependencies pip install -r requirements.txt

Set up the database python manage.py makemigrations python manage.py migrate

Load sample data (creates test classes and bookings) python manage.py load_sample_data --clear

Start the server python manage.py runserver

Your API will be running at http://localhost:8000/api/

Technologies Used

Django 4.2 - Web framework Django REST Framework - API framework SQLite - Database (for simplicity) Python timezone support - IST conversion

I will share postman collection along with the file
