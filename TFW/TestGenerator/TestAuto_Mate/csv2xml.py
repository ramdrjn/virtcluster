#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Convert csv description to xml description.
    Copyright (C) 2013 Ramesh Devarajan

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''

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
