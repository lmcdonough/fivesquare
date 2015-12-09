from rest_framework import generics, permissions, viewsets
from models import Category, Review, Establishment
from serializers import CategorySerializer, UserSerializer, ReviewSerializer, EstablishmentSerializer
from django.contrib.auth.models import User
from permissions import IsOwnerOrReadOnly, IsOwner
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAdminUser


@api_view(('GET',))
@permission_classes((permissions.AllowAny,))
def api_root(request, format=None):
    '''returns the endpoints for tha api.'''

    return Response({
        'users': reverse('user-list', request=request, format=format),
        'categories': reverse('category-list', request=request, format=format),
        'reviews': reverse('review-list', request=request, format=format),
        'establishments': reverse('establishment-list', request=request, format=format)        
    })


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset handles all the actions (list create, retreive, update, destroy)
    for the User viewset.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwner)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    This viewset handles all the actions (list create, retreive, update, destroy)
    for the Category viewset.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminUser)


    def perform_create(self, serializer):
        '''handles the saving of the serializer, 
        and assigns the user to the action'''

        serializer.save(created_by=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


    def perform_create(self, serializer):
        '''handles the saving of the serializer, 
        and assigns the user to the action'''

        serializer.save(user=self.request.user)

    def get_queryset(self):
        '''handles the queryset and any query parameters to filter reviews by establishment.'''

        establishment = self.request.query_params.get('establishment', None)
        if establishment is not None:
            self.queryset = self.queryset.filter(establishment=establishment).order_by('-created')
        return self.queryset


    
class EstablishmentViewSet(viewsets.ModelViewSet):
    """
    This viewset handles all the actions (list create, retreive, update, destroy)
    for the Establishment viewset.
    """
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


    def perform_create(self, serializer):
        '''handles the saving of the serializer, 
        and assigns the user to the action'''

        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        '''handles the queryset and any query parameters to filter establishments
        by distance to a particular lat long.'''

        latitude = self.request.query_params.get('latitude', None)
        longitude = self.request.query_params.get('longitude', None)
        distance = self.request.query_params.get('distance', None)

        if latitude and longitude and distance:
            self.queryset = Establishment.objects.raw_query({
                'location' : {
                    '$nearSphere': {
                        '$geometry': {
                            'type': "Point",
                            'coordinates': [ float(longitude) , float(latitude)]
                        }, 
                        '$maxDistance': float(distance)
                    }
                }   
            })
        return self.queryset


