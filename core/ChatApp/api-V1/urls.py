from django.urls import path
from . import views
app_name = "api-v1"
urlpatterns = [
    path('group/<int:pk>', views.GroupMessagesView.as_view(), name='group-messages-retrieve'),
    
     path('group/', views.GroupListCreateView.as_view(), name='group-list-create'),
]