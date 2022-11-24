import os

from multiprocessing import context
from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.views.generic import CreateView,ListView,UpdateView
from .models import User_Home
from book.models import Book
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SignupForm

# Create your views here.

class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('list-book')

    def form_valid(self, form):
        #https://knsoza1.com/wp-content/uploads/2020/07/70b3dd52350bf605f1bb4078ef79c9b9.png
        self.object = form.save()
        User_Home.objects.create(user_id=form.instance,text="未入力",thumbnail="")
        return super().form_valid(form)

class UserBookView(LoginRequiredMixin,ListView):
    template_name: str = 'accounts/user_home.html'
    model = User_Home

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_list'] = User_Home.objects.filter(user_id=self.request.user)
        context['book_list'] = Book.objects.filter(user_id=self.request.user)
        """
        context.update({
            #'home_list':User_Home.objects.filter(user_id=self.request.user),
            'book_list':Book.objects.filter(user_id=self.request.user),
        })
        print(context)
        """
        return context

class UpdateUserProfileView(LoginRequiredMixin,UpdateView):
    model = User_Home
    template_name = 'accounts/user_profile.html'
    fields = ('text','thumbnail')
    success_url = reverse_lazy('accounts:home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context