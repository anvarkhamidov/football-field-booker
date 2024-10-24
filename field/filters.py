from django_filters import rest_framework as filters

from field.models import Field


class FieldFilter(filters.FilterSet):
    available_from = filters.DateTimeFilter(method="filter_available_from")
    available_to = filters.DateTimeFilter(method="filter_available_to")
    price_per_hour = filters.RangeFilter(method="price_per_hour")
    latitude = filters.CharFilter(method="filter_geo")
    longitude = filters.CharFilter(method="filter_geo")

    class Meta:
        model = Field
        fields = [
            "available_from",
            "available_to",
            "latitude",
            "longitude",
            "price_per_hour",
        ]

    def filter_available_from(self, queryset, name, value):
        return queryset.filter(booking__start_time__gte=value).distinct()

    def filter_available_to(self, queryset, name, value):
        return queryset.filter(booking__start_time__lte=value).distinct()

    def filter_price_per_hour(self, queryset, name, value):
        return queryset.filter(
            hourly_rate__gte=value.start, hourly_rate__lte=value.stop
        ).distinct()

    def filter_geo(self, queryset, name, value):
        return queryset
