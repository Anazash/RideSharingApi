# from django.test import TestCase
# from django.contrib.auth.models import User
# from rest_framework.test import APIClient
# from rest_framework import status
# from .models import Ride

# class RideModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='testpass')
#         self.ride = Ride.objects.create(
#             rider=self.user,
#             pickup_location='A',
#             dropoff_location='B'
#         )

#     def test_ride_creation(self):
#         self.assertEqual(str(self.ride), f"Ride {self.ride.id} - requested")

# class RideAPITest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(username='testuser', password='testpass')
#         self.ride_data = {
#             'rider': self.user.id,
#             'pickup_location': 'A',
#             'dropoff_location': 'B'
#         }

#     def test_create_ride(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.post('/rides/', self.ride_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_list_rides(self):
#         response = self.client.get('/rides/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_ride_details(self):
#         ride = Ride.objects.create(
#             rider=self.user,
#             pickup_location='A',
#             dropoff_location='B'
#         )
#         response = self.client.get(f'/rides/{ride.id}/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_cancel_ride(self):
#         self.client.force_authenticate(user=self.user)
#         ride = Ride.objects.create(
#             rider=self.user,
#             pickup_location='A',
#             dropoff_location='B'
#         )
#         response = self.client.patch(f'/rides/{ride.id}/cancel_ride/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Ride.objects.get(id=ride.id).status, Ride.CANCELLED)

#     def test_accept_ride_request(self):
#         driver_user = User.objects.create_user(username='driveruser', password='driverpass', is_driver=True, is_available=True)
#         ride = Ride.objects.create(
#             rider=self.user,
#             pickup_location='A',
#             dropoff_location='B'
#         )
#         self.client.force_authenticate(user=driver_user)
#         response = self.client.post(f'/rides/{ride.id}/accept_ride_request/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Ride.objects.get(id=ride.id).status, Ride.ACCEPTED)
#         self.assertEqual(Ride.objects.get(id=ride.id).driver, driver_user)


#Advanced Testing ride_sharing_app/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from ride_sharing_app.models import Ride

class RideMatchingTestCase(APITestCase):
    def setUp(self):
        self.rider_user = User.objects.create_user(username='rider', password='password')
        self.driver_user = User.objects.create_user(username='driver', password='password', is_driver=True, is_available=True)

        self.ride_data = {
            'rider': self.rider_user.id,
            'pickup_location': 'Location A',
            'dropoff_location': 'Location B',
            'status': Ride.REQUESTED,
        }

        self.ride = Ride.objects.create(**self.ride_data)

    def test_ride_matching_algorithm(self):
        response = self.client.post(f'/rides/{self.ride.id}/accept_ride/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['driver'], self.driver_user.id)

class RideStatusUpdatesTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='password')
        self.ride = Ride.objects.create(rider=self.user, pickup_location='Location A', dropoff_location='Location B', status=Ride.REQUESTED)

    def test_ride_status_updates(self):
        response = self.client.patch(f'/rides/{self.ride.id}/start_ride/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], Ride.STARTED)

class DriverAPITestCase(APITestCase):
    def setUp(self):
        self.driver_user = User.objects.create_user(username='test_driver', password='password', is_driver=True, is_available=True)

    def test_driver_api_endpoints(self):
        response = self.client.post('/rides/1/accept_ride/')  
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  

class RideTrackingSimulationTestCase(APITestCase):
    def setUp(self):
        self.driver_user = User.objects.create_user(username='test_driver', password='password', is_driver=True, is_available=True)
        self.ride = Ride.objects.create(rider=self.driver_user, driver=self.driver_user, pickup_location='Location A', dropoff_location='Location B', status=Ride.ACCEPTED)

    def test_ride_tracking_simulation(self):
        response = self.client.patch(f'/rides/{self.ride.id}/update_location/', {'current_location': 'New Location'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_location'], 'New Location')
