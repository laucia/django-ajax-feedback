from django import forms
from feedback.models import AnonymousFeedback, Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ('user','context_url','browser')


class AnonymousFeedbackForm(forms.ModelForm):
    class Meta:
        model = AnonymousFeedback
        exclude = ('user','context_url','browser')
