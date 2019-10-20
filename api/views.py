from rest_framework import viewsets
import django_filters

from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import PlacesSerializer
from .models import Places, Review

class LatLngFilter(django_filters.FilterSet):

    lat = django_filters.RangeFilter()
    lng = django_filters.RangeFilter()
    facilityId = django_filters.CharFilter()
    class Meta:
        model = Places
        fields = ['lat','lng','facilityId']

class PlacesViewSet(viewsets.ModelViewSet):

    lookup_field = 'facilityId'
    queryset = Places.objects.all()
    serializer_class = PlacesSerializer
    filter_class = LatLngFilter

    @action(detail=True, methods=['get'])
    def reviews(self, request, facilityId=None, pk=None):
        queryset = Places.objects.filter(facilityId=facilityId)
        serializer = PlacesSerializer(queryset, fields=["review"], many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def review(self, request, facilityId=None, pk=None):
        places = Places.objects.get(facilityId=facilityId)
        Review.objects.create(places=places, **request.data)
        return Response(request.data)
    