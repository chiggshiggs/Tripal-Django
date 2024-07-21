from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Address
import requests
# Create your views here.

class AddressView(CreateView):
    model = Address
    fields = ['address']

    template_name = 'addresses/home.html'
    success_url = '/address'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['mapbox_access_token'] = 'pk.eyJ1IjoiY2hpZ2dzaGlnZ3MiLCJhIjoiY2xtYzEyZWc3MHBtejNscHhmeXc4enFsMCJ9.zC7lAw-zCPnQjpDsqL0ruw'
        context['addresses'] = Address.objects.all()
        

        try:
            addresses = Address.objects.all()
            sources = ';'.join([f'{address.long},{address.lat}' for address in addresses])

            # Construct the dynamic URL based on database values
            url = f'https://api.mapbox.com/directions-matrix/v1/mapbox/walking/{sources}?sources=0&destinations=all&annotations=distance,duration&access_token=pk.eyJ1IjoiY2hpZ2dzaGlnZ3MiLCJhIjoiY2xtYzEyZWc3MHBtejNscHhmeXc4enFsMCJ9.zC7lAw-zCPnQjpDsqL0ruw'
            
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()  # Assuming the response contains JSON data
                context['external_data'] = data  # Include the retrieved JSON data in the context
                context['distance_value'] =  data['distances'][0][1]
                context['time_taken'] = data['durations'][0][1]
                
        except requests.exceptions.RequestException as e:
            # Handle any exceptions or errors that may occur during the request
            context['external_data_error'] = str(e)

        return context
