from django.views import generic
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm

class RegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'
