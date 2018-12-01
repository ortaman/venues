
from foursquare import Foursquare

from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from common.mixins import APIMixin
from common.paginations import MyCustomPagination
from django.conf import settings

from .models import Favorite
from .serializers import VenuesQuerySer, FavoriteSerializer, FavoriteParcialUpdateSer


class FourSquareVenuesAPIView(APIView, APIMixin):
    """
    Get list of venues from foursquare.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        query_params = request.query_params
        query_serializer = VenuesQuerySer(data=query_params)

        if not query_serializer.is_valid():
            return Response(query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Construct the client object
        client = Foursquare(client_id=settings.FOURSQUARE.get('CLIENT_ID'),
                            client_secret=settings.FOURSQUARE.get('CLIENT_SECRET'),
                            redirect_uri=settings.FOURSQUARE.get('REDIRECT_URL'))

        # Build the authorization url for your app
        auth_uri = client.oauth.auth_url()

        params = query_serializer.data
        venues = client.venues.search(params=params)
        venues = venues['venues']

        # Shorted
        if query_params.get('order_by') == 'distance':
            venues = sorted(venues, key=lambda k: k['location']['distance'])

        elif query_params.get('order_by') == 'popular':
            venues = sorted(venues, key=lambda k: k['stats']['visitsCount'])

        # Pagination
        page = query_params.get('page')
        paginate_by = query_params.get('paginate_by')

        if page and paginate_by:
            venues = self.get_pagination(venues, page, paginate_by)

        return Response(venues)


class FavoriteViewSet(CreateModelMixin, ListModelMixin, UpdateModelMixin,
                      DestroyModelMixin, GenericViewSet):

    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    pagination_class = MyCustomPagination
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)

    def list(self, request, *args, **kwargs):
        query_params = request.query_params
        queryset = self.filter_queryset(self.get_queryset())

        if query_params.get('order_by') == 'distance':
            queryset = self.queryset.filter(added_by=request.user)

        elif query_params.get('order_by') == 'popular':
            queryset = self.queryset.filter(added_by=request.user).order_by('visits_count')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['results'] = sorted(response.data['results'], key=lambda f: f['distance'])
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action in ['partial_update']:
            return FavoriteParcialUpdateSer

        return self.serializer_class
