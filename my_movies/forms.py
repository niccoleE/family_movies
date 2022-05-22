from django import forms
from .models import Movie, Comment


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['year', 'description', 'rating',
                  'review', 'img_url']


class SelectForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title']


class AddForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['rating', 'review']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

