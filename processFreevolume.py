import os
from time import sleep
import sys
import subprocess
import decimal

def extract_numbers (line):
	lineString = line.replace ("\t", ",").replace (" ", ",").replace ("\n", "")
	for item in lineString.split (","):
		try:
			yield decimal.Decimal (item)
		except:
			pass

def processFiles (fileName):
	delInterval = 0
	nOccupied = {}
	nUnoccupied = {}
	nTimeframes = 0
	density = 0.93

	with open (fileName, "r") as inputFile:
		for line in inputFile:
			logData = list (extract_numbers (line))
			# print (logData)
			if (delInterval == 0):
				delInterval = logData[1] - logData[0]
				# print ("delInterval: ", delInterval)
			try:
				nOccupied[float (logData[0])] += int (logData[2])
				nUnoccupied[float (logData[0])] += int (logData[3])
				nTimeframes += 1
			except:
				nOccupied[float (logData[0])] = int (logData[2])
				nUnoccupied[float (logData[0])] = int (logData[3])
				nTimeframes += 1

	outputFilename = fileName.replace (".log", ".processed")

	with open (outputFilename, "w") as outputFile:
		for key in nOccupied:
			outputString = ("{} {} {} {} {}\n".format (float (key), (float (key) + float (delInterval)), nOccupied[key], nUnoccupied[key], nUnoccupied[key] / (nUnoccupied[key] + nOccupied[key])))
			outputFile.write (outputString)		

def checkAllFiles ():
	fileContains = str (sys.argv[1])
	filePaths = {}

	for dirs, dirname, files in os.walk("."):
		for file in files:
			if ((fileContains in file) and ('logs' in dirs)):
				filePath = dirs + "/" + file
				processFiles (filePath)

def main ():
	cwd = os.getcwd()
	checkAllFiles ()

if __name__ == '__main__':
	main()