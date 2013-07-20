#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys

#Globals
debug=5
opStream=None

def log(lvl, arg, *args):
	if lvl >= debug:
		print arg, (lambda: args and args or "")()
	return lvl

def procFlds(f):

	global opStream

	wk=lambda x,y: y and x %y or ""
	buffer=''
	buffer+=wk("\n<testCase typ=\"ST\">\n<cmd>%s</cmd>\n</testCase>", f[0])
	buffer+="\n<testCase typ=\"FUN\">"
	buffer+=wk("\n<cmd>%s</cmd>", f[1])
	buffer+=wk("\n<desc>\"%s\"</desc>", f[2])
	buffer+=wk("\n<cond>%s</cond>", f[3])
	buffer+=wk("\n<err>%s</err>", f[4])
	buffer+=wk("\n<errStr>%s</errStr>", f[5])
	buffer+=wk("\n<flags>%s</flags>", f[6])
	buffer+="\n</testCase>"
	buffer+=wk("\n<testCase typ=\"ST\"><cmd>%s</cmd></testCase>", f[7])
	buffer=buffer.replace('&', '&amp;')
	log(2, buffer)
	opStream.write(buffer)

def main():

	global opStream

	log(1, "Inside main")
	if len(sys.argv)<=1:
		print "Specify CSV file name. Exiting .."
		sys.exit(1)
	fileObj=open(sys.argv[1])
	opStream=open("xtest.xml", 'w')
	rdCSV=csv.reader(fileObj, delimiter='#')
	rdCSV.next()
	map(procFlds, rdCSV)
	fileObj.close()
	opStream.close()
	log(1, "Exiting main")

if __name__=='__main__':
	log(1, "Before calling main")
	main()
	log(1, "Exiting")
