from django import forms
from timeline.models import RestaurantTimelineComment, MenuTimelineComment


class RestaurantTimelineCommentForm(forms.ModelForm):
    class Meta:
        model = RestaurantTimelineComment
        fields = (
            'restaurant_timeline',
            'comment',
            'writer'
        )


class MenuTimelinCommentForm(forms.ModelForm):
    class Meta:
        model = MenuTimelineComment
        fields = (
            'menu_timeline',
            'comment',
            'writer'
        )
