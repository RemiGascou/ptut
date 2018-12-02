#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
PtutApp -> PtutApp

Author: Remi GASCOU
Last edited: December 2018
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from lib.ui import *
from lib.core import *

class PtutApp(QMainWindow):
	"""docstring for PtutApp."""
	def __init__(self, parent=None):
		super(PtutApp, self).__init__()
		self.title        = PtutAppInfos.get_name() + " - " + PtutAppInfos.get_version_tag()
		self.margin_left  = 200
		self.margin_top   = 200
		self.width        = 800
		self.height       = 600
		self._initUI()

	def _initUI(self):
		self.setWindowTitle(self.title)
		#self.setWindowIcon(QIcon('lib/meta/ico.png'))
		self.setGeometry(self.margin_left, self.margin_top, self.width, self.height)
		self.setFixedSize(self.size())
		self.setAttribute(Qt.WA_DeleteOnClose)
		self._initMenus()
		self.show()

	def _initMenus(self):
		mainMenu = self.menuBar()
		menuFile  = mainMenu.addMenu('File')
		menuClient  = mainMenu.addMenu('Client')
		entry0Button = QAction('Entry 0', self)
		entry0Button.triggered.connect(self.start_entry0Window)
		menuFile.addAction(entry0Button)
		entry1Button = QAction('Entry 1', self)
		entry1Button.triggered.connect(self.start_entry1Window)
		menuFile.addAction(entry1Button)
		menuFile.addSeparator()
		exitButton = QAction('Exit', self)
		exitButton.setShortcut('Ctrl+Q')
		exitButton.setStatusTip('Exit application')
		exitButton.triggered.connect(self.close)
		menuFile.addAction(exitButton)

		connectButton = QAction('Connect to analysis box', self)
		connectButton.triggered.connect(self.start_connectWindow)
		menuClient.addAction(connectButton)

# *------------------------------Windows Handlers----------------------------- *

	def start_entry0Window(self):
		self.wentry0Window = entry0Window()
		self.wentry0Window.show()

	def start_entry1Window(self):
		self.wentry1Window = entry1Window()
		self.wentry1Window.show()

	def start_connectWindow(self):
		self.wconnectWindow = connectWindow()
		self.wconnectWindow.show()



if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = PtutApp()
	sys.exit(app.exec_())
