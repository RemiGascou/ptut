#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
App -> App

Author: Remi GASCOU
Last edited: December 2018
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#from lib.core import *

class App(QMainWindow):
	"""docstring for App."""
	def __init__(self, parent=None):
		super(App, self).__init__()
		self.title        = AppInfos.get_name() + " - " + AppInfos.get_version_tag()
		self.margin_left  = 200
		self.margin_top   = 200
		self.width        = 800
		self.height       = 600


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())
