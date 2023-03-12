from users.views import UserCreateAPIView, UserDestroyAPIView, UserListAPIView, UserRetrieveUpdateAPIView
from django.urls import path


urlpatterns = [
    path('', UserListAPIView.as_view(), name='users'),
    path('create/', UserCreateAPIView.as_view(), name='create_user'),
    path('<int:pk>/', UserRetrieveUpdateAPIView.as_view(), name='retrieve_update_user'),
    path('delete/<int:pk>/', UserDestroyAPIView.as_view(), name='delete_user'),
    ]