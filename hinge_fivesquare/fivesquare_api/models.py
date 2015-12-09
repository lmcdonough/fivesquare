# Create your models here.
from django.db import models
from django.contrib.auth.models import User
# from .. import settings
from taggit.managers import TaggableManager
from djangotoolbox.fields import EmbeddedModelField
from django_mongodb_engine.contrib import MongoDBManager
from forms import ObjectListField
from djangotoolbox.fields import ListField
from pymongo import GEO2D

STAR_CHOICES = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]


class Category(models.Model):
	created_by = models.ForeignKey(User, related_name='category')
	name = models.CharField(max_length=200, blank=False, null=False)

	class Meta:
		app_label = 'fivesquare_api'

	def __unicode__(self):
		return self.name

class Point(models.Model):
	longitude = models.FloatField()
	latitude = models.FloatField()

	def __unicode__(self):
		try:
			return "{}, {}".format(self.longitude, self.latitude)
		except:
			return ''


class Establishment(models.Model):
	name = models.CharField(max_length=200, blank=False, null=False)
	created_by = models.ForeignKey(User, related_name='establishment')
	created = models.DateTimeField(auto_now_add=True)
	category = models.ForeignKey(Category, related_name='establishment', null=True, blank=True)
	closed = models.BooleanField(default=False)
	city = models.CharField(max_length=200, blank=False, null=False)
	state = models.CharField(max_length=10, blank=False, null=False)
	country = models.CharField(max_length=10, blank=False, null=False)
	latitude = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=9)
	longitude = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=9)
	location = EmbeddedModelField(Point, null=True, blank=True)
	objects = MongoDBManager()

	class Meta:
		ordering = ('created',)
		app_label = 'fivesquare_api'

	class MongoMeta:
	  indexes = [
	     {'fields': [('location', GEO2D)]}
	  ]

	def __unicode__(self):
		return self.name


class Review(models.Model):	
	user = models.ForeignKey(User, related_name='review')
	establishment = models.ForeignKey(Establishment, related_name='establishment')
	created = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=200, blank=True, null=True, default='')
	text = models.TextField()
	stars = models.IntegerField(choices=STAR_CHOICES, null=False, blank=False)
	tags = ListField()

	class Meta:
		ordering = ('created',)
		app_label = 'fivesquare_api'

	def __unicode__(self):
		try:
			return "{}, {}".format(self.user.username, self.establishment.name)
		except:
			return ''

