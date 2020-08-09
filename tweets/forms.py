from django import forms

from tweets.models import Tweet

TWEET_MAX_LENGTH = 250

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']

    # Ensure that the tweet content will not exceed 250 characters.
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > TWEET_MAX_LENGTH:
            raise forms.ValidationError("This Tweet is too long")
        elif len(content) == 0:
            raise forms.ValidationError("Tweet is empty!")
        return content