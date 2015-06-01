# -*- coding: utf-8 -*- 
	
import datetime
import re
import time
import os, sys
import argparse

filter = False
parser = argparse.ArgumentParser(description='Parser for using the Calendar as a Time logger')

parser.add_argument('--filter', type=str, help='Only include events in filter', default='')
args = parser.parse_args()

if 'filter' in args:
	filter = args.filter

try:
	import config
except IOError:
	print "No configuration :("
	exit(1)

words = ['DTSTART', 'DTEND', 'SUMMARY', 'LOCATION']

def createComponent(array):
	component = {}
	a = array.split(':')

	for word in words:
		if a[0].startswith(word):
			a[0] = word
			return (a[0], a[1].strip())

	return (False, False)

def createEvent(array):

	event = {}

	for line in array:
		name, value = createComponent(line)
		if False != value:
			event[name] = value

	if filter:
		if filter != event['SUMMARY']:
			return {'minutes': 0}

	try:
		start = datetime.datetime.strptime(event['DTSTART'], '%Y%m%dT%H%M%S')
	except ValueError as e:
		print 'Assuming all day event, skipping ..'
		event['minutes'] = 0
		return event

	event['DTSTART'] = start

	end = datetime.datetime.strptime(event['DTEND'], '%Y%m%dT%H%M%S')
	event['DTEND'] = end

	delta = end - start
	event['minutes'] = delta.seconds / 60

	return event
			

def parseFile(f):
	insideEvent = False
	array = []

	for line in f:
		if line.startswith("BEGIN:VEVENT"):
			insideEvent = True
			continue
		
		elif line.startswith("END:VEVENT"):
			insideEvent = False
			return createEvent(array)

		if insideEvent:
			array.append(line)


def main():
	print "Mathing events with summary: \"%s\"" % ('Progr')

	totalTime = 0

	files = os.listdir(config.path + '/Events')
	for file in files:
		if os.path.isfile(config.path + '/Events' + '/' + file) == True:
			try:
				f = open(config.path + '/Events' + '/' + file, 'r')
				event = parseFile(f)
				totalTime += event['minutes']
			except IOError:
				print "Missing file! Continuing..."

	print "Total time for current calendar is %s hours and %s minutes" % (totalTime/60, totalTime%60)

main()
