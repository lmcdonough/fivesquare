from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient, APITestCase
from models import *
from views import *
from django.contrib.auth.models import User

class RootTests(APITestCase):
	
	def setUp(self):
   		self.client = APIClient()
   		self.domain = 'testserver'
   		self.response = self.client.get('/')
   		self.data = {
   		    "reviews": "http://%s/reviews/" % self.domain, 
    		"establishments": "http://%s/establishments/" % self.domain,
    		"users": "http://%s/users/" % self.domain, 
    		"categories": "http://%s/categories/" % self.domain
    		}

   	def test_status(self):   		
   		self.assertEqual(self.response.status_code, 200)

   	def test_endpoints_data(self):
   		self.assertEqual(self.response.data, self.data)


class EstablishmentTests(APITestCase):
	
	def setUp(self):
   		self.client = APIClient()   
   		self.test_user = User.objects.create_user("test_user", "test@user.com", "123456")				
		self.client.force_authenticate(user=self.test_user)
		self.url = reverse('establishment-list')		
   		self.establishment_data = {
   			'name': 'Test Location',
   			'created_by': self.test_user.pk,
   			'city': 'New York City',
   			'state': 'New York',
   			'country': 'USA',
   			'location': {
   				'longitude': 73.9753,
   				'latitude': 40.7517
   			}
   		}

   	def test_status(self):
   		response = self.client.get(self.url)
   		self.assertEqual(response.status_code, 200)

   	def test_create(self):
   		response = self.client.post(self.url, self.establishment_data, format='json')
   		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
   		self.assertEqual(Establishment.objects.count(), 1)
   		self.assertEqual(Establishment.objects.get().name, 'Test Location')

   	def test_read(self):
   		establishment = Establishment.objects.get()
   		self.url = reverse('establishment-detail', kwargs={'pk': establishment.pk})   		
 		self.response = self.client.get(self.url)   	
   		self.assertEqual(self.response.data['pk'], establishment.pk)


class ReviewTests(APITestCase):
	
	def setUp(self):
   		self.client = APIClient()   
   		self.test_user = User.objects.create_user("test_user", "test@user.com", "123456")		 				
		self.client.force_authenticate(user=self.test_user)
		self.test_establishment = Establishment(
			name='Test Location',
			created_by=self.test_user,
			city='New York City',state='NY',
			country='USA',
			location=Point(longitude=73.9753, latitude=40.7517))		
		self.test_establishment.save()
		self.url = reverse('review-list')
		self.response = self.client.get(self.url)
		
   	def test_status(self):

   		self.assertEqual(self.response.status_code, 200)

   	def test_create(self):
   		
   		review_data = {
   			'user': self.test_user.pk,
   			'establishment': self.test_establishment.pk,
   			'title': 'This is the test Title',
   			'text': 'This is the text for the test Review',
   			'stars': 5,
   			'tags': ['FirstTag', 'SecondTag']
   			}
   
   		response = self.client.post(self.url, review_data, format='json')
   		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
   		self.assertEqual(Review.objects.count(), 1)
   		self.assertEqual(Review.objects.get().title, 'This is the test Title')

   	def test_read(self):
   		review = Review.objects.get()
   		self.url = reverse('review-detail', kwargs={'pk': review.pk})   		
 		self.response = self.client.get(self.url)   	
   		self.assertEqual(self.response.data['pk'], review.pk)



