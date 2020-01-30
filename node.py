class RoadNode:
    def __init__(self, id, lon, lat):
       self.id =  id
       self.lon = lon
       self.lat = lat
       self.land_node_list = []

    def add_land(self, land_node):
        self.land_node_list.append(land_node)

################################################################################################
        
class LandNode:
    def __init__(self, id, road_node):
        self.id = id
        self.road_node = road_node
        
################################################################################################