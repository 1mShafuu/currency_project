from django.urls import path
from currency_app import views

urlpatterns = [
    path('get-current-usd/', views.get_current_usd, name='get_current_usd'),
]