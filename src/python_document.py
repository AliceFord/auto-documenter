import re
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class CustomInputBox(QHBoxLayout):
	def __init__(self, labelText, placeholderText, type="text", dropdownOptions=[]):
		super(CustomInputBox, self).__init__()
		self.labelText = labelText
		label = QLabel()
		label.setText(labelText)
		self.addWidget(label)

		if type == "text":
			self.lineEdit = QLineEdit()
			self.lineEdit.setPlaceholderText(placeholderText)
			self.addWidget(self.lineEdit)
		elif type == "dropdown":
			dropdown = QComboBox()
			dropdown.addItems(dropdownOptions)
			dropdown.setPlaceholderText(placeholderText)
			self.addWidget(dropdown)

	def getData(self):
		return [self.labelText, self.lineEdit.text()]


class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		self.filename, success = QFileDialog.getOpenFileName(self, "Please choose the file you wish to document.")

		f = open(self.filename)
		fileText = f.read()

		self.docks = []
		self.currentDock = 0

		mainWidget = QWidget()
		mainLayout = QHBoxLayout()
		mainLayout.setAlignment(Qt.AlignTop)

		self.view = QTableWidget()
		functions = self.getFunctions(fileText)

		self.view.setRowCount(len(functions))
		self.view.setColumnCount(1)
		self.view.setHorizontalHeaderLabels(["Function Name"])
		self.view.setVerticalHeaderLabels([str(function[0]) for function in functions])
		writeDoc = QPushButton("Write Documentation")
		writeDoc.clicked.connect(self.writeDocumentation)

		for index, function in enumerate(functions):
			dock = QDockWidget(function[1])

			dockWidget = QWidget()

			dockLayout = QVBoxLayout()

			mainDescription = CustomInputBox("Main Description:", "Main Description")
			dockLayout.addLayout(mainDescription)

			for param in self.getParameters(function[2]):
				if param[0] == ' ':
					param = param[1:]
				paramUse = CustomInputBox(f"Parameter \'{param}\' Use:", "Use")
				dockLayout.addLayout(paramUse)

				paramType = CustomInputBox(f"Parameter \'{param}\' Type:", "Type")
				dockLayout.addLayout(paramType)

			returns = CustomInputBox("Function Returns:", "Returns")
			dockLayout.addLayout(returns)

			rtype = CustomInputBox("Function Return Type:", "Return Type")
			dockLayout.addLayout(rtype)

			dockWidget.setLayout(dockLayout)
			dock.setWidget(dockWidget)

			dock.setVisible(False)
			self.docks.append(dock)
			self.addDockWidget(Qt.RightDockWidgetArea, dock)
			button = QPushButton(function[1])
			button.clicked.connect(lambda checked, index=index: self.changeActiveFunction(index))
			self.view.setCellWidget(index, 0, button)

		f.close()

		mainLayout.addWidget(self.view)
		mainLayout.addWidget(writeDoc)

		mainWidget.setLayout(mainLayout)

		self.setCentralWidget(mainWidget)
		self.setWindowTitle("Auto Documenter")
		self.setGeometry(50, 50, 200, 200)
		self.show()

	def writeDocumentation(self):
		with open(self.filename) as text:
			text = text.read()
			functions = self.getFunctions(text)
			functions.append([[-1]])
			funcCounter = 0
			finalText = ""
			for index, line in enumerate(text.split("\n")):
				finalText += line + "\n"
				if index+1 == functions[funcCounter][0]:
					listOfItems = self.docks[funcCounter].widget().layout()
					finalText += "\t\"\"\"\n"
					finalText += ("\t" + listOfItems.itemAt(0).getData()[1] + "\n") if listOfItems.itemAt(0).getData()[1] != "" else ""
					i = 1
					while(i < len(listOfItems)-2):
						finalText += ("\t:param " + self.getFunctionName(listOfItems.itemAt(i).getData()[0]) + ": " + listOfItems.itemAt(i).getData()[1] + "\n") if listOfItems.itemAt(i).getData()[1] != "" else ""
						i+=1
						finalText += ("\t:type " + self.getFunctionName(listOfItems.itemAt(i).getData()[0]) + ": " + listOfItems.itemAt(i).getData()[1] + "\n") if listOfItems.itemAt(i).getData()[1] != "" else ""
						i+=1
					finalText += ("\t:return:" + listOfItems.itemAt(len(listOfItems)-2).getData()[1] + "\n") if listOfItems.itemAt(len(listOfItems)-2).getData()[1] != "" else ""
					finalText += ("\t:rtype:" + listOfItems.itemAt(len(listOfItems)-1).getData()[1] + "\n") if listOfItems.itemAt(len(listOfItems)-1).getData()[1] != "" else ""
					finalText += "\t\"\"\"\n"
					funcCounter += 1

		with open(self.filename, "w") as f:
			f.write(finalText)

	def changeActiveFunction(self, functionIndex):
		self.docks[self.currentDock].setVisible(False)
		self.docks[functionIndex].setVisible(True)
		self.currentDock = functionIndex

	@staticmethod
	def getFunctionName(text):
		return re.findall("'(.*?)'", text)[0]

	@staticmethod
	def getParameters(text):
		allParams = re.findall("[(](.*?)[)]", text)
		if allParams == [] or allParams == [""]:
			return []
		return allParams[0].split(',')

	@staticmethod
	def getFunctions(text):
		functions = []
		for i in range(len(text.split("\n"))):
			line = text.split("\n")[i]
			if re.findall("def (.*?)[(]", line):
				functions.append([i + 1, re.findall("def (.*?)[(]", line)[0], line])

		return functions


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	app.exec_()
