
from rest_framework import serializers


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

        if not latitude or not longitude:
            return {
                'query': query,
                'limit': limit
            }

        return {
            'query': query,
            'll': '{0}, {1}'.format(latitude, longitude),
            'limit': limit,
        }
