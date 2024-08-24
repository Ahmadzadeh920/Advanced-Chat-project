from django.urls import path
from .views import GroupMessagesView, room

urlpatterns = [
    path('messages/<int:pk>/', GroupMessagesView.as_view(), name='group-messages-retrieve'),
    path('index/', room, name='index_page_render'),
]