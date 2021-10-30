from django.core import serializers
from django.views import generic
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict


from .forms import ContactCreationForm
from .models import Contact

class ContactCreationView(SuccessMessageMixin, generic.CreateView):
    form_class = ContactCreationForm
    template_name = 'contacts/add.html'
    success_url = reverse_lazy('contacts:new')
    success_message = "Contact created!"

def home(request):
    return HttpResponse('Home')

class ContactList(generic.ListView):
    model = Contact
    context_object_name = 'contacts'
    template_name = 'contacts/list.html'

def contact_details(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    contact = {k: v for k, v in model_to_dict(contact).items() if v}
    return JsonResponse(contact)
