from django.shortcuts import render, redirect

from .models import Flight,Passenger

# Create your views here.

def index(request):
    return render(request,"flights/index.html",{
        "flights":Flight.objects.all()
    })

def flight(request,flight_id):
    flight = Flight.objects.get(id=flight_id)
    return render(request,"flights/flight.html",{
        "flight":flight,

        #.passengers uses related_name="passengers" attribute in Passenger Model
        "passengers":flight.passengers.all(),
        #excluding all the passengers whose Flights attribute already includes the current flight
        "nonpassengers":Passenger.objects.exclude(Flights=flight).all()
    })

#function to book flight for passenger
def book(request,flight_id):
    if request.method=="POST":
        flight = Flight.objects.get(id=flight_id)
        passenger = Passenger.objects.get(pk = int(request.POST['passenger']))
        passenger.Flights.add(flight)
        return redirect('flight',flight_id=flight.id)
    else:
        flight = Flight.objects.get(id=flight_id)
        return redirect('flight',flight_id=flight.id)
