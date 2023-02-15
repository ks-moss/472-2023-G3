# Element class
# attributes:
#	attributeListDictionary - dictionary of attributes
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
	def __init__(self, attributeTypeList = [], attributeValueList = []):
		assert len(attributeTypeList) == len(attributeValueList)
		self.attributeListDictionary = {}
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
	#	attributeListDictionary.__str__()
	def __str__(self):
		return self.attributeListDictionary.__str__()

# TrafficSystem class
# attributes:
#	elementList - list of Element objects
# methods:
#	GetElementsByAttributeType
#	PrintElements
#	AppendElement
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