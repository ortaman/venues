
from rest_framework import status
from foursquare import Foursquare
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from common.mixins import APIMixin
from django.conf import settings
from .serializers import VenuesQuerySer


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
