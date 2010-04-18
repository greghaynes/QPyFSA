import sys
import gettext
from fsas import FSA

from PyQt4 import QtCore, QtGui

_ = gettext.gettext

class StateView(QtGui.QGraphicsEllipseItem):
	def __init__(self, name):
		QtGui.QGraphicsEllipseItem.__init__(self, 20, 20, 50, 50)
		self.setFlags(QtGui.QGraphicsItem.ItemIsMovable)
		self.setBrush(QtGui.QBrush(QtGui.QColor(0x00, 0xff, 0xff)))

class FSAView(QtGui.QMainWindow):
	def __init__(self, model):
		QtGui.QMainWindow.__init__(self)
		self.model = model
		self.scene = QtGui.QGraphicsScene(self)
		self.sceneView = QtGui.QGraphicsView(self.scene)
		self.sceneView.setInteractive(True)
		self.setWindowTitle(model.name)
		
		# static actions
		new_actioin = QtGui.QAction(_('New'), self)
		close_action = QtGui.QAction(_('Close'), self)
		self.connect(new_actioin, QtCore.SIGNAL('triggered()'), self.newModel)
		self.connect(close_action, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

		# non-static actions
		self.add_state_action = QtGui.QAction(_('Add State'), self)
		self.connect(self.add_state_action, QtCore.SIGNAL('triggered()'), self.addState)

		# menus
		file_menu = self.menuBar().addMenu(_('&File'))
		file_menu.addAction(new_actioin)
		file_menu.addAction(close_action)
		edit_menu = self.menuBar().addMenu(_('&Edit'))
		edit_menu.addAction(self.add_state_action)

		try:
			self.states = model.fsa.states
		except AttributeError:
			self.stateviews = []
		
		self.setCentralWidget(self.sceneView)
	def newModel(self):
		model = self.model.editor.createFSA()
		view = model.createView()
		view.show()
	def addState(self):
		name, ok = QtGui.QInputDialog.getText(self, 'Add State', 'State name:')
		if ok:
			view = StateView(name)
			self.stateviews.append(view)
			self.scene.addItem(view)

class FSAModel(QtCore.QObject):
	def __init__(self, editor, name=_('Untitled')):
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

