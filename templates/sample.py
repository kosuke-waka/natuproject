from calendar import c
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse,reverse_lazy
from django.contrib.auth import logout
from django.views.generic import ListView,DetailView,CreateView,DeleteView,UpdateView
from .models import Book,Review
#from .accounts.models import User_Home
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Avg
#from django.core.paginator import Pagenator
#from .consts import ITEM_PER_PAGE


# Create your views here.
class ListBookView(LoginRequiredMixin,ListView):
    template_name: str = 'book/book_list.html'
    queryset = Book.objects.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ranking_list'] = Book.objects.annotate(avg_rating=Avg('review__rate')).order_by('-avg_rating')
        return context

class DetailBookView(LoginRequiredMixin,DetailView):
    template_name: str = 'book/book_detail.html'
    model = Book

class CreateBookView(LoginRequiredMixin,CreateView):
    template_name: str = 'book/book_create.html'
    model = Book
    #fields = ('title','user_id','text','file','category')
    fields = ('title','text','file','category')
    #success_url = reverse_lazy('index')
    success_url = reverse_lazy('list-book')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(username=self.request.user)
        print(context)
        return context


    def form_valid(self, form):
        #print(form)
        #print(User.objects.get(username=self.request.user))
        #form.objects.user_id = User.objects.get(username=self.request.user)
        form.instance.user_id = self.request.user
        return super(CreateView, self).form_valid(form)


class DeleteBookView(LoginRequiredMixin,DeleteView):
    template_name: str = 'book/book_confirm_delete.html'
    model = Book
    success_url = reverse_lazy('list-book')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user_id != self.request.user:
            raise PermissionDenied

        return obj

class UpdateBookView(LoginRequiredMixin,UpdateView):
    model = Book
    template_name: str = 'book/book_update.html'
    fields = ('title','text','file','category')
    success_url = reverse_lazy('list-book')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user_id != self.request.user:
            raise PermissionDenied

        return obj

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def index_view(request):
    object_list = Book.objects.order_by('category')
    return render(request,'book/index.html',{'object_list':object_list})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

class CreateReviewView(CreateView):
    model = Review
    fields = ('book','title','text','rate')
    template_name = 'book/review_form.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = Book.objects.get(pk=self.kwargs['book_id'])
        #print(context)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail-book',kwargs={'pk':self.object.book.id})