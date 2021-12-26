from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ExtrasensesView.as_view(), name='extrasenses'),
    path('test/', views.session_test, name='test'),
    path('test2/', views.SessionTestView.as_view(), name='test2'),
]
