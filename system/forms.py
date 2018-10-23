from django import forms
from django.contrib.auth.forms import UserCreationForm
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


class UserCreateForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
