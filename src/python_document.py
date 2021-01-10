import re
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


def getParameters(text):
	allParams = re.findall("[(](.*?)[)]", text)
	if allParams == []:
		return []
	return allParams[0].split(',')


def getFunctions(text):
	functions = []
	for i in range(len(text.split("\n"))):
		line = text.split("\n")[i]
		if re.findall("def (.*?)[(]", line):
			functions.append([i+1, re.findall("def (.*?)[(]", line)[0], line])

	return functions


def main(text):
	finalText = ""
	for i in range(len(text.split("\n"))):
		line = text.split("\n")[i]
		finalText += line + "\n"
		if "def" in line:
			if "\"\"\"" in text.split("\n")[i+1]:
				continue
			doc = input("Would you like to document the \"" + re.findall("def (.*?)[()]", line)[0] + "\" function?")
			if doc == 'y':
				mainDescription = input("Please enter the main description for the function: ")
				parameters = [[param, input("Enter the description for parameter " + param + ": "), input("Enter the type of parameter " + param + ": ")] for param in getParameters(line)]
				returns = input("Please enter what the program returns: ")
				rtype = input("Please enter the type the program returns: ")
				finalText += "\t\"\"\"\n" \
							"\t" + mainDescription + "\n" + \
							'\t\n'.join([f":param {param[0]}: {param[1]}\n:type {param[0]}: {param[2]}\n" for param in parameters]) + \
							"\t:return: " + returns + "\n" \
							"\t:rtype: " + rtype + "\n" \
							"\t\"\"\""

	return finalText


class CustomInputBox(QHBoxLayout):
	def __init__(self, labelText, placeholderText, type="text", dropdownOptions=[]):
		super(CustomInputBox, self).__init__()

		label = QLabel()
		label.setText(labelText)
		self.addWidget(label)

		if type == "text":
			lineEdit = QLineEdit()
			lineEdit.setPlaceholderText(placeholderText)
			self.addWidget(lineEdit)
		elif type == "dropdown":
			dropdown = QComboBox()
			dropdown.addItems(dropdownOptions)
			dropdown.setPlaceholderText(placeholderText)
			self.addWidget(dropdown)


class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		filename, success = QFileDialog.getOpenFileName(self, "Please choose the file you wish to document.")

		f = open(filename)

		self.docks = []
		self.currentDock = 0

		mainWidget = QWidget()
		mainLayout = QHBoxLayout()
		mainLayout.setAlignment(Qt.AlignTop)

		self.view = QTableWidget()
		functions = getFunctions(f.read())

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

			for param in getParameters(function[2]):
				if param[0] == ' ':
					param = param[1:]
				paramUse = CustomInputBox(f"Parameter \'{param}\' Use:", "Use")
				dockLayout.addLayout(paramUse)

				paramType = CustomInputBox(f"Parameter \'{param}\' Type:", "Type")
				dockLayout.addLayout(paramType)

			returns = CustomInputBox("Function Returns:", "Returns")
			dockLayout.addLayout(returns)

			rtype = CustomInputBox("Function Return Type:", "options")
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
		pass  # TODO

	def changeActiveFunction(self, functionIndex):
		self.docks[self.currentDock].setVisible(False)
		self.docks[functionIndex].setVisible(True)
		self.currentDock = functionIndex


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	app.exec_()
