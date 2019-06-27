from django.contrib.gis import admin

from .models import Sensor, SensorData


@admin.register(Sensor)
class SensorAdmin(admin.OSMGeoAdmin):
    list_display = ['name', 'position']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset


@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ['pk', 'sensor', 'position', 'timestamp',
        'fahrenheit', 'humidity']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('sensor')
        return queryset