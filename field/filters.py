from django_filters import rest_framework as filters

from field.models import Field


class FieldFilter(filters.FilterSet):
    available_from = filters.DateTimeFilter(method='filter_by_availability')

    class Meta:
        model = Field
        fields = ['available_from']

    def filter_by_availability(self, queryset, name, value):
        return queryset.filter(
            booking__start_time__gte=value
        ).distinct()
