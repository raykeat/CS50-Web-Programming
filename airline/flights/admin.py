from django.contrib import admin
from .models import Airport,Flight,Passenger

# Register your models here.

#specifying the display settings for admin interface
class FlightAdmin(admin.ModelAdmin):
    list_display=("id","origin","destination","duration")

class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("Flights",)


#So that can use admin app to manipulate Flight and Airports and Passenger table
admin.site.register(Airport)

#use FlightAdmin settings when registering the flight
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passenger,PassengerAdmin)


