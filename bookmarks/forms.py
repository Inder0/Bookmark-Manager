from django import forms
from .models import Bookmark

class BookmarkForm(forms.Form):
    url=forms.URLField(
        widget=forms.URLInput(attrs={
            "class": "input",
            "placeholder": "Enter URL (https://...)"
        })
    )
    custom_name = forms.CharField(
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter"
        })
    )