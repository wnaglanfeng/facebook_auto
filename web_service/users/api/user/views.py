# -*- coding: utf-8 -*-

from rest_framework import viewsets

from users.api.user.serializers import UserSerializer
from users.models import User
from utils.request_utils import AdminPermission, search, handle_order


# Created by: guangda.lee
# Created on: 2019/3/25
# Function: 用户视图


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminPermission]

    @handle_order
    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(auth__username=username)
        email = self.request.query_params.get('email', None)
        if email is not None:
            queryset = queryset.filter(auth__email=email)
        fullname = self.request.query_params.get('fullname', None)
        if fullname is not None:
            queryset = queryset.filter(auth__last_name__icontains=fullname)
        from django.db.models import Q
        queryset = search(self.request, queryset,
                          lambda qs, keyword: qs.filter(Q(auth__username=keyword)|Q(auth__email__icontains=keyword)|Q(auth__last_name__icontains=keyword)))
        return queryset

    # 移除用户
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            return super(UserViewSet, self).destroy(request, *args, **kwargs)
        finally:
            # 删除 auth_user 中的关联数据
            instance.auth.delete()

