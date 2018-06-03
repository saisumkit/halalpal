from django import forms
from .models import Review


RATING_LEVEL = (
    (1,'Rating 1'),
    (2,'Rating 2'),
    (3,'Rating 3'),
    (4,'Rating 4'),
    (5,'Rating 5'),
)

class ReviewForm( forms.ModelForm ):
    body = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 2, 'cols': 40}))
    rating = forms.ChoiceField(  required = True, choices = RATING_LEVEL )

    class Meta:
        model = Review
        fields = [ 'body', 'rating']
