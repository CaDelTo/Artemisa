from django.urls import path
from .api import get_data

urlpatterns = [
    path('', get_data, name='data-retriever'),
]