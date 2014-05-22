# coding=utf-8
"""
InaSAFE Disaster risk assessment tool developed by AusAid

Contact : ole.moller.nielsen@gmail.com

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
__author__ = 'gumbia'


from safe.common.testing import get_qgis_app
from qgis.core import QgsVectorLayer, QgsVectorDataProvider, QgsField


QGIS_APP, CANVAS, IFACE, PARENT = get_qgis_app()


def load_layer(data_source, layer_name):
    """Load a vector layer with ogr provider.

    :param data_source: The path to the data source.
    :type data_source: str

    :param layer_name: The name of the soon-to-be our loaded layer.
    :type layer_name: str

    :return: A layer of QgsVectorLayer if it is successfully loaded.
        Or False if it fails.
    :rtype: QgsVectorLayer, bool
    """
    layer = QgsVectorLayer(data_source, layer_name, 'ogr')
    if layer.isValid():
        return layer
    return False


def add_string_attribute(layer, attribute_name):
    """Add a string attribute in vector layer with specific name.

    :param layer: The layer that we will work on.
    :type layer: QgsVectorLayer

    :param attribute_name: The name of the attribute. Remember that ESRI
        shapefile restricts the length of the attribute name to be less than 12.
    :type attribute_name: str

    :return: The result layer with new attribute on it.
    :rtype: QgsVectorLayer
    """
    provider = layer.dataProvider()
    capabilities = provider.capabilities()

    if capabilities & QgsVectorDataProvider.AddAttributes:
        pass
