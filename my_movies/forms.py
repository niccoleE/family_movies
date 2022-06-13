from django import forms
from .models import Movie, Comment, Note


class MovieForm(forms.ModelForm):
    rating = forms.FloatField(max_value=10, min_value=0,
                              widget=forms.NumberInput(attrs={'step': "0.5"}))

    class Meta:
        model = Movie
        fields = ['title', 'rating', 'review', 'year', 'description', 'homepage', 'img_url']
        widgets = {'review': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'cols': 60}),
                   'description': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'cols': 60}),
                   }


class AddForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title']


class ReviewForm(forms.ModelForm):
    rating = forms.FloatField(required=True, max_value=10, min_value=0,
                              widget=forms.NumberInput(attrs={'step': "0.5"}))

    class Meta:
        model = Movie
        fields = ['rating', 'review']
        widgets = {'review': forms.Textarea(
            attrs={'class': 'form-control form-control-lg',
                   'cols': 60,
                   'required': True})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(
            attrs={'class': 'form-control form-control-lg', 'cols': 80})
        }


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'rating']
