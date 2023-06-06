from django.test import TestCase, Client
from .models import Airport, Flight, Passenger
from django.db.models import Max


# Create your tests here.
class FlightTestCase(TestCase):
    def setUp(self):

        # Create airports.
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        # Create flights.
        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=200)
        Flight.objects.create(origin=a1, destination=a2, duration=-100)

    #function to test flight(departure) count
    def test_departure_count(self):
        a = Airport.objects.get(code='AAA')
        self.assertEqual(a.Departures.count(),3)

    #function to test if flight is valid
    def test_flight_validity(self):
        a1=Airport.objects.get(code="AAA")
        a2=Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1,destination=a2,duration=100)
        self.assertTrue(f.is_valid_flight)

    #function to test validity of flight destination  
    def test_invalid_flight_destination(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())



    #function to test that particular web pages work
    def test_index(self):

        # Set up client to make requests
        c = Client()
        # Send get request to index page and store response
        response = c.get("/flights/")
        # Make sure status code is 200
        self.assertEqual(response.status_code, 200)
        # Make sure three flights are returned in the context
        self.assertEqual(response.context["flights"].count(), 3)
    
    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_flight_page(self):
        invalid_id = -1  # Use an invalid ID

        c = Client()
        response = c.get(f"/flights/{invalid_id}")
        self.assertEqual(response.status_code, 404)
    


    def test_flight_page_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(firstname="Alice", lastname="Adams")
        f.passengers.add(p)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)




    

    





        
