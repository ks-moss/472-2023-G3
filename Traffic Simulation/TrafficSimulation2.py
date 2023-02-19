import xml.etree.ElementTree as ET
# Element class
# attributes:
#   attributeListDictionary - dictionary of attributes
#   elementType -
# methods:
#   Append
#   __getitem__ overload
#   __str__ overload

class Element:
    # Constructor
    # parameters:
    #   attributeTypeList - list of dictionary keys
    #   attributeValueList - list of dictionary values
    # precondition:
    #   new Element instance does not exist
    # postcondition:
    #   new Element instance exists with attributeValueList
    #   defined by parameters
    def __init__(self, elementType="VEHICLE", attributeTypeList=[], attributeValueList=[]):
        assert len(attributeTypeList) == len(attributeValueList)
        assert elementType in ["VEHICLE", "TRAFFIC LIGHT", "ROAD", "VEHICLE GENERATOR"]
        self.attributeListDictionary = {}
        self.elementType = elementType
        for i in range(0, len(attributeTypeList)):
            self.attributeListDictionary.update({attributeTypeList[i]: attributeValueList[i]})

    # Append
    # parameters:
    #   attributeType
    #   attributeValue
    # precondition:
    #   none
    # postcondition:
    #   attributeListDictioary has been updated
    #   with a new entry defined by the
    #   parameters
    def Append(self, attributeType, attributeValue):
        self.attributeListDictionary.update({attributeType: attributeValue})

    # __getitem__
    # parameters:
    #   attributeType
    # precondition:
    #   attributeValueList contains an entry with the [attributeType] key
    # postcondition:
    #   none
    # returns:
    #   the value referenced by the [attributeType] key
    def __getitem__(self, attributeType):
        assert attributeType in self.attributeListDictionary
        return self.attributeListDictionary[attributeType]

    # __str__
    # parameters:
    #   none
    # precondition:
    #   none
    # postcondition:
    #   none
    # returns:
    #   attributeListDictionary.__str__()
    def __str__(self):
        return f'{self.elementType} {self.attributeListDictionary}'

# TrafficSystem class
# attributes:
#   roadList - list of roads
#   trafficLightList - list of traffic lights
#  vehicleList - list of vehicles
# methods:
#   GetElementsByAttributeType
#   PrintElements
#   AppendElement
#   ReadElementsFromFile

class TrafficSystem:
    def __init__(self):
        self.roadList = []
        self.trafficLightList = []
        self.vehicleList = []

    def ReadElementsFromFile(self, fileName):
        tree = ET.parse(fileName)
        root = tree.getroot()

        for child in root:
            if child.tag == "ROAD":
                name = child.find("name").text
                length = int(child.find("length").text)
                self.roadList.append({"name": name, "length": length})
            elif child.tag == "TRAFFICLIGHT":
                road = child.find("road").text
                position = int(child.find("position").text)
                cycle = int(child.find("cycle").text)
                self.trafficLightList.append({"road": road, "position": position, "cycle": cycle})
            elif child.tag == "VEHICLE":
                road = child.find("road").text
                position = int(child.find("position").text)
                self.vehicleList.append({"road": road, "position": position})