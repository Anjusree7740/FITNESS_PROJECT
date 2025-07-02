
from django.db import models
from django.core.validators import MinValueValidator, EmailValidator
from django.utils import timezone
import pytz
import logging

logger = logging.getLogger(__name__)


class FitnessClass(models.Model):
   
    CLASS_TYPES = [
        ('yoga', 'Yoga'),
        ('zumba', 'Zumba'),
        ('hiit', 'HIIT'),
        ('pilates', 'Pilates'),
        ('cardio', 'Cardio'),
        ('strength', 'Strength Training'),
    ]
    
    name = models.CharField(
        max_length=100,
        choices=CLASS_TYPES,
    )
    description = models.TextField(
        blank=True,
    )
    instructor = models.CharField(
        max_length=100,
    )
    datetime = models.DateTimeField(
    )
    duration_minutes = models.PositiveIntegerField(
        default=60,
        validators=[MinValueValidator(15)],
    )
    total_slots = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )
    available_slots = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['datetime']
        verbose_name = 'Fitness Class'
        verbose_name_plural = 'Fitness Classes'
    
    def __str__(self):
        return f"{self.get_name_display()} - {self.instructor} ({self.datetime_ist})"
    
    @property
    def datetime_ist(self):
        ist = pytz.timezone('Asia/Kolkata')
        return self.datetime.astimezone(ist)
    
    @property
    def is_full(self):
        return self.available_slots <= 0
    
    @property
    def is_upcoming(self):
        return self.datetime > timezone.now()
    
    def save(self, *args, **kwargs):
        if self.available_slots > self.total_slots:
            self.available_slots = self.total_slots
        super().save(*args, **kwargs)
        logger.info(f"FitnessClass saved: {self}")
    
    def book_slot(self):
        
        if self.available_slots > 0:
            self.available_slots -= 1
            self.save(update_fields=['available_slots', 'updated_at'])
            logger.info(f"Slot booked for class {self.id}. Available slots: {self.available_slots}")
            return True
        logger.warning(f"Attempted to book slot for full class {self.id}")
        return False
    
    

class Booking(models.Model):
    
    fitness_class = models.ForeignKey(
        FitnessClass,
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    client_name = models.CharField(
        max_length=100,
    )
    client_email = models.EmailField(
        validators=[EmailValidator()],
    )
    booking_time = models.DateTimeField(
        auto_now_add=True,
    )
    is_active = models.BooleanField(
        default=True,
    )
    notes = models.TextField(
        blank=True,
    )
    
    class Meta:
        ordering = ['-booking_time']
        unique_together = ['fitness_class', 'client_email']  
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
    
    def __str__(self):
        return f"{self.client_name} - {self.fitness_class}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            logger.info(f"New booking created: {self}")
    
    @property
    def class_datetime_ist(self):
        return self.fitness_class.datetime_ist