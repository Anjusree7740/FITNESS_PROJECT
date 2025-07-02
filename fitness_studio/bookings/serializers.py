
from rest_framework import serializers
from django.utils import timezone
from .models import FitnessClass, Booking
import pytz
import logging

logger = logging.getLogger(__name__)


class FitnessClassSerializer(serializers.ModelSerializer):
    
    datetime_ist = serializers.SerializerMethodField()
    class_type = serializers.CharField(source='get_name_display', read_only=True)
    is_full = serializers.ReadOnlyField()
    is_upcoming = serializers.ReadOnlyField()
    
    class Meta:
        model = FitnessClass
        fields = [
            'id',
            'name',
            'class_type',
            'description',
            'instructor',
            'datetime',
            'datetime_ist',
            'duration_minutes',
            'total_slots',
            'available_slots',
            'is_full',
            'is_upcoming',
            'created_at'
        ]
        read_only_fields = ['id', 'available_slots', 'created_at']
    
    def get_datetime_ist(self, obj):
        if obj.datetime:
            ist = pytz.timezone('Asia/Kolkata')
            return obj.datetime.astimezone(ist).isoformat()
        return None
    
    def validate_datetime(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Class datetime must be in the future.")
        return value
    
    def validate(self, data):
        if 'total_slots' in data and 'available_slots' in data:
            if data['available_slots'] > data['total_slots']:
                raise serializers.ValidationError(
                    "Available slots cannot exceed total slots."
                )
        return data


class BookingCreateSerializer(serializers.ModelSerializer):
    
    class_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Booking
        fields = ['class_id', 'client_name', 'client_email', 'notes']
    
    def validate_class_id(self, value):
        try:
            fitness_class = FitnessClass.objects.get(id=value)
        except FitnessClass.DoesNotExist:
            raise serializers.ValidationError("Fitness class not found.")
        
        if not fitness_class.is_upcoming:
            raise serializers.ValidationError("Cannot book past classes.")
        
        if fitness_class.is_full:
            raise serializers.ValidationError("Class is fully booked.")
        
        return value
    
    def validate_client_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Client name cannot be empty.")
        return value.strip()
    
    def validate_client_email(self, value):
        return value.lower().strip()
    
    def validate(self, data):
        fitness_class = FitnessClass.objects.get(id=data['class_id'])
        client_email = data['client_email'].lower().strip()
        
        # Check if user already has a booking for this class
        if Booking.objects.filter(
            fitness_class=fitness_class,
            client_email=client_email,
            is_active=True
        ).exists():
            raise serializers.ValidationError(
                "You already have a booking for this class."
            )
        
        return data
    
    def create(self, validated_data):
        class_id = validated_data.pop('class_id')
        fitness_class = FitnessClass.objects.get(id=class_id)
        
        if not fitness_class.book_slot():
            raise serializers.ValidationError("Class is fully booked.")
        
        # Create the booking
        booking = Booking.objects.create(
            fitness_class=fitness_class,
            **validated_data
        )
        
        logger.info(f"Booking created successfully: {booking}")
        return booking


class BookingListSerializer(serializers.ModelSerializer):
    
    class_name = serializers.CharField(source='fitness_class.get_name_display', read_only=True)
    class_instructor = serializers.CharField(source='fitness_class.instructor', read_only=True)
    class_datetime_ist = serializers.SerializerMethodField()
    class_duration = serializers.IntegerField(source='fitness_class.duration_minutes', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id',
            'class_name',
            'class_instructor',
            'class_datetime_ist',
            'class_duration',
            'client_name',
            'client_email',
            'booking_time',
            'is_active',
            'notes'
        ]
    
    def get_class_datetime_ist(self, obj):
        if obj.fitness_class.datetime:
            ist = pytz.timezone('Asia/Kolkata')
            return obj.fitness_class.datetime.astimezone(ist).isoformat()
        return None


class BookingDetailSerializer(serializers.ModelSerializer):
  
    fitness_class = FitnessClassSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id',
            'fitness_class',
            'client_name',
            'client_email',
            'booking_time',
            'is_active',
            'notes'
        ]