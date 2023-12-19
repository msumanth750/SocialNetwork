from .views import search_users, send_friend_request, accept_friend_request, list_friends, list_pending_friend_requests
from django.urls import path
from .views import signup, login_user, authenticated_api

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_user, name='login'),
    path('authenticated-api/', authenticated_api, name='authenticated-api'),

    path('search-users/<str:keyword>/', search_users, name='search-users'),
    path('send-friend-request/<int:friend_id>/',
         send_friend_request, name='send-friend-request'),
    path('accept-friend-request/<int:friend_id>/',
         accept_friend_request, name='accept-friend-request'),
    path('list-friends/', list_friends, name='list-friends'),
    path('list-pending-friend-requests/', list_pending_friend_requests,
         name='list-pending-friend-requests'),
]