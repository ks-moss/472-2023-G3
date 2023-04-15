#3.7 Simulation of intersections

# Goal:
# A road can contain intersections. Vehicles must choose which road to follow at an intersection.
# You also need to implement use case 1.5 for this.

# Precondition:
# The system contains a sceme of the virtual traffic network. This scheme contains at least 2 roads and 1 intersection.
# Postcondition:Vehicles choose a road at each intersection.

# Notes:
# If the position of an intersection on a road is equal to the length of the road, then the road ends at that intersection. 
# Vehicles will therefore not be able to choose this road at this intersection. 
# If the position of an intersection on a road is zero, then the road starts at that intersection.

# Atributes:
#   trafficSystem
#       - AutomaticSimulation
#   vehicle_state
#       - vehicle list (Vehicles choose a road at each intersection) 
#   trafficlight_state
#       - Store state of all intersections
# Methods:
#   is_approaching_N_selected_road
#       - First check if the vehicle is on thesame road as the intersection is located
#       - Secondly, check if the current position of hte vehicle is approaching the intersection
#           - If yes, then make a choice the swap the road
#           - If no, keep searching


class IntersectionSim:

    def __init__(self, intersections_data, roads_data):
        self.intersection_list = intersections_data
        self.road_list = roads_data

        

    def is_approaching_N_selected_road(self, vehicle_road, vehicle_position):

        selected_road = vehicle_road
        get_position = vehicle_position

        for i in range(len(self.intersection_list)):
            for j in range(len(self.intersection_list[i])):

                trafficlight_position = (self.intersection_list[i][j]["position"])
                
                     
                 # Check if vehicle is on the same road as the intersection
                if (vehicle_road == self.intersection_list[i][j]["road"] and vehicle_position < trafficlight_position + 0.18):
                    # print("______________________________________________________")
                    # print("| VEHICLE IS APPROACHING THE INTERSECTION(S)")
                    # print("______________________________________________________")
                    # print("| Vehicle on Road:", vehicle_road)
                    # print("| Vehicle Position: ",  get_position)
                    # print("| Traffic Light on Road:", self.intersection_list[i][j]["road"])
                    # print("| Intersection Position: ", trafficlight_position)
                    # print("______________________________________________________\n")
                          
                    if (vehicle_position > trafficlight_position): 

                        if(j == 0):       
                            selected_road = self.intersection_list[i][1]["road"]      
                        if(j == 1):
                            selected_road = self.intersection_list[i][0]["road"]
                    
                        # Update position after making a turn
                        for k in range(len(self.road_list)):
                            if(selected_road == self.road_list[k]["name"]):
                                get_position = self.road_list[k]["length"] - vehicle_position

                        # print("------------------------| Vehivle make a TURN to: ", selected_road)
                        # print("------------------------| Current Position: ", get_position)
                        # print("______________________________________________________\n")
    
        return selected_road, get_position

       

    def update(self):
        self.is_approaching_N_selected_road()
        
        
# interSim = IntersectionSim()   


# t_end = time.time() + 60 * 15
# while time.time() < t_end:
#     interSim.update()
#     time.sleep(1)


    
            
            



            

    
