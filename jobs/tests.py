from django.test import TestCase

# Create your tests here.
import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_homepage_loads():
    client = Client()
    response = client.get(reverse("job_list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_admin_login_page():
    client = Client()
    response = client.get("/admin/login/")
    assert response.status_code == 200
