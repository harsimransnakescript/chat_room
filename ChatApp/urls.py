from django.urls import path

from .views import *


urlpatterns = [
    path("chat/", index, name="index"),
    path("chat/<str:room_name>/", room, name="room"),
    path('', signup, name='signup'),
    path('login/', login, name='login'),
    path('user/', normal_user_View,name="user"),
    path('chat/api/rooms/',chat_room_view,name='chat/api/rooms/'),
    path('chat/api/users/',user_list_View,name = 'chat/api/users/'),
    path('chat/api/add-room-name/',add_roomName,name='chat/api/add-room-name/'),
    path('user_status/<str:room_name>', user_status,name="user_status"),
]