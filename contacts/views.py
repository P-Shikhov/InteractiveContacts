from django.http.response import HttpResponse
from django.urls.base import reverse, reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST

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


def home(request):
    return HttpResponse('200!')

class DashboardView(LoginRequiredMixin, generic.ListView, FormMixin):
    model = Contact
    allow_empty = True
    context_object_name = 'contacts'
    template_name = 'contacts/list.html'
    form_class = ContactCreationForm

    def get_queryset(self):
        # what if non-int is passed
        return Contact.objects.filter(user_id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)

        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data(object_list=self.object_list, form=self.form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        self.form = ContactCreationForm(context['prepopulated_form'])
        return super(DashboardView, self).post(request, *args, **kwargs) 


@login_required
@csrf_exempt #todo: csrf protection
def contact_details(request, contact_id, **kwargs): #todo: id in url for POST
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


class LogView(generic.ListView, FormMixin):
    model = LogEntry
    allow_empty = True
    context_object_name = 'log'
    template_name = 'contacts/log.html'
    form_class = LogEntryCreationForm

    def get_queryset(self, contact_id):
        # what if non-int is passed
        return LogEntry.objects.filter(contact_id=contact_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_id'] = self.kwargs['contact_id']
        return context

    def get(self, request, contact_id, *args, **kwargs):
        session_user = self.request.user
        if session_user.is_authenticated:
            contact_id_from_url = self.kwargs['contact_id']
            contact = get_object_or_404(Contact, pk=contact_id_from_url)
            if contact.user_id == session_user.id:
                form_class = self.get_form_class()
                self.form = self.get_form(form_class)
                self.object_list = self.get_queryset(contact_id_from_url)
                allow_empty = self.get_allow_empty()
                if not allow_empty:
                    if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                        is_empty = not self.object_list.exists()
                    else:
                        is_empty = not self.object_list
                    if is_empty:
                        raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                            'class_name': self.__class__.__name__,
                        })
                context = self.get_context_data(object_list=self.object_list, form=self.form)
                return self.render_to_response(context)
        return HttpResponseRedirect(reverse("contacts:contact_list"))

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        self.form = LogEntryCreationForm(context['prepopulated_form'])
        return super(LogView, self).post(request, *args, **kwargs)

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
