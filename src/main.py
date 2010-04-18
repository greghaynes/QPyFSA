import sys

from PyQt4 import QtCore, QtGui

class FSAViewInternal(QtGui.QWidget):
	def __init__(self, view):
		QtGui.QWidget.__init__(self, view)
		self.view = view
		self.scene = QtGui.QGraphicsScene(self)
		
		vlayout = QtGui.QVBoxLayout(self)
		vlayout.addWidget(QtGui.QGraphicsView(self.scene))
		self.setLayout(vlayout)

class FSAView(QtGui.QMainWindow):
	def __init__(self, model):
		QtGui.QMainWindow.__init__(self)
		self.model = model
		self.setWindowTitle(model.name)
		
		new_actioin = QtGui.QAction('New', self)
		self.connect(new_actioin, QtCore.SIGNAL('triggered()'), self.newModel)
		close_action = QtGui.QAction('Close', self)
		self.connect(close_action, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
		file_menu = self.menuBar().addMenu('&File')
		file_menu.addAction(new_actioin)
		file_menu.addAction(close_action)

		self.setCentralWidget(FSAViewInternal(self))
	def newModel(self):
		model = self.model.editor.createFSA()
		view = model.createView()
		view.show()

class FSAModel(QtCore.QObject):
	def __init__(self, editor, name='Untitled'):
		QtCore.QObject.__init__(self, editor)
		self.name = name
		self.editor = editor
		self.views = []
	def createView(self):
		created = FSAView(self)
		self.views.append(created)
		return created

class FSAEditor(QtCore.QObject):
	def __init__(self):
		QtCore.QObject.__init__(self)
		self.models = []
	def createFSA(self):
		created = FSAModel(self)
		self.models.append(created)
		return created

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	editor = FSAEditor()
	view = editor.createFSA().createView()
	view.show()
	sys.exit(app.exec_())

