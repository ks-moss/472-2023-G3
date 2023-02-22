# Element class
# attributes:
#	attributeListDictionary - dictionary of attributes
#	elementType - 
# methods:
#	Append
#	__getitem__ overload
#	__str__ overload
class Element:
	# Constructor
	# parameters:
	#	attributeTypeList - list of dictionary keys
	#	attributeValueList - list of dictionary values
	# precondition:
	#	new Element instance does not exist
	# postcondition:
	#	new Element instance exists with attributeValueList
	#	defined by parameters
	def __init__(self, elementType = "VEHICLE", attributeTypeList = [], attributeValueList = []):
		assert len(attributeTypeList) == len(attributeValueList)
		assert (elementType in ["VEHICLE", "TRAFFIC LIGHT", "ROAD", "VEHICLE GENERATOR"])
		self.attributeListDictionary = {}
		self.elementType = elementType
		for i in range(0, len(attributeTypeList)):
			self.attributeListDictionary.update({attributeTypeList[i]: attributeValueList[i]})
	# Append
	# parameters:
	#	attributeType
	#	attributeValue
	# precondition:
	#	none
	# postcondition:
	#	attributeListDictioary has been updated
	#	with a new entry defined by the
	#	parameters
	def Append(self, attributeType, attributeValue):
		self.attributeListDictionary.update({attributeType: attributeValue})
	# __getitem__
	# parameters:
	#	attributeType
	# precondition:
	# 	attributeValueList contains an entry with the [attributeType] key
	# postcondition:
	#	none
	# returns:
	#	the value referenced by the [attributeType] key
	def __getitem__(self, attributeType):
		assert (attributeType in self.attributeListDictionary)
		return self.attributeListDictionary[attributeType]
	# __str__
	# parameters:
	#	none
	# precondition:
	#	none
	# postcondition:
	#	none
	# returns:
	#	Element properties cast as a string
	def __str__(self):
		return (self.elementType, self.attributeListDictionary).__str__()

# TrafficSystem class
# attributes:
#	elementList - list of Element objects
# methods:
#	GetElementsByAttributeType
#	PrintElements
#	AppendElement
#	ReadElementsFromFile
class TrafficSystem:
	# Constructor
	# parameters:
	#	elementList - list of Element objects
	# precondition:
	#	new TrafficSystem instance does not exist
	# postcondition:
	#	new TrafficSystem exists with elementList
	def __init__(self, elementList = []):
		self.elementList = elementList
	# GetElementsByAttributeValue
	# parameters:
	#	elementAttributeType
	#	elementAttributeValue
	# precondition:
	#	none
	# postcondition:
	#	none
	# returns:
	#	list of Element objects which contain an
	#	attribute key/value pair of [elementAttributeType]
	#	and [elementAttributeValue]
	def GetElementsByAttributeValue(self, elementAttributeType, elementAttributeValue):
		output = []
		for e in self.elementList:
			if (e[elementAttributeType] == elementAttributeValue):
				output.append(e)
		return output
	# AppendElement
	# parameters:
	#	element
	# precondition:
	#	none
	# postcondition:
	#	elementList now contains [element]
	def AppendElement(self, element):
		self.elementList.append(element)
	# ReadAttributesFromString
	# parameters:
	#	input
	# precondition:
	#	input contains a formatted Attribute description
	# postcondition:
	#	input no longer contains the formatted Attribute description
	# returns:
	#	input
	#	attributeTypeList
	#	attributeValueList
	def ReadAttributesFromString(self, input):
		attributeTypeList = []
		attributeValueList = []
		while (True):
			openBraceIndex = 0
			while (input[openBraceIndex] != '<'):
				openBraceIndex += 1
			#assert (openBraceIndex < len(input))
			if(openBraceIndex >= len(input)):
				print("Input not properly formatted, data may not have been read")
				return
			input = input[openBraceIndex:]
			openBraceIndex = 0
			closeBraceIndex = openBraceIndex + 1
			while (input[closeBraceIndex] != '>'):
				if (input[closeBraceIndex] == '/'):
					return (input, attributeTypeList, attributeValueList)
				closeBraceIndex += 1
			#assert (closeBraceIndex < len(input))
			if(closeBraceIndex >= len(input)):
				print("Input not properly formatted, data may not have been read")
				return
			attributeTypeList.append(input[openBraceIndex + 1: closeBraceIndex])
			input = input[closeBraceIndex + 1:]
			openBraceIndex = 0
			while (input[openBraceIndex] != '<'):
				openBraceIndex += 1
			#assert (openBraceIndex < len(input))
			if(openBraceIndex >= len(input)):
				print("Input not properly formatted, data may not have been read")
				return
			attributeValueList.append(input[:openBraceIndex])
			closeBraceIndex = openBraceIndex + 1
			while (input[closeBraceIndex] != '>'):
				closeBraceIndex += 1
			#assert (closeBraceIndex < len(input))
			if(closeBraceIndex >= len(input)):
				print("Input not properly formatted, data may not have been read")
				return
			assert (input[openBraceIndex + 1: closeBraceIndex] == "/" + attributeTypeList[len(attributeTypeList) - 1])
			input = input[closeBraceIndex + 1:]
	# ReadElementsFromString
	# parameters:
	#	input
	# precondition:
	#	input contains a formatted TrafficSystem description
	# postcondition:
	#	TrafficSystem contains Elements described in file
	def ReadElementsFromString(self, input):
		while (input != ""):
			openBraceIndex = 0
			while (input[openBraceIndex] != '<'):
				openBraceIndex += 1
				if (openBraceIndex >= len(input)):
					return
			#assert (openBraceIndex < len(input))
			if(openBraceIndex >= len(input)):
				print("Input not properly formatted, data may not have been read")
				return
			input = input[openBraceIndex:]
			openBraceIndex = 0
			closeBraceIndex = openBraceIndex + 1
			while (input[closeBraceIndex] != '>'):
				closeBraceIndex += 1
			#assert (closeBraceIndex < len(input))
			if(closeBraceIndex >= len(input)):
				print("Input not properly formatted, data may not have been read")
				return
			elementType = input[openBraceIndex + 1: closeBraceIndex]
			assert (elementType != "")
			input = input[closeBraceIndex + 1:]
			input, attributeTypeList, attributeValueList = self.ReadAttributesFromString(input)
			assert(input != "")
			openBraceIndex = 0
			while (input[openBraceIndex] != '<'):
				openBraceIndex += 1
			#assert(openBraceIndex < len(input))
			if(openBraceIndex >= len(input)):
				print("Input not properly formatted, data may not have been read")
				return
			closeBraceIndex = openBraceIndex + 1
			while (input[closeBraceIndex] != '>'):
				closeBraceIndex += 1
			assert (input[openBraceIndex + 1: closeBraceIndex] == "/" + elementType)
			element = Element(elementType, attributeTypeList, attributeValueList)
			self.AppendElement(element)
			input = input[closeBraceIndex + 1:]
	# ReadElementsFromFile
	# parameters:
	#	filename
	# precondition:
	#	file exists with formatted TrafficSystem description
	# postcondition:
	#	TrafficSystem contains Elements described in file
	def ReadElementsFromFile(self, filename):
		file = open(filename, "r")
		fileString = file.read()
		file.close()
		self.ReadElementsFromString(fileString)


#mySystem = TrafficSystem()
#mySystem.ReadElementsFromFile("InputFiles/trafficSim1.xml")