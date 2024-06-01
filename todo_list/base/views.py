from django.http import HttpResponse
from django.shortcuts import render,redirect
# from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Tasks
from django.urls import reverse_lazy
# Create your views here.

class CustomLogin(LoginView):
    template_name = "base/login.html"
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
    


class Registerpage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirected_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        User = form.save()
        if User is not None:
            login(self.request, User)

        return super(Registerpage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(Registerpage, self).get(*args, **kwargs)
    


class taskList(LoginRequiredMixin, ListView):
    # return HttpResponse('to do list')
    model = Tasks
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(User=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        # return context
    
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context



class taskDetail(LoginRequiredMixin, DetailView):
    model = Tasks  
    context_object_name = 'task'
    template_name = 'base/task.html'  
    

class taskCreate(LoginRequiredMixin, CreateView):
    model = Tasks
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.User = self.request.user
        return super(taskCreate, self).form_valid(form)



class taskUpdate(LoginRequiredMixin, UpdateView):
    model = Tasks
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')




class taskDelete(LoginRequiredMixin, DeleteView):
    model = Tasks
    fields = '__all__'
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')