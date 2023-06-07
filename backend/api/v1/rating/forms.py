from django.forms import ModelForm
from .models import Movie


class FileUploadForm(ModelForm):
    class Meta:
        model = Movie
        fields = ["title", "file"]
