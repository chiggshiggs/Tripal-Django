from django.contrib import admin
from .models import Location, Participant, Request, Transport, Trip

# Register your models here.
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)
    list_per_page = 25

class TransportAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)
    list_per_page = 25

class TripAdmin(admin.ModelAdmin):
    list_display = ('start', 'end', 'transport', 'created_by', 'date')
    list_display_links = ('start', 'end', 'transport', 'created_by')
    search_fields = ('start__name', 'end__name', 'transport__name', 'created_by__username', 'date')
    list_per_page = 25

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('trip', 'user')
    list_display_links = ('trip', 'user')
    search_fields = ('user__username',)
    list_per_page = 25

class RequestAdmin(admin.ModelAdmin):
    list_display = ('trip', 'description', 'created_by')
    list_display_links = ('trip', 'created_by')
    search_fields = ('created_by__username',)
    list_per_page = 25

# Register your models here.
admin.site.register(Location, LocationAdmin)
admin.site.register(Transport, TransportAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Request, RequestAdmin)
