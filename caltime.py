# -*- coding: utf-8 -*- 
	
import datetime
import re
import time

validWords = ['DESCRIPTION', 'SUMMARY', 'LOCATION', 'DTSTART', 'DTEND']

def createEvent(array):

	event = {}

	for line in array:
		l = line.split(':')

		if l[0] in validWords:
			event[l[0]] = l[1]

	return event
			

def calc(event):
	print "%s \n" % event


def main():

	insideEvent = False

	try:
		f = open("Kåda.ics", 'r');
	except IOError:
		print "Missing file!"
		exit(1)

	now = datetime.datetime.now()

	array = []

	for line in f:
		if line.startswith("BEGIN:VEVENT"):
			insideEvent = True
			continue
		
		elif line.startswith("END:VEVENT"):
			insideEvent = False
			event = createEvent(array)
			print event
			array = []

		if insideEvent:
			array.append(line)

main()
