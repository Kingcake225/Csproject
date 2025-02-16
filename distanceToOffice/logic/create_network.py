import networkx as nx
import osmnx as ox
import folium

class Map:
    def __init__(self, start_coords, end_coords): # Start coords must be given at tuple
        self.start_coords = start_coords
        self.end_coords = end_coords
        self.network = ox.graph_from_point(start_coords, dist=1000, network_type='drive') # dist is buffer distance, only road networks, doesn't account for walking

    def convertToAdjacencyList(self):
        nx.write_multiline_adjlist(self.network, 'network.adjlist')

    def findNearestNode(self):

        orig_node = ox.distance.nearest_nodes(self.network, self.start_coords[1], self.start_coords[0])
        dest_node = ox.distance.nearest_nodes(self.network, self.end_coords[1], self.end_coords[0])
        return orig_node, dest_node

    # Current implementation only shows shortest driving route, not walking, because shit takes to long to load otherwise
    def generateShortestMap(self, orig_node, dest_node):
        self.shortest_path = nx.dijkstra_path(self.network, orig_node, dest_node, weight='length')
        
        self.m = folium.Map(location=self.start_coords, zoom_start=15)
        
        route_coords = [(self.network.nodes[node]['y'], self.network.nodes[node]['x']) for node in self.shortest_path]
        
        folium.PolyLine(route_coords, color='blue', weight=5).add_to(self.m)
        
        folium.Marker(
            location=self.start_coords,
            popup='Start',
            icon=folium.Icon(color='green')
        ).add_to(self.m)
        
        folium.Marker(
            location=self.end_coords,
            popup='End',
            icon=folium.Icon(color='red')
        ).add_to(self.m)
        
        return self.shortest_path

    def get_map_html(self):
        return self.m._repr_html_()
        
    def calculate_route_distance(self, path):
        length = nx.path_weight(self.network, path, weight='length')
        return length / 1000  # Convert meters to kilometers

if __name__ == '__main__': # Only run if file being run directly as opposed to being run when called as a module.
    # Origin location and destination
    #start_coords = ()
    end_coords = (51.45898602638651, -2.6188274814116506) # CHS

    #Map1 = Map(start_coords, end_coords)
    #orig_node, dest_node = Map1.findNearestNode()
    #Map1.generateShortestMap(orig_node, dest_node) # creates folium map in html format

    #Map1.convertToAdjacencyList()
