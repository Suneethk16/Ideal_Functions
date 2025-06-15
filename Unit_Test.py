"""
Unit tests
These tests validate the correctness of:
1. Ideal function selection based on least squares.
2. Mapping of test data based on the allowed deviation threshold.
"""

import unittest
import pandas as pd
from Processor import Process

class TestProcess(unittest.TestCase):
    """
    Test for verifying the logic in the Process class.
    """
    def setUp(self):
        """
        Prepare trial datasets for training, ideal, and test cases.
        This runs before each test to ensure consistent test data.
        """
        self.traindataset = pd.DataFrame({
            'x': [1, 2, 3],
            'y1': [2, 3, 4],
            'y2': [0, 0, 0],
            'y3': [0, 0, 0],
            'y4': [0, 0, 0],
        })

        self.idealdataset = pd.DataFrame({
            'x': [1, 2, 3],
            'y10': [2.1, 3.1, 4.1],  
            'y20': [10, 10, 10],
            'y30': [0, 0, 0],
            'y40': [0, 0, 0],
            'y50': [-5, -5, -5],
        })

        self.testdataset = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [2.15, 3.05, 4.0]  
        })

    def test_ideal_functions(self):
        """
        Tests that the correct ideal functions are selected for training data.
        """
        processor = Process(self.traindataset, self.idealdataset, self.testdataset)
        selected = processor.idealfunctions()
        self.assertEqual(len(selected), 4)
        self.assertIn('y1', selected)
        self.assertEqual(selected['y1'], 'y10')

    def test_map_test_data(self):
        """
        Tests that all test data points are correctly mapped to ideal functions.
        """
        processor = Process(self.traindataset, self.idealdataset, self.testdataset)
        selected = processor.idealfunctions()
        mappeddata, unmapped = processor.mapdata(selected)

        # All points should be mapped
        self.assertEqual(len(mappeddata), 3)
        self.assertEqual(len(unmapped), 0)
        self.assertTrue('delta_y' in mappeddata.columns)
        self.assertTrue(all(mappeddata['delta_y'] <= processor.max_deviations['y10'] * 2 ** 0.5))

if __name__ == '__main__':
    unittest.main()
