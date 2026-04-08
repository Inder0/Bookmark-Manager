from django.shortcuts import render,redirect
from .models import *
from .forms import *
from .utils import scrape_url
from django.views import View 
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.

class AddBookmarkView(LoginRequiredMixin,View):
    def post(self,request):
        form=BookmarkForm(request.POST)
        if form.is_valid():
            url=form.cleaned_data['url']
            custom_name=form.cleaned_data['custom_name']
            if not url.startswith("http"):
                url="https://"+url
            validator = URLValidator()
            try:
                validator(url)
            except ValidationError:
                form.add_error("url", "Enter a valid URL starting with http/https")
                return self.render_with_errors(request, form)
            try:
                
                if Bookmark.objects.filter(user=request.user, url=url).exists():
                    form.add_error("url", "Bookmark already exists")
                    return self.render_with_errors(request, form)
                data=scrape_url(url)
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

def search_bookmarks(request):
    query=request.GET.get("q","")
    page_number = request.GET.get("page")
    bookmarks=Bookmark.objects.filter(user=request.user)
    if query:
        bookmarks=bookmarks.filter(
            Q(title__icontains=query) | 
            Q(custom_name__icontains=query) |
            Q(url__icontains=query)|
            Q(description__icontains=query)
        )
    paginator = Paginator(bookmarks, 10)
    page_obj = paginator.get_page(page_number)
    return render(request,template_name="bookmarks/partials/bookmark_list.html",context={
                                                                        "bookmarks": page_obj.object_list,
                                                                        "page_obj": page_obj,
                                                                        "query": query})
def delete_bookmark(request, pk):
    bookmark = Bookmark.objects.get(id=pk, user=request.user)

    if request.method == "POST":
        bookmark.delete()
        messages.success(request,message="Bookmark deleted successfully")
        
        query = request.GET.get("q", "")
        bookmarks = Bookmark.objects.filter(user=request.user)
        if query:
            bookmarks = bookmarks.filter(
                Q(title__icontains=query) |
                Q(custom_name__icontains=query) |
                Q(url__icontains=query)
            )

        paginator = Paginator(bookmarks, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "bookmarks/partials/bookmark_list.html", {
            "bookmarks": page_obj.object_list,
            "page_obj": page_obj,
            "query": query,
        })