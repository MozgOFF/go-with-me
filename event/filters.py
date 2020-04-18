from django_filters import rest_framework as filters
from .models import Event


class EventFilter(filters.FilterSet):
    price = filters.RangeFilter(field_name='price')
    # TODO Check with `IsoDateTimeFromToRangeFilter`
    start = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Event
        fields = ['categories', 'price', 'start', ]
