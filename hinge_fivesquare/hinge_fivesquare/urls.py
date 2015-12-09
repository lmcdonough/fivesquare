from django.conf.urls import url, include, patterns
from rest_framework import routers, serializers, viewsets
from  fivesquare_api import urls as api_urls
from django.contrib import admin

admin.autodiscover()


urlpatterns = [
    url(r'^', include(api_urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls))
]
