from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from users.serializers import User, UserSerializer
from django.contrib.auth.hashers import make_password


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data.update({'password': make_password(request.data.get('password'))})
        super().create(request, *args, **kwargs)
        return Response({"To continue start a chat with bot https://t.me/Suuupsupbot"},
                        status=status.HTTP_201_CREATED)


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.get(pk=self.request.user.pk)




