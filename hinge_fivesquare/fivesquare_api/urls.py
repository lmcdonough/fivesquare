from django.conf.urls import url
from views import UserViewSet, CategoryViewSet, ReviewViewSet, EstablishmentViewSet
from rest_framework.urlpatterns import format_suffix_patterns
from viewset_maps import CustomViewSet, ViewSetType
import views


urlpatterns = [
    url(r'^$', views.api_root),

    url(r'^categories/$', CustomViewSet.register(CategoryViewSet, ViewSetType.GENERIC_LIST) , name='category-list'),
    url(r'^category/(?P<pk>[a-zA-Z0-9]+)/$', CustomViewSet.register(CategoryViewSet, ViewSetType.GENERIC_DETAIL), name='category-detail'),
    url(r'^reviews/$', CustomViewSet.register(ReviewViewSet, ViewSetType.GENERIC_LIST) , name='review-list'),
    url(r'^review/(?P<pk>[a-zA-Z0-9]+)/$', CustomViewSet.register(ReviewViewSet, ViewSetType.GENERIC_DETAIL), name='review-detail'),
    url(r'^establishments/$', CustomViewSet.register(EstablishmentViewSet, ViewSetType.GENERIC_LIST) , name='establishment-list'),
    url(r'^establishment/(?P<pk>[a-zA-Z0-9]+)/$', CustomViewSet.register(EstablishmentViewSet, ViewSetType.GENERIC_DETAIL), name='establishment-detail'),   
    url(r'^users/$', CustomViewSet.register(UserViewSet, ViewSetType.GENERIC_LIST), name='user-list'),
    url(r'^users/(?P<pk>[a-zA-Z0-9]+)/$', CustomViewSet.register(UserViewSet, ViewSetType.READ_ONLY_DETAIL), name='user-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
