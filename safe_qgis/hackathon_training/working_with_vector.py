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

from PyQt4.QtCore import QVariant

from safe.common.testing import get_qgis_app
from qgis.core import (
    QgsVectorLayer,
    QgsVectorDataProvider,
    QgsField,
    QgsVectorFileWriter)


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
        shapefile restricts the length of the attribute name to be less than
        or equal to 10.
    :type attribute_name: str
    """
    layer.startEditing()
    provider = layer.dataProvider()
    capabilities = provider.capabilities()

    if capabilities & QgsVectorDataProvider.AddAttributes:
        result = provider.addAttributes(
            [QgsField(attribute_name, QVariant.String)])
        if not result:
            raise Exception(
                'Oh no, there is something wrong when adding this new '
                'attribute:' % attribute_name)
    layer.commitChanges()


def delete_attribute(layer, attribute_name):
    """Delete an attribute with given index.

    :param layer: The target we are working on.
    :type layer: QgsVectorLayer

    :param attribute_name: The attribute name that are going to be deleted.
    :type attribute_name: str
    """
    layer.startEditing()
    provider = layer.dataProvider()
    capabilities = provider.capabilities()

    attribute_index = provider.fieldNameIndex(attribute_name)
    if attribute_index == -1:
        raise Exception(
            'Dude, you are lying to me by giving wrong attribute name!')

    if capabilities & QgsVectorDataProvider.DeleteAttributes:
        layer.dataProvider().deleteAttributes([attribute_index])
    layer.commitChanges()


def iterate_data(layer):
    """Iterate all features in the layer.

    :param layer: The layer that we're working on.
    :type layer: QgsVectorLayer
    """
    features = layer.getFeatures()
    for feature in features:
        # fetch attributes
        attributes = feature.attributes()

        # attributes is a list.
        # It contains all the attribute values of this feature
        print attributes


def modify_attribute_value(layer, attribute_name):
    """Modify the attribute value. We'll just change the value of the
        attribute all to 'modif'

    :param layer: The layer we're working on.
    :type layer: QgsVectorLayer

    :param attribute_name: The attribute name that will be modified.
    :type attribute_name: str
    """
    layer.startEditing()
    provider = layer.dataProvider()
    capabilities = provider.capabilities()

    attribute_index = provider.fieldNameIndex(attribute_name)
    if attribute_index == -1:
        raise Exception(
            'Dude, you are lying to me by giving wrong attribute name!')

    if capabilities & QgsVectorDataProvider.ChangeAttributeValues:
        features = layer.getFeatures()
        for feature in features:
            feature_id = feature.id()
            attributes = {attribute_index: 'modif'}
            layer.dataProvider().changeAttributeValues({feature_id: attributes})
    layer.commitChanges()


def write_layer_to_shapefile(layer, path):
    """Write layer to a shapefile with given path.

    :param layer: The layer that will be saved.
    :type layer: QgsVectorLayer

    :param path: The file path.
    :type path: str

    :return: Path to the result file if it's successful. Or else return False
    :rtype: str, bool
    """
    error = QgsVectorFileWriter.writeAsVectorFormat(
        layer, path, "CP1250", None, "ESRI Shapefile")

    if error == QgsVectorFileWriter.NoError:
        return path

    return False


