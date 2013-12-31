#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    Convert XML description to source.
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

'''
1. Expect a single definition of testType and TestSUT.
2. TestMod can be multiple.
Each new occurence of testMod start a new file.
This testMod will be the name of the file generated.
3. The tags used in a testMod will be deleted after each occurence.
This is to catch any stray tag that floats without a valid xml structure.
For example a testCase tag cannot exits outside either a codeMod or the
currMod.
4. Currently the same format of testcases for both FUNtional testing and
STesting.
5. Formatting and generation of c code files will be handled by another module.

'''

import xml.sax
import os
import sys
import operator
import subprocess
from functools import reduce

debug=5

def log(lvl, arg, *args):
	if lvl >= debug:
		print(arg, (lambda: args and args or "")())
	return lvl

dir='./'

def fileCommit(fname, buffer):
        global dir

        opfile=dir+fname[fname.rfind('/')+1:]
        fobj=open(opfile, mode='w')
        fobj.write(buffer)
        fobj.flush()
        fobj.close
        subprocess.call(["indent", "%s" %opfile])
        os.remove("%s~" %opfile)

class commiter:
        def reinitElements(self):
                _f=lambda x:operator.setitem(self.elements, x, '\n')
                list(list(map(_f, ['include', 'define', 'gvariable', 'codeMod', 'currMod'])))
        def clearElements(self):
                _f=lambda x: operator.delitem(self.elements, x)
                list(list(map(_f, ['include', 'define', 'gvariable', 'codeMod', 'currMod'])))
        def __init__(self):
                log(1, "Initialized commiter class")
                self.elements={}
                self.tcElements={}
        def __del__(self):
                pass
        def testType_Start(self, name, attrs):
                log(1, "Fun "+name+"_Start", attrs)
                self.elements[name]=attrs['type']
        def testSUT_Start(self, name, attrs):
                log(1, "Fun "+name+"_Start", attrs)
                self.elements[name]=attrs['lib']+"_"+attrs['version']
        def testMod_Start(self, name, attrs):
                log(1, "Fun "+name+"_Start", attrs)
                self.modName=attrs['mod']
                '''if already .h then skip .c addition'''
                self.elements[name]=self.modName+".c"
                self.reinitElements()
        def include_End(self, name, attrs):
                log(1, "Fun "+name+"_End", attrs)
                self.elements[name]+="\n#include "+attrs['value']
        def define_End(self, name, attrs):
                log(1, "Fun "+name+"_End", attrs)
                self.elements[name]+="\n#define "+attrs['value']
        def gvariable_End(self, name, attrs):
                log(1, "Fun "+name+"_End", attrs)
                self.elements[name]+="\n"+attrs['value']+";"
        def codeMod_Start(self, name, attrs):
                log(1, "Fun "+name+"_Start", attrs)
                '''re-init local variables and the testcases for
                the code module'''
                if 'func' in attrs:
                        self.elements['func']=attrs['func']
                else:
                        self.elements['func']=None
                operator.setitem(self.elements, 'lvariable', '\n')
                operator.setitem(self.elements, 'testCase', '\n')
        def currMod_Start(self, name, attrs):
                log(1, "Fun "+name+"_Start", attrs)
                '''re-init local variables and the testcases for
                the curr module'''
                operator.setitem(self.elements, 'lvariable', '\n')
                operator.setitem(self.elements, 'testCase', '\n')
        def lvariable_End(self, name, attrs):
                log(1, "Fun "+name+"_End", attrs)
                self.elements[name]+="\n  "+attrs['value']+";"
        def testCase_Start(self, name, attrs):
                log(1, "Fun "+name+"_Start", attrs)
                self.tcElements['typ']=attrs['typ']
        def cmd_End(self, name, attrs):
                log(1, "Fun "+name+"_End", attrs)
                self.tcElements[name]='value' in attrs and attrs['value'] or ""
        def desc_End(self, name, attrs):
                log(1, "Fun "+name+"_End", attrs)
                self.tcElements[name]='value' in attrs and attrs['value'] or ""
        def cond_End(self, name, attrs):
                log(1, "Fun "+name+"_End", attrs)
                self.tcElements[name]='value' in attrs and attrs['value'] or ""
        def err_End(self, name, attrs):
                log(1, "Fun "+name+"_End", attrs)
                self.tcElements[name]='value' in attrs and attrs['value'] or ""
        def errStr_End(self, name, attrs):
                log(1, "Fun "+name+"_End", attrs)
                self.tcElements[name]='value' in attrs and attrs['value'] or ""
        def flags_End(self, name, attrs):
                log(1, "Fun "+name+"_End", attrs)
                self.tcElements[name]='value' in attrs and attrs['value'] or ""
        def testCase_End(self, name, attrs):
                log(1, "Fun "+name+"_End", attrs)
                log(2, self.tcElements)
                fun=getattr(self, "%s_Fmt" %self.tcElements['typ'], lambda x:False)
                self.elements[name]+=fun(self.tcElements)+"\n"
        def FUN_Fmt(self, h):
                log(1, "Inside Fun_Fmt")
                cmd="\n  "+h['cmd']+";\n  EXEC_TSTCASE(&tstCase,"+h['desc']+","
                cmd+=h['cond']+","+h['err']+","+h['errStr']+","+h['flags']+");"
                return cmd
        def ST_Fmt(self, h):
                log(1, "Inside ST_Fmt")
                cmd="\n  "+h['cmd']+";\n  EXEC_TSTCASE(&tstCase,"+h['desc']+","
                cmd+=h['cond']+","+h['err']+","+h['errStr']+","+h['flags']+");"
                return cmd
        def IT_Fmt(self, h):
                log(1, "Inside IT_Fmt")
                cmd="\n  "+h['cmd']+";\n  EXEC_TSTCASE(&tstCase,"+h['desc']+","
                cmd+=h['cond']+","+h['err']+","+h['errStr']+","+h['flags']+");"
                return cmd
        def SH_Fmt(self, h):
                log(1, "Inside SH_Fmt")
                cmd="\n  EXEC_SH(&tstCase,\""+h['cmd']+"\","+h['desc']+","
                cmd+=h['flags']+");"
                return cmd
        def statement_End(self, name, attrs):
                log(1, "Fun "+name+"_End", attrs)
                self.elements['testCase']+="\n  "+attrs['value']+"\n"
        def codeMod_End(self, name, attrs):
                log(1, "Fun "+name+"_End", attrs)
                if self.elements['func']:
                        cm=self.elements['func']+"\n{\n"+self.elements['lvariable']+self.elements['testCase']+"\n}\n"
                else:
                        cm=self.elements['lvariable']+self.elements['testCase']
                self.elements[name]+=cm
                operator.delitem(self.elements, 'lvariable')
                operator.delitem(self.elements, 'func')
                operator.delitem(self.elements, 'testCase')
        def currMod_End(self, name, attrs):
                log(1, "Fun "+name+"_End", attrs)
                cm="\nvoid test_%s(void)\n{" %self.modName
                cm+=self.elements['lvariable']
                cm+="\n\n  hdr(\"Testing of %s module started\");" %self.modName
                cm+=self.elements['testCase']
                cm+="\n  hdr(\"Testing of %s module compleated\");" %self.modName
                cm+="\n}\n"
                self.elements[name]+=cm
                operator.delitem(self.elements, 'lvariable')
                operator.delitem(self.elements, 'testCase')
        def testMod_End(self, name, attrs):
                global dir

                log(1, "Fun "+name+"_End", attrs)
                _f=lambda a,b: a+'/'+self.elements[b]
                path=dir.rstrip('/')
                path+=reduce(_f, ['','testType', 'testSUT', 'testMod'])
                path=path.replace(' ','')
                path=path.replace('.h.c', '.h')
                log(2, path)
                self.purgeCommit(path)
                log(2, self.elements)
                self.clearElements()
        def purgeCommit(self, path=" "):
                log(1, "Inside purgeCommit")
                buffer="\n/*Autogenerated file %s*/" %path
                buffer+=self.elements['include']
                buffer+=self.elements['define']
                buffer+=self.elements['gvariable']
                buffer+=self.elements['codeMod']
                buffer+=self.elements['currMod']
                fileCommit(path, buffer)

class TestHandler(xml.sax.ContentHandler):
	def startDocument(self):
		log(1, "Start of parsing")
		self.commiter=commiter()
	def endDocument(self):
		log(1, "End of parsing")
	def wait4Val(self, name, attr):
		self.attrBuf=attr
		self.valBuf=""
		self.waitFlag=True
	def startElement(self, name, attrs):
		log(2, "Start of element %s" %name)
		attrdict=dict([(n, attrs.getValue(n)) for n in attrs.getNames()])
		log(3, "Attributes: ", attrdict)
		self.waitFlag=False
		fun=getattr(self.commiter, "%s_Start" %name, self.wait4Val)
		fun(name, attrdict)
	def endElement(self, name):
		log(2, "End of element %s" %name)
		fun=getattr(self.commiter, "%s_End" %name, lambda x,y:False)
		if self.waitFlag and self.valBuf:
			self.attrBuf['value']=self.valBuf
		fun(name, self.attrBuf)
		self.waitFlag=False
		self.valBuf=''
	def characters(self, content):
		string = content.strip()
		if string:
			if self.waitFlag:
				self.valBuf+=string
			else:
				log(4, "Other contents: %s" %string)

def startDecode(stream):
	log(1, "Inside startDecode function")
	saxobj = TestHandler()
	saxparser = xml.sax.make_parser()
	saxparser.setContentHandler(saxobj)
	saxparser.parse(stream)

def main():
        global dir

        log(1, "Inside main")
        if len(sys.argv)<=1:
                print("Specify xml file name. Exiting ..")
                sys.exit(1)
        if len(sys.argv) >= 3:
                dir=sys.argv[2]
        else:
                print("Assuming current directory")
        fileObj=open(sys.argv[1])
        startDecode(fileObj)
        fileObj.close()

if __name__=='__main__':
	log(1, "Before calling main")
	main()
