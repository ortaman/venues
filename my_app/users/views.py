
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin

from .models import User
from .serializers import UserSerializer
from .permissions import AllowAnyCreateOrIsAuthenticated, IsSelfUserOrReadOnly


class UserViewSet(CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    Endpoint to create users for anyone, retrieve and update the user.
    """
    lookup_field = 'pk'

    queryset = User.objects.all()
    serializer_class = UserSerializer

    # authentication_classes = ("",)
    # pagination_class = MyCustomPagination
    permission_classes = (AllowAnyCreateOrIsAuthenticated, IsSelfUserOrReadOnly)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        token = Token.objects.create(user=serializer.instance)
        headers = self.get_success_headers(serializer.data)

        return Response({'token': token.key}, status=status.HTTP_201_CREATED, headers=headers)
