from django.contrib import admin

# Register your models here.
from models import Category, Establishment, Review, Point

admin.site.register(Category)
admin.site.register(Establishment)
admin.site.register(Review)
admin.site.register(Point)


