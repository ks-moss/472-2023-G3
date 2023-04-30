import TrafficSimulation2 as func
import unittest

class TestElement(unittest.TestCase):
    
    # Test element equals
    def test_correct_element_type(self):
        elem = func.Element(elementType="TRAFFIC LIGHT")
        self.assertEqual(elem.elementType, "TRAFFIC LIGHT")
        
    # Test element mismatch
    def test_invalid_element_type(self):
        with self.assertRaises(AssertionError):
            elem = func.Element(elementType="INVALID")
        
    # Testing adding attributes to elements
    def test_append_attribute(self):
        elem = func.Element(attributeTypeList=["color"], attributeValueList=["red"])
        elem.Append("position", (0,0))
        self.assertEqual(elem["position"], (0,0))
        
    # Testing getter
    def test_get_existing_attribute(self):
        elem = func.Element(attributeTypeList=["color"], attributeValueList=["red"])
        self.assertEqual(elem["color"], "red")
        
    # Test getter (element that does not exist)
    def test_get_nonexisting_attribute(self):
        elem = func.Element(attributeTypeList=["color"], attributeValueList=["red"])
        with self.assertRaises(AssertionError):
            elem["position"]

    # Testing empty attributes        
    def test_empty_attribute_lists(self):
        elem = func.Element()
        self.assertEqual(len(elem.attributeListDictionary), 0)

unittest.main()