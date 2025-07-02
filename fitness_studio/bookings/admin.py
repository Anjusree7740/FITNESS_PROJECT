
from django.contrib import admin
from .models import FitnessClass, Booking


@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
   
    list_display = [
        'name',
        'instructor',
        'datetime_ist_formatted',
        'available_slots',
        'total_slots',
        'is_full',
        'is_upcoming'
    ]
    list_filter = [
        'name',
        'instructor',
        'datetime',
        'created_at'
    ]
    search_fields = [
        'name',
        'instructor',
        'description'
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
        'is_full',
        'is_upcoming',
        'datetime_ist'
    ]
    fieldsets = (
        ('Class Information', {
            'fields': ('name', 'description', 'instructor')
        }),
        ('Schedule', {
            'fields': ('datetime', 'datetime_ist', 'duration_minutes')
        }),
        ('Capacity', {
            'fields': ('total_slots', 'available_slots')
        }),
        ('Status', {
            'fields': ('is_full', 'is_upcoming')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def datetime_ist_formatted(self, obj):
        return obj.datetime_ist.strftime('%Y-%m-%d %H:%M IST')
    datetime_ist_formatted.short_description = 'Date & Time (IST)'
    datetime_ist_formatted.admin_order_field = 'datetime'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
  
    list_display = [
        'client_name',
        'client_email',
        'fitness_class_name',
        'class_datetime_ist_formatted',
        'booking_time',
        'is_active'
    ]
    list_filter = [
        'is_active',
        'booking_time',
        'fitness_class__name',
        'fitness_class__instructor'
    ]
    search_fields = [
        'client_name',
        'client_email',
        'fitness_class__name',
        'fitness_class__instructor'
    ]
    readonly_fields = [
        'booking_time',
        'fitness_class_details'
    ]
    fieldsets = (
        ('Client Information', {
            'fields': ('client_name', 'client_email')
        }),
        ('Class Information', {
            'fields': ('fitness_class', 'fitness_class_details')
        }),
        ('Booking Details', {
            'fields': ('booking_time', 'is_active', 'notes')
        })
    )
    
    def fitness_class_name(self, obj):
        return obj.fitness_class.get_name_display()
    fitness_class_name.short_description = 'Class'
    fitness_class_name.admin_order_field = 'fitness_class__name'
    
    def class_datetime_ist_formatted(self, obj):
        return obj.class_datetime_ist.strftime('%Y-%m-%d %H:%M IST')
    class_datetime_ist_formatted.short_description = 'Class Date & Time'
    class_datetime_ist_formatted.admin_order_field = 'fitness_class__datetime'
    
    def fitness_class_details(self, obj):
        cls = obj.fitness_class
        return f"{cls.get_name_display()} with {cls.instructor} - {cls.datetime_ist.strftime('%Y-%m-%d %H:%M IST')}"
    fitness_class_details.short_description = 'Class Details'