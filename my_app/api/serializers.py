
from math import sin, cos, sqrt, atan2, radians
from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Favorite

class VenuesQuerySer(serializers.Serializer):
    query = serializers.CharField(required=False)
    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)
    limit = serializers.IntegerField(required=False)

    def validate_title(self, value):
        return value

    def to_representation(self, obj):
        query = obj.get("query")
        latitude = obj.get("latitude")
        longitude = obj.get("longitude")
        limit = obj.get("limit", 10)

        if not query:
            return {
                'll': '{0}, {1}'.format(latitude, longitude),
                'limit': limit
            }

        return {
            'query': query,
            'll': '{0}, {1}'.format(latitude, longitude),
            'limit': limit,
        }


class FavoriteSerializer(serializers.ModelSerializer):

    added_by = UserSerializer(read_only=True)
    distance = serializers.SerializerMethodField('calculate_distance', read_only=True)

    def calculate_distance(self, favorite):
        query_params = self.context.get('request').query_params

        lat = query_params.get('latitude')
        lng = query_params.get('longitude')

        if not lat or not lng:
            return None

        R = 6373.0

        lat1 = radians(float(lat))
        lon1 = radians(float(lng))
        lat2 = radians(favorite.lat)
        lon2 = radians(favorite.lng)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'address', 'photo', 'lat', 'lng',
                  'tip_count', 'users_count', 'checkins_count', 'visits_count', 'added_by', 'distance')

    read_only_fields = ('created_at', 'updated_at')

    def perform_create(self, serializer):
        return serializer.save(added_by=self.request.user)


class FavoriteParcialUpdateSer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('photo',)
