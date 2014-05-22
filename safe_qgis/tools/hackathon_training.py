__author__ = 'akbar'

from PyQt4 import QtGui
from PyQt4.QtGui import QMessageBox
from safe_qgis.ui.hackathon_training import Ui_Dialog


class HackathonTrainingDialog(QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        """Constructor for the dialog.

        :param parent: Parent widget of this dialog
        :type parent: QWidget
        """

        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        # Set up listener
        self.test.clicked.connect(self.say_hello)

    def say_hello(self):
        """Action to a listener."""
        QMessageBox.information(
            self,
            self.tr("Window Title"),
            'Happy coding you all!')



