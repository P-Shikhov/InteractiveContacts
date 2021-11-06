from django.urls import path

from .views import DashboardView, process_contact_creation, contact_details, home

app_name = 'contacts'
urlpatterns = [
    path('', DashboardView.as_view(), name='contact_list'),
    # path('home/', home, name='home'),
    path('new/', process_contact_creation, name='new'),
    path('<int:contact_id>', contact_details, name='details'),
]