from models import Establishment, Category, Review
from django.contrib.auth.models import User

def execute():
	user = User.objects.get(username='fivesquare_admin')
	category = Category.objects.get(name='Landmark')
	establishment = Establishment()


	establishment.name = 'Chrysler Building'
	establishment.created_by = user
	establishment.city = 'New York'
	establishment.state = "NY"
	establishment.country = 'USA'	
	establishment.latitude = 40.7517
	establishment.longitude = 73.9753
	establishment.category = category
	establishment.save()
	print "Done"


def make_review():
	user = User.objects.get(username='fivesquare_admin')
	establishment = Establishment.objects.get(name='Chrysler Building')

	review = Review()
	review.user = user
	review.establishment = establishment
	review.title = 'Site Seeing at the Chrysler Building.'
	review.text = 'We decided to go see the Chrysler Building and the view was pretty great. Price was also reasonable.'
	review.stars = 3
	review.tags = ['Site Seeing', 'Urban', 'Cheap']
	review.save()
	print "DONE"