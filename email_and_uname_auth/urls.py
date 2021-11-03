from django.urls import path

from .views import RegisterView

app_name = 'registration'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='home'),
]