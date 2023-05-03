from django.db import models

# Create your models here.
# each model maps to a single database table (flights table, passengers table, countryid table)
# django model documentation: https://docs.djangoproject.com/en/4.2/topics/db/models/


class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city}({self.code})"
    
class Flight(models.Model):
    # related_name attribute on the foreign key fields allows for reverse lookups 
    # from an Airport object to a set of related Flight objects.
    origin = models.ForeignKey(Airport,on_delete=models.CASCADE,related_name="Departures")
    destination = models.ForeignKey(Airport,on_delete=models.CASCADE,related_name="Arrivals")
    duration = models.IntegerField()

    #returns a string representation of the object
    def __str__(self):
        return f"{self.id}:{self.origin} to {self.destination}"
    
class Passenger(models.Model):
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    #blank=True allows possibility that passenger has no flight
    #related_ name attribute allows for reverse lookups from Flight object to passenger)
    Flights = models.ManyToManyField(Flight,blank=True,related_name="passengers")

    #returns a string representation of passenger object
    def __str__(self):
        return f"{self.firstname} {self.lastname}"



