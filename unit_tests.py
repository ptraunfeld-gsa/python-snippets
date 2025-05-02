import unittest
from rules_engine import RequestFact, has_one_extension_id, has_valid_chrome_extension_id

class ExampleUnitTests(unittest.TestCase):
    def test_has_one_extension_id_true(self):
        # Arrange
        fact = RequestFact(chrome_extension_id="123")

        # Act
        result = has_one_extension_id(fact) 
        
        # Assert
        self.assertTrue(result)

    def test_has_one_extension_id_false(self):
        # Arrange
        fact = RequestFact(chrome_extension_id="123, 456")

        # Act
        result = has_one_extension_id(fact) 
        
        # Assert
        self.assertFalse(result)


# Run with `python unit_tests.py` or `python -m unittest unit_tests`
if __name__ == "__main__":
    unittest.main()