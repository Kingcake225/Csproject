from django.shortcuts import render
from django.contrib import messages
from .forms import Location
from .logic.FindLatAndLong import addyToLatAndLong
from .logic.create_network import Map
import folium

def route(request):
    context = {
        'title': 'Loose Change - Best Route',
    }
    
    # Office coordinates (CHS)
    office_coords = (51.45898602638651, -2.6188274814116506)
    
    if request.method == 'POST':
        form = Location(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            
            # Convert address to coordinates
            lat, lon = addyToLatAndLong(address)
            
            if lat and lon:
                start_coords = (lat, lon)
                
                # Create map and find route
                route_map = Map(start_coords, office_coords)
                orig_node, dest_node = route_map.findNearestNode()
                shortest_path = route_map.generateShortestMap(orig_node, dest_node)
                
                # Get the map HTML directly from the Map object
                map_html = route_map.get_map_html()
                
                # Calculate the route distance
                distance = route_map.calculate_route_distance(shortest_path)
                
                # Add results to context
                context.update({
                    'form': form,
                    'map_html': map_html,
                    'distance': distance
                })
            else:
                context.update({
                    'form': form,
                    'error': 'Could not find coordinates for the provided address. Please check the address and try again.'
                })
                messages.error(request, 'Could not find coordinates for the provided address. Please check the address and try again.')
    else:
        form = Location()
        context['form'] = form
    
    return render(request, 'distanceToOffice/route.html', context)
