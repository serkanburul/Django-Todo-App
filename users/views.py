from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView


# Create your views here.


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    fields = ('username', 'password')
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('taskList')


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('taskList')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('taskList')
        return super(RegisterView, self).get(*args, **kwargs)
