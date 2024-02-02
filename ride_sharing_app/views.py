
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from ride_sharing_app.models import Ride 
from .serializers import RideSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    
    @action(detail=True, methods=['post'])
    def accept_ride_request(self, request, pk):
        ride = self.get_object()

        if ride.status == Ride.REQUESTED:
            driver = User.objects.filter(is_driver=True, is_available=True).first()

            if driver:
                ride.driver = driver
                ride.status = Ride.ACCEPTED
                ride.save()

                self.notify_ride_status(ride)

                serializer = RideSerializer(ride)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No available drivers at the moment'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Ride is not in a request state'}, status=status.HTTP_400_BAD_REQUEST)
        
    @async_to_sync
    async def notify_ride_status(self, ride):
        channel_layer = get_channel_layer()
        await channel_layer.group_add(f"ride_{ride.id}", self.channel_name)

        await channel_layer.group_send(
            f"ride_{ride.id}",
            {"type": "update_location", "location": ride.status},
    )

    

        


    @action(detail=True, methods=['patch'])
    def update_current_location(self, request, pk):
        ride = self.get_object()
        current_location = request.data.get('current_location', None)
        
        if current_location is not None:
            ride.current_location = current_location
            ride.save()
            serializer = RideSerializer(ride)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Current location cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        
          
    def perform_create(self, serializer):
        serializer.save(rider=self.request.user, status=Ride.REQUESTED)
        
    

    @action(detail=False, methods=['post'])
    def request_ride(self, request):
        serializer = RideSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def ride_details(self, request, pk):
        ride = self.get_object()
        serializer = RideSerializer(ride)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def list_rides(self, request):
        rides = Ride.objects.all()
        serializer = RideSerializer(rides, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


    @action(detail=True, methods=['patch'])
    def cancel_ride(self, request, pk):
        ride = self.get_object()
        ride.status = Ride.CANCELLED
        ride.save()
        serializer = RideSerializer(ride)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['patch'])
    def accept_ride(self, request, pk):
        ride = self.get_object()
        ride.status = Ride.ACCEPTED
        ride.save()
        serializer = RideSerializer(ride)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def start_ride(self, request, pk):
        ride = self.get_object()
        ride.status = Ride.STARTED
        ride.save()

        self.notify_ride_status(ride)

        serializer = RideSerializer(ride)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def complete_ride(self, request, pk):
        ride = self.get_object()
        ride.status = Ride.COMPLETED
        ride.save()

        self.notify_ride_status(ride)

        serializer = RideSerializer(ride)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @async_to_sync
    async def notify_ride_status(self, ride):
        channel_layer = get_channel_layer()
        await channel_layer.group_add(f"ride_{ride.id}", self.channel_name)

        await channel_layer.group_send(
            f"ride_{ride.id}",
            {"type": "update_location", "location": "Current ride location"},
        )