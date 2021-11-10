from django.urls import path

from .views import DashboardView, LogView, process_contact_creation, handle_contact_details_request, create_log_entry

app_name = 'contacts'
urlpatterns = [
    path('', DashboardView.as_view(), name='contact_list'),
    path('new/', process_contact_creation, name='new'),
    path('<int:contact_id>', handle_contact_details_request, name='details'),
    path('<int:contact_id>/log', LogView.as_view(), name='log'),
    path('<int:contact_id>/log/new-entry', create_log_entry),
]