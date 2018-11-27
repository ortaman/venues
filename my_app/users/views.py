
# from django.contrib.auth.models import User
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin

# from common.paginations import MyCustomPagination
from .models import User
from .serializers import UserCreateSer
from .permissions import AllowAnyCreateOrIsAuthenticated


class UserViewSet(CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    Endpoint to create users for anyone, retrieve and update the user.
    """
    lookup_field = 'pk'

    queryset = User.objects.all()

    serializer_class = UserCreateSer
    # authentication_classes = ("",)
    # pagination_class = MyCustomPagination
    permission_classes = (AllowAnyCreateOrIsAuthenticated,)

    '''
    def create(self, request, *args, **kwargs):
        return super(UserViewSet, self).create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(UserViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(UserViewSet, self).update(request, *args, **kwargs)
    '''
