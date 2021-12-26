from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ExtrasensesView.as_view(), name='extrasenses'),
]
