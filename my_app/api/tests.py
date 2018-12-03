
import json

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User


class VenuesWithAuthTest(APITestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=User.objects.get(username='username'))

    def test_list_venues(self):
        response = self.client.get(
            '/api/v1/venues/?'
            'query=car&latitude=40&longitude=-76&',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_list_venues_without_location(self):
        response = self.client.get(
            '/api/v1/venues/?'
            'query=car',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_venues_without_query(self):
        response = self.client.get(
            '/api/v1/venues/?'
            'latitude=40&longitude=-76',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_venues_with_limit(self):
        response = self.client.get(
            '/api/v1/venues/?'
            'query=car&latitude=40&longitude=-76&'
            'limit=5',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_list_venues_with_limit_and_paginated(self):
        response = self.client.get(
            '/api/v1/venues/?'
            'query=car&latitude=40&longitude=-76&'
            'limit=5&'
            'page=2&paginate_by=3',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_page'], 2)
        self.assertEqual(response.data['paginated_by'], 3)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 2)

    def test_list_venues_with_limit_paginated_and_order_by_distance(self):
        response = self.client.get(
            '/api/v1/venues/?'
            'query=car&latitude=40&longitude=-76&'
            'limit=5&'
            'page=1&paginate_by=5&'
            'order_by=distance',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_page'], 1)
        self.assertEqual(response.data['paginated_by'], 5)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

        venues = response.data['results']

        for i in range(len(venues) - 1):
            if venues[i]['location']['distance'] > venues[i + 1]['location']['distance']:
                raise AssertionError("list of venues not shorted by distance")
