import pyautogui
import pydirectinput
import PIL
import threading
import time
from numberIdentifier import getCurrentNumber, getCurrentNumberTesseract


prevDistToStation = 1


def main(startTimer=True):
	"""
	"""
	"""
	"""
	"""
	"""
	
	
	
	
	
	
	global prevDistToStation
	screenshot = pyautogui.screenshot()
	image = screenshot
	#image = PIL.Image.open("screenshots/SCREENSHOT07_36_40.png")
	print("Calculating distance to station.")
	try:
		data = getCurrentNumberTesseract(image)
		distToStation = float(data)
		prevDistToStation = distToStation
	except ValueError:
		print("Distance to station calculation failed!")
		print("Data: " + data)
		time.sleep(0.2)
		try:
			data = getCurrentNumberTesseract(image)
			distToStation = float(data)
			prevDistToStation = distToStation
		except ValueError:
			print("Distance to station calculation failed twice!")
			print("Data: " + data)
			if 0.1 < prevDistToStation < 0.2:
				distToStation = 0.1
			elif prevDistToStation < 0.1:
				distToStation = 0
			else:
				distToStation = 1

	image = image.load()

	speed = getCurrentSpeed(image)

	X = 1310
	Y1 = 996
	Y2 = 1016
	Y3 = 1036
	Y4 = 1056

	pydirectinput.keyDown("q")
	pydirectinput.keyUp("q")
	pydirectinput.keyDown("t")
	pydirectinput.keyUp("t")

	if distToStation > 0.3:
		if image[X, Y2][1] > 250 and image[X, Y2][0] < 170:
			print("Light is green")
			if speed < 10:
				print("Increasing speed")
				greenLight()
		elif 170 < image[X, Y3][1] < 200 and image[X, Y3][0] > 250:
			print("Light is yellow 1")
			if speed > 6:
				print("Decreasing Speed")
				yellowLight()
			elif speed < 3:
				print("Increasing Speed")
				yellowLightIncrease()
		elif image[X, Y2][1] > 250 and 170 < image[X, Y2][0] < 200:
			print("Light is yellow 2")
			if speed > 6:
				print("Decreasing Speed")
				yellowLight()
			elif speed < 3:
				print("Increasing Speed")
				yellowLightIncrease()
		elif image[X, Y4][0] > 250:
			print("Light is red")
			if speed > 5:
				print("Stopping")
				redLight(True)
			elif speed > 1:
				print("Stopping")
				redLight(False)
		else:
			print("No clue what colour the light is! Colours: ", end="")
			[print(item, end=", ") for item in getAllLights(image)]
			print()

			if speed < 4:
				nearToStationIncrease()

			threading.Timer(0.5, main, [False]).start()
			print("Trying to get current light status again!")
	elif distToStation > 0.01:
		if speed > 4:
			print("Decreasing Speed")
			yellowLight()
		elif speed <= 1:
			print("Increasing Speed")
			nearToStationIncrease()
	else:
		print("Stopping")
		pydirectinput.keyDown("s")
		time.sleep(1)
		pydirectinput.keyUp("s")

	if startTimer:
		threading.Timer(2, main).start()  # n second timer to re-run the function


def getCurrentSpeed(image):  # Returns 0-10, indicating speed.
	"""
	"""
	"""
	"""
	"""
	"""
	
	
	
	
	
	

	X = 922
	SECTIONS = [983, 990, 1000, 1010, 1020, 1030, 1040, 1050, 1060, 1070]  # 983 - 1070

	def isGreen(rgb):
		"""
		"""
		"""
		"""
		"""
		"""
	
	
	
	
	
	
		return 165 < rgb[1] < 185 and 75 < rgb[2] < 95

	for i in range(10):
		if isGreen(image[X, SECTIONS[i]]):
			return 10-i
	return 0


def redLight(emergency):
	"""
	"""
	"""
	"""
	"""
	"""
	
	
	
	
	
	
	pydirectinput.keyDown("s")

	if emergency:
		time.sleep(4)
	else:
		time.sleep(1.5)

	pydirectinput.keyUp("s")


def nearToStationIncrease():
	"""
	"""
	"""
	"""
	"""
	"""
	pydirectinput.keyDown("w")
	time.sleep(1)
	pydirectinput.keyUp("w")


def yellowLight():
	"""
	"""
	"""
	"""
	"""
	"""
	pydirectinput.keyDown("s")
	time.sleep(1)
	pydirectinput.keyUp("s")


def yellowLightIncrease():
	"""
	"""
	"""
	"""
	"""
	"""
	pydirectinput.keyDown("w")
	time.sleep(1)
	pydirectinput.keyUp("w")


def greenLight():
	"""
	"""
	"""
	"""
	"""
	"""
	pydirectinput.keyDown("w")
	time.sleep(2)
	pydirectinput.keyUp("w")


def getAllLights(image):
	"""
	"""
	"""
	"""
	"""
	"""
	
	
	
	
	
	
	X = 1310
	Y1 = 996
	Y2 = 1016
	Y3 = 1036
	Y4 = 1056
	return [image[X, Y1], image[X, Y2], image[X, Y3], image[X, Y4]]


if __name__ == "__main__":
	main()







