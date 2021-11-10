from django.urls.base import reverse
from django.views import generic
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect

from .forms import ContactCreationForm, LogEntryCreationForm
from .models import Contact, LogEntry

@login_required
@require_POST
def process_contact_creation(request):
    form = ContactCreationForm(request.POST)
    if form.is_valid():
        contact = form.save(commit=False)
        contact.user_id = request.user.id
        contact.save()
        messages.success(request, 'Contact Created')
        return HttpResponseRedirect(reverse('contacts:contact_list'))
    else:
        messages.error(request, '{}'.format(form.errors))
    return HttpResponseRedirect(reverse('contacts:contact_list'))


class DashboardView(LoginRequiredMixin, generic.ListView):
    model = Contact
    allow_empty = True
    context_object_name = 'contacts'
    template_name = 'contacts/list.html'

    def get_queryset(self):
        # what if non-int is passed
        return Contact.objects.filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['form'] = ContactCreationForm()
        return context


@login_required
@csrf_exempt #todo: csrf protection
def handle_contact_details_request(request, contact_id, **kwargs): #todo: id in url for POST
    if (request.method == 'GET'):
        contact = get_object_or_404(Contact, pk=contact_id)
        return JsonResponse(model_to_dict(contact))
    elif (request.method == 'POST'):
        allowed_fields = [field.name for field in Contact._meta.get_fields()]
        allowed_fields.remove('id')
        request_body = request.body.decode('utf-8')
        update_values = dict()
        for pair in request_body.split("&"):
            pair = pair.split("=")
            if pair[1] and pair[0] in allowed_fields:
                update_values[pair[0]] = pair[1]
        contact_to_be_updated = Contact.objects.filter(pk=contact_id)
        if len(contact_to_be_updated) == 1 and contact_to_be_updated[0].user.id == request.user.id:
            contact_to_be_updated.update(**update_values)
        else:
            messages.error(request, 'Permission denied.')
        return HttpResponseRedirect(reverse("contacts:contact_list"))


class LogView(LoginRequiredMixin, generic.ListView):
    model = LogEntry
    allow_empty = True
    context_object_name = 'log'
    template_name = 'contacts/log.html'

    def get_queryset(self):
        try:
            contact = Contact.objects.get(id=self.kwargs['contact_id'])
        except Contact.DoesNotExist:
            messages.error(self.request, 'Contact {} is not available'.format(self.kwargs['contact_id']))
            return None

        if contact.user_id == self.request.user.id:
            return LogEntry.objects.filter(contact_id=contact.id)
        else:
            messages.error(self.request, 'Contact {} is not available'.format(self.kwargs['contact_id']))
            return None

    def render_to_response(self, context):
        if self.object_list is None:
            return redirect('contacts:contact_list')
        return super().render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LogEntryCreationForm()
        return context


@require_POST
def create_log_entry(request, contact_id):
    session_user = request.user
    if session_user.is_authenticated:
        contact = get_object_or_404(Contact, pk=contact_id)
        if contact.user_id == session_user.id:
            form = LogEntryCreationForm(request.POST)
            if form.is_valid():
                log_entry = form.save(commit=False)
                log_entry.contact_id = contact.id
                log_entry.save()
                messages.success(request, 'Log Entry Created')
                return HttpResponseRedirect(reverse('contacts:log', kwargs={'contact_id': contact.id}))
