from django import forms
from .models import Poll, Choice

class PollAddForm(forms.ModelForm):
    choice1 = forms.CharField(label='choice 1', max_length=100, min_length=2, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    choice2 = forms.CharField(label='choice 2', max_length=100, min_length=2, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    choice3 = forms.CharField(label='choice 3', max_length=100, min_length=2, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    class Meta:
        model = Poll
        fields = ['text', 'choice1', 'choice2', 'choice3']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 50})
        }

class PollEditForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 50})
        }

class ChoiceAddForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
        widgets = {
            'choice_text': forms.TextInput(attrs={'class': 'form-control'})
        }


