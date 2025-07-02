from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from .models import FitnessClass, Booking
from .serializers import (
    FitnessClassSerializer,
    BookingCreateSerializer,
    BookingListSerializer,
    BookingDetailSerializer
)
import logging

logger = logging.getLogger(__name__)


class FitnessClassListView(generics.ListAPIView):
   
    serializer_class = FitnessClassSerializer
    
    def get_queryset(self):
        return FitnessClass.objects.filter(
            datetime__gt=timezone.now()
        ).order_by('datetime')
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            
            logger.info(f"Classes list requested. Found {len(serializer.data)} upcoming classes.")
            
            return Response({
                'status': 'success',
                'message': f'Found {len(serializer.data)} upcoming classes',
                'count': len(serializer.data),
                'data': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error fetching classes: {str(e)}")
            return Response({
                'status': 'error',
                'message': 'Failed to fetch classes',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_booking(request):
   
    try:
        with transaction.atomic():  
            serializer = BookingCreateSerializer(data=request.data)
            
            if serializer.is_valid():
                booking = serializer.save()
                
                response_serializer = BookingDetailSerializer(booking)
                
                logger.info(f"Booking created successfully for {booking.client_email}")
                
                return Response({
                    'status': 'success',
                    'message': 'Booking created successfully',
                    'data': response_serializer.data
                }, status=status.HTTP_201_CREATED)
            
            else:
                logger.warning(f"Invalid booking data: {serializer.errors}")
                return Response({
                    'status': 'error',
                    'message': 'Invalid data provided',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
    except Exception as e:
        logger.error(f"Error creating booking: {str(e)}")
        return Response({
            'status': 'error',
            'message': 'Failed to create booking',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_bookings_by_email(request):
    
    try:
        email = request.query_params.get('email')
        
        if not email:
            return Response({
                'status': 'error',
                'message': 'Email parameter is required',
                'example': '/api/bookings?email=user@example.com'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = email.lower().strip()
        
        bookings = Booking.objects.filter(
            client_email=email,
            is_active=True
        ).select_related('fitness_class').order_by('-booking_time')
        
        serializer = BookingListSerializer(bookings, many=True)
        
        logger.info(f"Bookings requested for email: {email}. Found {len(bookings)} bookings.")
        
        return Response({
            'status': 'success',
            'message': f'Found {len(bookings)} bookings for {email}',
            'email': email,
            'count': len(bookings),
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error fetching bookings: {str(e)}")
        return Response({
            'status': 'error',
            'message': 'Failed to fetch bookings',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_booking_detail(request, booking_id):
    
    try:
        booking = get_object_or_404(Booking, id=booking_id, is_active=True)
        serializer = BookingDetailSerializer(booking)
        
        logger.info(f"Booking detail requested for ID: {booking_id}")
        
        return Response({
            'status': 'success',
            'message': 'Booking details retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error fetching booking detail: {str(e)}")
        return Response({
            'status': 'error',
            'message': 'Failed to fetch booking details',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




