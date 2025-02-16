from create_network import Map
from FindLatAndLong import addyToLatAndLong

destlatitude, destlongitude = addyToLatAndLong('35-37 Stanley Rd, Redland, Bristol BS6 6NP') # Doesn't Produce Accurate Results

start_coords = (destlatitude, destlongitude)
end_coords = (51.45898602638651, -2.6188274814116506)  # CHS

Map1 = Map(start_coords, end_coords)
orig_node, dest_node = Map1.findNearestNode()
Map1.generateShortestMap(orig_node, dest_node) # creates folium map in html format