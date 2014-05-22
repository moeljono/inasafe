__author__ = 'gumbia'

import os
import unittest

from qgis.core import QgsVectorLayer
from safe_qgis.hackathon_training.working_with_vector import (
    load_layer,
    iterate_data,
    add_string_attribute,
    delete_attribute,
    write_layer_to_shapefile)


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

    def test_iterate_data(self):
        """Test the iterate_data function works."""
        # Load the layer first
        vector_path = os.path.join(
            os.path.dirname(__file__),
            '../../safe/test/data/boundaries/district_osm_jakarta.shp')
        layer = load_layer(vector_path, 'District OSM Jakarta')
        iterate_data(layer)

    def test_add_string_attribute(self):
        """Test the add_string_attribute function works."""
        # Load the layer first
        vector_path = os.path.join(
            os.path.dirname(__file__),
            '../../safe/test/data/boundaries/district_osm_jakarta.shp')
        layer = load_layer(vector_path, 'District OSM Jakarta')

        # Add an attribute called 'tes_add'
        add_string_attribute(layer, 'tes_add')
        provider = layer.dataProvider()
        attribute_names = []
        fields = provider.fields()
        for field in fields:
            attribute_names.append(field.name())
        print 'The fields now after adding tes_add: %s' % attribute_names

        # Delete the attribute again OK, so we're back to the clean state
        delete_attribute(layer, 'tes_add')

        provider = layer.dataProvider()
        attribute_names = []
        fields = provider.fields()
        for field in fields:
            attribute_names.append(field.name())
        print 'The fields now after deleting tes_add: %s' % attribute_names

    def test_delete_attribute(self):
        """Test the delete_attribute function works."""
        # Load the layer first
        vector_path = os.path.join(
            os.path.dirname(__file__),
            '../../safe/test/data/boundaries/district_osm_jakarta.shp')
        layer = load_layer(vector_path, 'District OSM Jakarta')

        # Add an attribute called 'tes_delete'
        add_string_attribute(layer, 'delete')

        # Delete it again
        delete_attribute(layer, 'delete')

    def test_write_layer_to_shapefile(self):
        """Test the write_layer_to_shapefile works."""
        # Load layer
        vector_path = os.path.join(
            os.path.dirname(__file__),
            '../../safe/test/data/boundaries/district_osm_jakarta.shp')
        layer = load_layer(vector_path, 'District OSM Jakarta')

        # Add an attribute called 'hackathon' to layer
        add_string_attribute(layer, 'hackathon')

        # Save it to new shapefile
        new_layer_path = '/tmp/hackathon.shp'
        path = write_layer_to_shapefile(layer, new_layer_path)

        # There should be exist /tmp/hackthon.shp file
        self.assertTrue(os.path.exists(path))

        # Delete hackathon attribute again to make the layer back to clean
        # state
        delete_attribute(layer, 'hackathon')


