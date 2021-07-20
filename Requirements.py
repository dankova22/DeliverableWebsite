#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 19:45:15 2021

@author: dankovacevich
"""
from zipfile import ZipFile
import re
import py_compile
import os
import sys
import PyPDF2
import imghdr
import subprocess

#-----------list of condition names-----------
pythonFile = f".*(.py)$"
pdfFile = f"(.pdf)$"
pngFile = f"(.png)$"



def UnixFileType(filename):
    return subprocess.check_output(["file","--mime-type", "-b", filename]).decode().rstrip()
       
#----------Test For Readable Text File------------
def ReadableTextFile():
    def readabletext(filename):
        try: 
           filetype = UnixFileType(filename)
           if(filetype == "text/plain"):
               return 'correct'
           else:
               return "Not a valid .txt file" 
        except:
           return "Not a valid .txt file" 
    return readabletext 
ReadableTextFile = ReadableTextFile()


#----------Test For Readable PDF File------------
def ReadablePDFFile():
    def readablepdf(filename):
        try: 
           filetype = UnixFileType(filename)
           if(filetype  == "application/pdf"):
               return 'correct'
           else:
               return "Not a valid .pdf file" 
        except: 
           return "Not a valid .pdf file"
    return readablepdf
ReadablePDFFile = ReadablePDFFile()

#----------Test For Readable JPEG File------------
def ReadableJPEGFile():
    def readablejpg(filename):
        try: 
           filetype = UnixFileType(filename)
           if(filetype  == "image/jpeg"):
               return 'correct'
           else:
               return "Not a valid JPEG file" 
        except: 
           return "Not a valid JPEG file"
    return readablejpg
ReadableJPEGFile = ReadableJPEGFile()

#----------Test For Readable PNG File------------
def ReadablePNGFile():
    def readablepng(filename):
        try: 
           filetype = UnixFileType(filename)
           if(filetype  == "image/png"):
               return 'correct'
           else:
               return "Not a valid png file" 
        except: 
           return "Not a valid png file"
        return 'correct'
    return readablepng
ReadablePNGFile = ReadablePNGFile()

#----------Test For Readable MSWORD File------------
def ReadableMSWORDFile():
    def readableword(filename):
        try: 
           filetype = UnixFileType(filename)
           if(filetype  == "application/msword" or 
              filetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"):
               return 'correct'
           else:
               return "Not a valid MS word document" 
        except: 
           return "Not a valid MS word document"
    return readableword
ReadableMSWORDFile = ReadableMSWORDFile()

#----------Test For Readable EXCEL File------------
def ReadableEXCELFile():
    def readableexcel(filename):
        try: 
           filetype = UnixFileType(filename)
           if(filetype  == "application/vnd.ms-excel" or 
              filetype == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"):
               return 'correct'
           else:
               return "Not a valid MS Excel file" 
        except: 
           return "Not a valid MS Excel file"
    return readableexcel
ReadableEXCELFile = ReadableEXCELFile()

#----------Test For Readable PPT File------------
def ReadablePPTFile():
    def readableppt(filename):
        try: 
           filetype = UnixFileType(filename)
           if(filetype  == "application/vnd.ms-powerpoint" or 
              filetype == "application/vnd.openxmlformats-officedocument.presentationml.presentation"):
               return 'correct'
           else:
               return "Not a valid MS PPT file" 
        except: 
           return "Not a valid MS PPT file"
    return readableppt
ReadablePPTFile = ReadablePPTFile()

#----------Test For Readable HTML File------------
def ReadableHTMLFile():
    def readablehtml(filename):
        try: 
           filetype = UnixFileType(filename)
           if(filetype  == "text/html"):
               return 'correct'
           else:
               return "Not a valid html file" 
        except: 
           return "Not a valid html file"
    return readablehtml
ReadableHTMLFile = ReadableHTMLFile()

#----------Test For Readable CSS File------------
def ReadableCSSFile():
    def readablecss(filename):
        try: 
           filetype = UnixFileType(filename)
           if(filetype  == "text/css"):
               return 'correct'
           else:
               return "Not a valid css file" 
        except: 
           return "Not a valid css file"
    return readablecss
ReadableCSSFile = ReadableCSSFile()

#----------Test For Readable CSV File------------
def ReadableCSVFile():
    def readablecsv(filename):
        try: 
           filetype = UnixFileType(filename)
           if(filetype  == "text/csv"):
               return 'correct'
           else:
               return "Not a valid csv file" 
        except: 
           return "Not a valid csv file"
    return readablecsv
ReadableCSVFile = ReadableCSVFile()


#--------------Test for Max Pages-----------------
def PDFMaxPages(num):
    def pdfpages(filename):
        try: 
            reader = PyPDF2.PdfFileReader(filename)
            if(reader.getNumPages() > num):
                difference = reader.getNumPages() - num
                dif = str(difference)
                number = str(num)
                return 'Over Max (' + number + ') Pages By ' + dif
            else:
                return 'correct'
        except:
            return 'Failed to Open File'     
    return pdfpages


#---------------Test For Compilation------------------
def PythonThatCompiles():
    def pythontest(filename):
        try:
            py_compile.compile(filename, doraise=True)
        except:
            return 'Failed Compile Check'
        return 'correct'
    return pythontest
PythonThatCompiles = PythonThatCompiles()




#-------------Checks Specific Condition-----------   
def checkcondition(zipfile,filename,requirement):
     with ZipFile(zipfile, 'r') as my_zip:
         my_zip.extract(filename)
     return requirement(filename)
  

