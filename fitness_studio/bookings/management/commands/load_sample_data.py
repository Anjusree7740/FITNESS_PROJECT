from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from bookings.models import FitnessClass, Booking
import random


class Command(BaseCommand):
    help = 'Load sample fitness classes and bookings for testing'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before loading sample data',
        )
    
    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data')
            Booking.objects.all().delete()
            FitnessClass.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))
        
        self.stdout.write('Loading sample data')
        
        now = timezone.now()
        
        classes_data = [
            {
                'name': 'yoga',
                'instructor': 'Priya Sharma',
                'datetime': now + timedelta(days=1, hours=9),
                'total_slots': 15,
                'available_slots': 12,
                'description': 'Relaxing Hatha Yoga session for beginners and intermediate practitioners.'
            },
            {
                'name': 'yoga',
                'instructor': 'Amit Kumar',
                'datetime': now + timedelta(days=1, hours=18),
                'total_slots': 20,
                'available_slots': 15,
                'description': 'Evening Vinyasa flow yoga with focus on breathing and flexibility.'
            },
            {
                'name': 'zumba',
                'instructor': 'Maria Rodriguez',
                'datetime': now + timedelta(days=1, hours=10),
                'total_slots': 25,
                'available_slots': 20,
                'description': 'High-energy Zumba dance workout with Latin music.'
            },
            {
                'name': 'zumba',
                'instructor': 'Carlos Mendez',
                'datetime': now + timedelta(days=2, hours=19),
                'total_slots': 30,
                'available_slots': 25,
                'description': 'Fun and energetic Zumba party workout for all fitness levels.'
            },
            {
                'name': 'hiit',
                'instructor': 'Jake Thompson',
                'datetime': now + timedelta(days=2, hours=7),
                'total_slots': 12,
                'available_slots': 8,
                'description': 'Intense 45-minute HIIT workout focusing on strength and cardio.'
            },
            {
                'name': 'hiit',
                'instructor': 'Sarah Johnson',
                'datetime': now + timedelta(days=2, hours=17),
                'total_slots': 15,
                'available_slots': 10,
                'description': 'Full-body HIIT training with bodyweight exercises.'
            },
            {
                'name': 'pilates',
                'instructor': 'Emma Watson',
                'datetime': now + timedelta(days=3, hours=8),
                'total_slots': 10,
                'available_slots': 7,
                'description': 'Core-focused Pilates class emphasizing posture and flexibility.'
            },
            {
                'name': 'cardio',
                'instructor': 'Mike Davis',
                'datetime': now + timedelta(days=3, hours=16),
                'total_slots': 20,
                'available_slots': 18,
                'description': 'High-intensity cardio workout with various equipment.'
            },
            {
                'name': 'strength',
                'instructor': 'Rocky Balboa',
                'datetime': now + timedelta(days=4, hours=11),
                'total_slots': 8,
                'available_slots': 5,
                'description': 'Weight training session focusing on major muscle groups.'
            },
            {
                'name': 'yoga',
                'instructor': 'Anjali Patel',
                'datetime': now + timedelta(days=5, hours=19),
                'total_slots': 16,
                'available_slots': 16,
                'description': 'Weekend relaxation yoga with meditation and breathing exercises.'
            }
        ]
        
        created_classes = []
        for class_data in classes_data:
            fitness_class = FitnessClass.objects.create(**class_data)
            created_classes.append(fitness_class)
            self.stdout.write(f'Created class: {fitness_class}')
        
        sample_clients = [
            {'name': 'Rahul Gupta', 'email': 'rahul.gupta@email.com'},
            {'name': 'Sneha Reddy', 'email': 'sneha.reddy@email.com'},
            {'name': 'Arjun Singh', 'email': 'arjun.singh@email.com'},
            {'name': 'Kavya Nair', 'email': 'kavya.nair@email.com'},
            {'name': 'Rohan Sharma', 'email': 'rohan.sharma@email.com'},
            {'name': 'Ananya Das', 'email': 'ananya.das@email.com'},
            {'name': 'Vikram Malhotra', 'email': 'vikram.malhotra@email.com'},
            {'name': 'Deepika Agarwal', 'email': 'deepika.agarwal@email.com'},
        ]
        
        booking_count = 0
        for fitness_class in created_classes:
            booked_slots = fitness_class.total_slots - fitness_class.available_slots
            clients_to_book = random.sample(sample_clients, min(booked_slots, len(sample_clients)))
            
            for client in clients_to_book:
                try:
                    booking = Booking.objects.create(
                        fitness_class=fitness_class,
                        client_name=client['name'],
                        client_email=client['email'],
                        notes=f"Booking made via sample data for {fitness_class.get_name_display()} class"
                    )
                    booking_count += 1
                    self.stdout.write(f'Created booking: {booking}')
                except Exception as e:
                    pass
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded sample data:\n'
                f'- {len(created_classes)} fitness classes\n'
                f'- {booking_count} bookings'
            )
        )
        
        total_upcoming = FitnessClass.objects.filter(datetime__gt=timezone.now()).count()
        total_bookings = Booking.objects.filter(is_active=True).count()
        
        self.stdout.write(
            self.style.WARNING(
                f'\nCurrent stats:\n'
                f'- {total_upcoming} upcoming classes\n'
                f'- {total_bookings} active bookings'
            )
        )