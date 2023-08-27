import django_filters
from django_filters import DateFilter, CharFilter, DateFromToRangeFilter, OrderingFilter, ModelChoiceFilter
from django_filters.widgets import RangeWidget
from django import forms

from .models import *

class MoodChoiceFilter(django_filters.ChoiceFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('field_name', 'mood')
        kwargs.setdefault('label', 'Mood')
        choices = UserContent._meta.get_field('mood').choices
        kwargs.setdefault('choices', choices)
        kwargs.setdefault('widget', forms.Select(attrs={'label': 'choices'}))
        super().__init__(*args, **kwargs)

class FeelingChoiceFilter(django_filters.ChoiceFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('field_name', 'feeling')
        kwargs.setdefault('label', 'Intensity')
        choices = [(str(i), str(i)) for i in range(1, 11)]  # Assuming feeling choices are from 1 to 10
        kwargs.setdefault('choices', choices)
        kwargs.setdefault('widget', forms.Select())
        super().__init__(*args, **kwargs)

class EntryFilter(django_filters.FilterSet):
    body_text = CharFilter(field_name="title", label='title', lookup_expr='icontains')
    mood = MoodChoiceFilter()
    feeling = FeelingChoiceFilter()
    date_range = DateFromToRangeFilter(field_name="created_at", label = 'Published', widget=RangeWidget(attrs={'placeholder': 'MM/DD/YYYY'}))

    class Meta:
        model = UserContent
        fields='__all__'
        exclude = ['author', 'mood','feeling', 'title', 'content', 'created_at', 'updated_at', 'graditude']

class ModEntryFilter(django_filters.FilterSet):
    body_text = CharFilter(field_name="title", label='title', lookup_expr='icontains')
    mood = MoodChoiceFilter()
    feeling = FeelingChoiceFilter()
    date_range = DateFromToRangeFilter(field_name="created_at", label = 'Published', widget=RangeWidget(attrs={'placeholder': 'MM/DD/YYYY'}))

    class Meta:
        model = UserContent
        fields='__all__'
        exclude = [ 'mood','feeling', 'title', 'content', 'created_at', 'updated_at', 'graditude']