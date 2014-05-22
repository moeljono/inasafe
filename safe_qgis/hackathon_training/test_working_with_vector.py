__author__ = 'gumbia'

import os
import unittest

from qgis.core import QgsVectorLayer
from safe_qgis.hackathon_training.working_with_vector import load_layer


class TestWorkingWithVector(unittest.TestCase):
    def test_load_layer(self):
        """Test the load_layer function works."""
        vector_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '../../safe/test/data/boundaries/district_osm_jakarta.shp'))
        layer = load_layer(vector_path, 'District OSM Jakarta')
        message = 'It is not a QgsVectorLayer instance :('
        self.assertTrue(isinstance(layer, QgsVectorLayer), message)
        message = 'Hmm, something is wrong here, the number of features ' \
                  'should be 5'
        self.assertEqual(layer.featureCount(), 5, message)

        # Let's mess it up with wrong path
        vector_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '../../safe/test/data/boundaries/this_file_is_a_fool.shp'))
        layer = load_layer(vector_path, 'District OSM Jakarta')
        message = 'Dude! You are doing something wrong here'
        self.assertFalse(layer, message)



