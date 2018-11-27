
# from django.contrib.auth.models import User
from rest_framework import serializers
from .models import User


class UserCreateSer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields =  ('email', 'username', 'names', 'surnames', 'phone', 'gender')

    read_only_fields = ('token', 'is_staff', 'created_at', 'updated_at')
