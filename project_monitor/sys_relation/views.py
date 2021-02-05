
import logging
from rest_framework import viewsets
from sys_relation.models import User, Role

from sys_relation.serializers import UserSerializer, RoleSerializer

logger = logging.getLogger('log')



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_user_email(self):
        user_info = User.objects.filter(roles__id=8).all()
        email_list = []
        for user in user_info:
            email_list.append(user.email)
        return email_list



class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer



