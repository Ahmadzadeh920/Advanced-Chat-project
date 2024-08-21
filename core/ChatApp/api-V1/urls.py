from django.urls import path
from .views import GroupMessagesView

urlpatterns = [
    path('messages/<int:pk>/', GroupMessagesView.as_view(), name='group-messages-retrieve'),
]