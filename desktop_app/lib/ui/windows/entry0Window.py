#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
PtutApp -> entry0Window

Author: Remi GASCOU
Last edited: December 2018
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from lib.ui import *
from lib.core import *

class entry0Window(QWidget):
	def __init__(self, parent=None):
		super(entry0Window, self).__init__()
		self.title = 'entry0Window'
		self.marginleft = 0
		self.margintop  = 0
		self.width      = 300
		self.height     = 200
		self._initUI()
		self.show()

	def _initUI(self):
		self.setWindowTitle(self.title)
		self.setAttribute(Qt.WA_DeleteOnClose)  #Kill application on close
		self.setGeometry(self.marginleft, self.margintop, self.width, self.height)
		self.label = QLabel("<b>" + PtutAppInfos.get_name() + " " + PtutAppInfos.get_version() + " </b><br><br>" + PtutAppInfos.get_credits(), self)
		self.label.setAlignment(Qt.AlignCenter)
		self.layout = QGridLayout()
		self.layout.addWidget(self.label, 0, 0)
		self.setLayout(self.layout)



if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = entry0Window()
	sys.exit(app.exec_())
