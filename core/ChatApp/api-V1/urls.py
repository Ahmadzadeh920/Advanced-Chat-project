from django.urls import path
from . import views
app_name = "api-v1"
urlpatterns = [
    path('group/<int:pk>', views.GroupMessagesView.as_view(), name='group-messages-retrieve'),
    path('group/', views.GroupListCreateView.as_view(), name='group-list-create'),
    path('login/', views.loginView.as_view(), name='login_render'),
    path('', views.IndexView.as_view(), name='index_render'),
    path('user-groups/',views.UserGroupsListView.as_view(), name='user-groups-list'),

    
]