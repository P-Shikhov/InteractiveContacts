from django.core import serializers
from django.urls.base import reverse
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.views.generic.edit import ModelFormMixin
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

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
# class ContactList(generic.ListView, ModelFormMixin):
    model = Contact
    context_object_name = 'contacts'
    template_name = 'contacts/list.html'
    form_class = ContactCreationForm

@csrf_exempt #todo: csrf protection
@require_http_methods(['GET', 'POST'])
def contact_details(request, contact_id, **kwargs): #todo: id in url for POST
    if (request.method == 'GET'):
        contact = get_object_or_404(Contact, pk=contact_id)
        return JsonResponse(model_to_dict(contact))
    else: # POST
        allowed_fields = [field.name for field in Contact._meta.get_fields()]
        allowed_fields.remove('id')
        request_body = request.body.decode('utf-8')
        update_values = dict()
        for pair in request_body.split("&"):
            pair = pair.split("=")
            if pair[1] and pair[0] in allowed_fields:
                update_values[pair[0]] = pair[1]
        Contact.objects.filter(pk=contact_id).update(**update_values)
        return HttpResponseRedirect(reverse("contacts:contact_list"))

# def update_contact(request):
