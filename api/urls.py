from django.urls import path

from .views import Authentication,Search,FriendRequestView

urlpatterns = [
    path('auth/', Authentication.as_view(), name='auth'),
    path('search/', Search.as_view(), name='search'),
    path('friend-request/', FriendRequestView.as_view(), name='friend-request'),
]