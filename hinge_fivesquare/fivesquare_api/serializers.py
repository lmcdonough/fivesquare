from rest_framework import serializers
from models import Category, Establishment, Review
from django.contrib.auth.models import User
from taggit_serializer.serializers import (TagListSerializerField,
										   TaggitSerializer)



class CategorySerializer(serializers.ModelSerializer):
	'''The category serializer, in the future admins should be able to create categories
	for users to associate their establishments with, eg. Landmarks, Bars, Restaurants...'''

	pk = serializers.CharField(read_only=True)
	created_by = serializers.ReadOnlyField(source='created_by.username')
	name = serializers.CharField(required=True, allow_blank=False, max_length=200)

	class Meta:
			model = Category
			fields = ('pk', 'name', 'created_by')    

class ReviewSerializer(TaggitSerializer, serializers.ModelSerializer): 
	'''The review serializer, pretty straight forward, serializes and deserializes Review objects.'''
	pk = serializers.CharField(read_only=True)   
	created_by = serializers.ReadOnlyField(source='user.username')
	establishment_name = serializers.ReadOnlyField(source='establishment.name')

	class Meta:
			model = Review
			fields = ('pk', 'created_by', 'created', 'establishment', 'establishment_name', 'title', 'text', 'stars', 'tags')

class EstablishmentSerializer(serializers.HyperlinkedModelSerializer):  
	'''The establishment serializer serializes and deserializes Establishment objects.
	There are a few calculated fields that get serialized to return the average rating, unique
	list of tags, and the amount of reviews.'''

	pk = serializers.CharField(read_only=True)     
	created_by = serializers.ReadOnlyField(source='created_by.username')
	category = serializers.HyperlinkedRelatedField(view_name='category-detail', read_only=True)
	review_count = serializers.SerializerMethodField()   
	tags = serializers.SerializerMethodField()
	rating = serializers.SerializerMethodField()

	def get_review_count(self, establishment):
		'''returns the amount of reviews for an estalishment.'''

		reviews_queryset = Review.objects.filter(establishment=establishment).count()
		return reviews_queryset

	def get_tags(self, establishment):
		'''returns a unique list of tags for an astablishment'''

		tags_queryset = Review.objects.filter(establishment=establishment).values('tags') 
		tags_list = []
		tags = [tags_list.extend(x['tags']) for x in tags_queryset if tags_queryset]  
		return set(tags_list)

	def get_rating(self, establishment):
		'''returns the average rating for an establishment.'''
		
		stars_queryset = Review.objects.filter(establishment=establishment).values('stars') 
		stars_list = [x['stars'] for x in stars_queryset if stars_queryset] 
		stars = None
		if len(stars_list) > 0:
			stars = reduce(lambda x, y: x + y, stars_list) / float(len(stars_list))
		return stars

	class Meta:
			model = Establishment
			fields = ('pk', 'name', 'created_by', 'category', 'closed', 'city', 'state', 'country', 'location', 'review_count', 'rating', 'tags')

class UserSerializer(serializers.HyperlinkedModelSerializer):
	'''Straight forward, serializes the User object.'''

	class Meta:
		model = User
		fields = ('url', 'username')



