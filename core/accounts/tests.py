# from django.test import TestCase

import pytest
from django.urls import reverse
from .models import CustomUser




# Create your tests here.

@pytest.mark.django_db
def test_my_model_creation():
    obj = CustomUser.objects.create(name="Test")
    assert obj.name == "Test"

'''@pytest.mark.django_db
def test_my_view(client):
    response = client.get(reverse('my_view_name'))
    assert response.status_code == 200'''
