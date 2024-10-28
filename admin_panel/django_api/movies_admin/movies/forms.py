from .models import FilmWork
from django.forms import ModelForm


class FilmForm(ModelForm):

    class Meta:
        model = FilmForm
        fields = ('title', 'description', 'creation_date', 'rating', 'type')