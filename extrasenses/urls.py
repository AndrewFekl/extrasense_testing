from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.MainView, name='main'),
    path('tests', views.ExtrasensesView.as_view(), name='extrasenses-testing'),
    path('results', views.ResultsView.as_view(), name='extrasenses-results'),
]
