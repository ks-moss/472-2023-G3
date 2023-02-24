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
        self.vehicleGeneratorList = []
        self.errorList = []          

    def ReadElementsFromFile(self, fileName):
        tree = ET.parse(fileName)
        root = tree.getroot()

        for elem in root:
            if elem.tag == "ROAD":
                #error checking for invalid attributes of element - this is done for each element type
                for subelem in elem:
                    if subelem.tag != "name" and subelem.tag != "length":
                        self.errorList.append("- \"" + subelem.tag + "\" is not an acceptable attribute of \"" + elem.tag + "\"")
                name = elem.find("name").text
                length = int(elem.find("length").text)
                self.roadList.append({"name": name, "length": length})
            elif elem.tag == "TRAFFICLIGHT":
                for subelem in elem:
                    if subelem.tag != "road" and subelem.tag != "position" and subelem.tag != "cycle":
                        self.errorList.append("- \"" + subelem.tag + "\" is not an acceptable attribute of \"" + elem.tag + "\"")
                road = elem.find("road").text
                position = int(elem.find("position").text)
                cycle = int(elem.find("cycle").text)
                self.trafficLightList.append({"road": road, "position": position, "cycle": cycle})
            elif elem.tag == "VEHICLE":
                type = None #if a type is recognized it will be updated - these can be removed down the road when/if type becomes required
                for subelem in elem:
                    if subelem.tag != "road" and subelem.tag != "position" and subelem.tag != "speed" and subelem.tag != "acceleration" and subelem.tag != "type":
                        self.errorList.append("- \"" + subelem.tag + "\" is not an acceptable attribute of \"" + elem.tag + "\"")
                    if subelem.tag == "type":
                        type = elem.find("type").text   #recognized a type in the vehicle element so found it - finding when its not there throws an error
                road = elem.find("road").text
                position = int(elem.find("position").text)
                speed = int(elem.find("speed").text)
                acceleration = int(elem.find("acceleration").text)
                self.vehicleList.append({"road": road, "position": position, "speed": speed, "acceleration": acceleration, "type": type})
            elif elem.tag == "VEHICLEGENERATOR":
                type = None 
                for subelem in elem:
                    if subelem.tag != "name" and subelem.tag != "frequency" and subelem.tag != "type":
                        self.errorList.append("- \"" + subelem.tag + "\" is not an acceptable attribute of \"" + elem.tag + "\"")
                    if subelem.tag == "type":
                        type = elem.find("type").text
                name = elem.find("name").text
                frequency = int(elem.find("frequency").text)
                self.vehicleGeneratorList.append({"name": name, "frequency": frequency, "type": type})
            #checking for unacceptable element input
            else:
                self.errorList.append("- \"" + elem.tag + "\" is not an acceptable element")
