from django.urls import path
from django.urls import include
from . import views
app_name = "ChatApp"

urlpatterns = [
    path("api/v1/", include("ChatApp.api-V1.urls")),
    path("", views.index, name="render_page_index"),
]