from django.shortcuts import render,redirect
from .models import *
from .forms import *
from .utils import scrape_url
from django.views import View 
from django.views.generic import ListView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


# Create your views here.

class AddBookmarkView(LoginRequiredMixin,View):
    def post(self,request):
        form=BookmarkForm(request.POST)
        if form.is_valid():
            url=form.cleaned_data['url']
            custom_name=form.cleaned_data['custom_name']
            validator = URLValidator()
            try:
                validator(url)
            except ValidationError:
                messages.error(request, "Enter valid URL with https://")
                return redirect("home")
            try:
                data=scrape_url(url)
                if Bookmark.objects.filter(user=request.user, url=url).exists():
                    messages.warning(request, "Bookmark already exists")
                    return redirect("home")
                Bookmark.objects.create(
                    user=request.user,
                    url=url,
                    title=data["title"],
                    description=data['description'],
                    favicon=data['favicon'],
                    custom_name=custom_name,
                )
                messages.success(request,"Bookmark Added!")
            except:
                messages.error(request,"Invalid URL")
        return redirect("bookmarks:home")
    
class BookmarkListView(LoginRequiredMixin,ListView):
    model=Bookmark
    template_name="bookmarks/home.html"
    context_object_name="bookmarks"
    paginate_by=10
    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user).order_by("-created_at")
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["form"]=BookmarkForm()
        return context

