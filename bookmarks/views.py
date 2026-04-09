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
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
# Create your views here.

class AddBookmarkView(LoginRequiredMixin, View):

    def post(self, request):
        form = BookmarkForm(request.POST)
        if not form.is_valid():
            return self.render_with_errors(request, form)

        url = form.cleaned_data["url"]
        custom_name = form.cleaned_data.get("custom_name")
        if not url.startswith("http"):
            url = "https://" + url
        validator = URLValidator()
        try:
            validator(url)
        except ValidationError:
            form.add_error("url", "Enter a valid URL (include domain like google.com)")
            return self.render_with_errors(request, form)

        if Bookmark.objects.filter(user=request.user, url=url).exists():
            form.add_error("url", "This bookmark already exists")
            return self.render_with_errors(request, form)
        try:
            data = scrape_url(url)
            Bookmark.objects.create(
                user=request.user,
                url=url,
                title=data["title"],
                description=data["description"],
                favicon=data["favicon"],
                custom_name=custom_name,
            )
        except Exception as e:
            form.add_error("url", "Could not fetch site data")
            return self.render_with_errors(request, form)
        return redirect("bookmarks:home")
    
    def render_with_errors(self, request, form):
        bookmarks = Bookmark.objects.filter(user=request.user)

        return render(request, "bookmarks/home.html", {
            "form": form,
            "bookmarks": bookmarks,
        })
    
class BookmarkListView(LoginRequiredMixin,ListView):
    model=Bookmark
    template_name="bookmarks/home.html"
    context_object_name="bookmarks"
    paginate_by=9
    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["form"]=BookmarkForm()
        return context
    
def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(user=request.user)

    paginator = Paginator(bookmarks, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "bookmarks/partials/bookmark_list.html", {
        "bookmarks": page_obj,
        "page_obj": page_obj,
    })

def search_bookmarks(request):
    query=request.GET.get("q","")
    page_number = request.GET.get("page",1)
    bookmarks=Bookmark.objects.filter(user=request.user)
    if query:
        bookmarks=bookmarks.filter(
            Q(title__icontains=query) | 
            Q(custom_name__icontains=query) |
            Q(url__icontains=query)|
            Q(description__icontains=query)
        )
    paginator = Paginator(bookmarks, 9)
    try:
        page_obj = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)
    return render(request,template_name="bookmarks/partials/bookmark_list.html",context={
                                                                        "bookmarks": page_obj.object_list,
                                                                        "page_obj": page_obj,
                                                                        "query": query})
def delete_bookmark(request, pk):
    bookmark = Bookmark.objects.get(id=pk, user=request.user)

    if request.method == "POST":
        bookmark.delete()
        query = request.GET.get("q", "")
        bookmarks = Bookmark.objects.filter(user=request.user)
        if query:
            bookmarks = bookmarks.filter(
                Q(title__icontains=query) |
                Q(custom_name__icontains=query) |
                Q(url__icontains=query)
            )
        paginator = Paginator(bookmarks, 9)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "bookmarks/partials/bookmark_list.html", {
            "bookmarks": page_obj.object_list,
            "page_obj": page_obj,
            "query": query,
        })