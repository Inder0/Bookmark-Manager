from django import forms
from .models import Bookmark

class BookmarkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ["url", "custom_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["url"].widget.attrs.update({
            "class": "w-full sm:flex-1 bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500",
            "placeholder": "https://example.com",
            "type":"text",
        })

        self.fields["custom_name"].widget.attrs.update({
            "class": "w-full sm:w-64 bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500",
            "placeholder": "Type name",
        })