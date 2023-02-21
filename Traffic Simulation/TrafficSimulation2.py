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

    def ReadElementsFromFile(self, fileName):
        tree = ET.parse(fileName)
        root = tree.getroot()

        for elem in root:
            if elem.tag == "ROAD":
                #error checking for invalid attributes of element - this is done for each element type
                for subelem in elem:
                    if subelem.tag != "name" and subelem.tag != "length":
                        print("Bad Input Found: \"",subelem.tag,"\" is not an acceptable attribute of \"",elem.tag,"\"") 
                name = elem.find("name").text
                length = int(elem.find("length").text)
                self.roadList.append({"name": name, "length": length})
            elif elem.tag == "TRAFFICLIGHT":
                for subelem in elem:
                    if subelem.tag != "road" and subelem.tag != "position" and subelem.tag != "cycle" and (subelem.tag == "type" and not subelem.text):
                        print("Bad Input Found: \"",subelem.tag,"\" is not an acceptable attribute of \"",elem.tag,"\"")
                road = elem.find("road").text
                position = int(elem.find("position").text)
                cycle = int(elem.find("cycle").text)
                type = elem.find("type").text if elem.find("type") is not None else None
                self.trafficLightList.append({"road": road, "position": position, "cycle": cycle, "type": type})
            elif elem.tag == "VEHICLE":
                for subelem in elem:
                    if subelem.tag != "road" and subelem.tag != "position" and (subelem.tag == "type" and not subelem.text):
                        print("Bad Input Found: \"",subelem.tag,"\" is not an acceptable attribute of \"",elem.tag,"\"")
                road = elem.find("road").text
                position = int(elem.find("position").text)
                type = elem.find("type").text if elem.find("type") is not None else None
                self.vehicleList.append({"road": road, "position": position, "type": type})
            elif elem.tag == "VEHICLEGENERATOR":
                for subelem in elem:
                    if subelem.tag != "name" and subelem.tag != "frequency" and (subelem.tag == "type" and not subelem.text):
                        print("Bad Input Found: \"",subelem.tag,"\" is not an acceptable attribute of \"",elem.tag,"\"")
                name = elem.find("name").text
                frequency = int(elem.find("frequency").text)
                type = elem.find("type").text if elem.find("type") is not None else None
                self.vehicleGeneratorList.append({"name": name, "frequency": frequency, "type": type})
            #checking for unacceptable element input
            else:
                print("Bad Input Found: \"",elem.tag, "\" is not an acceptable element")
