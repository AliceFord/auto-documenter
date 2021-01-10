import re


def getParameters(text):
	allParams = re.findall("[(](.*?)[)]", text)
	if allParams == ['']:
		return []
	return allParams[0].split(',')


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


if __name__ == '__main__':
	with open(r"../test/example.py") as f:
		print(main(f.read()))
