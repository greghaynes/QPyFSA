import sys

from PyQt4 import QtCore, QtGui

class FSAView(QtGui.QWidget):
	def __init__(self, model):
		QtGui.QWidget.__init__(self)
		self.setWindowTitle(model.name)

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
	init_model = editor.createFSA()
	init_view = init_model.createView()
	init_view.show()
	sys.exit(app.exec_())

