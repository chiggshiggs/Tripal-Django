from django.db import models
import geocoder

mapbox_access_token = 'pk.eyJ1IjoiY2hpZ2dzaGlnZ3MiLCJhIjoiY2xtYzEyZWc3MHBtejNscHhmeXc4enFsMCJ9.zC7lAw-zCPnQjpDsqL0ruw'

# Create your models here.
class Address(models.Model):
    address = models.TextField()
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)

    def save(self,*args,**kwargs):
        g = geocoder.mapbox(self.address, key=mapbox_access_token)
        g = g.latlng
        self.lat = g[0]
        self.long = g[1]
        return super(Address,self).save(*args,**kwargs)
    
