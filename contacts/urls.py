from django.urls import path

from .views import ContactCreationView, ContactList, home, contact_details

app_name = 'contacts'
urlpatterns = [
    path('', ContactList.as_view(), name='contact_list'),
    path('new/', ContactCreationView.as_view(), name='new'),
    path('<int:contact_id>', contact_details, name='details'),
    path('home/', home, name='home'),
]