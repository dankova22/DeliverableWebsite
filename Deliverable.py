#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 18:19:06 2021

@author: dankovacevich
"""

from zipfile import ZipFile
import re
import py_compile
import os
from Requirements import *
#from Main import out_put

class Folder:
  def __init__(self, foldername):
    self.foldername = foldername + "/"
    self.folderrequirements = [] 
    self.folderoptional = []
  def mustHave(self, file, *requirements):
    self.folderrequirements.append([file])
    for condition in requirements:
      self.folderrequirements[-1].append(condition)
  def mayHave(self, file, *requirements):
    self.folderoptional.append([file])
    for condition in requirements:
      self.folderoptional[-1].append(condition)
        
    
               
class ZipFolder:
  #-----constructor that creates array of file names-----
  def __init__(self,zipfilename):
    self.files = []
    self.junk = []
    self.requirements = []
    self.optional = []
    self.correct = []
    self.errors = []
    self.missing = []
    self.zipfilename = zipfilename
    self.errmsg = [] 
    self.crrmsg = []
    self.missng = []
    for name in ZipFile(zipfilename,'r').namelist():
      self.files.append(name)
    
  #-------------adds must-have file to checklist----------------
  def mustHave(self, name, *requirements):
    self.requirements.append([name])
    for condition in requirements:
      self.requirements[-1].append(condition)
          
  #-------------adds optional file to checklist------------------
  def mayHave(self, name, *requirements):
    self.optional.append([name])
    for condition in requirements:
      self.optional[-1].append(condition)

  #--------prints all the contents of zipfolder----------   
  def printfiles(self):
    for i in self.files:
      print(i)
    print('\n')
      
  #----------checks all requirements in a folder----------
  def checkfolderrequirements(self, folder, foldername, folderarray, types):
    for k in range(0,len(folderarray)):
      foundfile = 0
      #checks requirements against actual zip contents
      for l in range(0,len(self.files)):
        #if finds match
        if(re.match(foldername + folderarray[k][0], self.files[l])):
          foundfile = 1 
          if(self.files[l].endswith(".py")):
            stop = "now"
          #only requirement is name
          if(len(folderarray[k]) == 1):
            if(types == 'r'):
              self.correct.append(foldername)
            elif(types == 'o'):
              self.correct.append(fldrname)
          else:
            try:
              self.foundfolderfilematch(self.files[l], folderarray[k], foldername, types)
            except Exception as e:
              print(e)
                  
      if(foundfile == 0 and types == 'r'):
        self.missng.append(folder.folderrequirements[k][0])
      
  #--loops through folder requirements if found foldermatch--
  def foundfoldermatch(self, folder, types):
    foldername = folder.foldername
    self.errmsg = [foldername] 
    if(types == 'r'):    
      self.crrmsg = [foldername]
    elif(types == 'o'):
      fldrname = foldername.strip('/')
      fldrname += " (optional)/"
      self.crrmsg = [fldrname]
    self.missng = [foldername]
    foundanymissing = 0
    self.checkfolderrequirements(folder, foldername, folder.folderrequirements, 'r')
    self.checkfolderrequirements(folder, foldername, folder.folderoptional, 'o')
    if(len(self.crrmsg) > 1):
      self.correct.append(self.crrmsg)
    if(len(self.errmsg) > 1 and types == 'r'):
      self.errors.append(self.errmsg)
    if(len(self.missng) > 1 and types == 'r'):
      self.missing.append(self.missng) 
          
  #--loops through file requirements for file in a folder--      
  def foundfolderfilematch(self, file, filerequirements, foldername, types):
    currentfile = file
    founderror = 0
    #loops through all the requirements of a required file and confirms them
    for m in range(1, len(filerequirements)):
      result = checkcondition(self.zipfilename, currentfile, filerequirements[m])
      os.remove(currentfile)
      if(result != 'correct'):
        founderror = 1
        self.errmsg.append(currentfile.strip(foldername))
        self.errmsg.append(result)
    if(founderror == 0):
      if(types == 'r'): 
        self.crrmsg.append(currentfile.strip(foldername))
        foundanycorrect = 1
      elif(types == 'o'):
        self.crrmsg.append(currentfile.strip(foldername) + " (optional)")
        foundanycorrect = 1
        
  #-----loops through requirements for individual file-----        
  def foundfilematch(self, file, types):
    #only requirement is file name
    if(len(file) == 1):
      self.correct.append(file[0])
    else:
      errmsg = []
      #loops through all the requirements of a required file and confirms them
      for k in range(1,len(file)):
        result = checkcondition(self.zipfilename, file[0], file[k])
        os.remove(file[0])
        if(result != 'correct'):
          errmsg.append(result)
        if(len(errmsg) == 0):
          if(types == 'o'):
            self.correct.append(file[0] + " (optional)")
          else:
            self.correct.append(file[0])
        else:
          self.errors.append([file[0]] + errmsg)
  
  #--------------checks requirements--------------------
  def checkrequirements(self, array, types):
      for i in range(0, len(array)):     
      #loop through all files in zip to check for that requirement
         foundmatch = 0
         for j in range(0, len(self.files)):
            #check if its a folder
            if(isinstance(array[i][0], Folder)):
                #check if found match of filename to requirement
                if(array[i][0].foldername == self.files[j]):    
                   foundmatch = 1
                   self.foundfoldermatch(array[i][0], types) 
                   #remove from junk array  
                   for l in range(len(self.files)):
                       if(self.files[l].startswith(array[i][0].foldername)):
                           self.junk[l] = 1
            #not a folder 
            else:
                #if file is a match 
                if(re.match(array[i][0], self.files[j])):
                    self.junk[j] = 1
                    foundmatch = 1
                    self.foundfilematch(array[i], types)        
         #file didn't match
         if(foundmatch == 0 and types == 'r'):
            if(isinstance(array[i][0], Folder)):
                self.missing.append(array[i][0].foldername)
            else:
                self.missing.append(array[i][0])     
   
 
              
  def printhtml(self):
    #Open html report and write opening tags, define style
    wd = os.getcwd()
    os.chdir(wd + '/templates' )
    f = open('Report.html','w')
    message = """ 
    <!DOCTYPE html>
    <html>
    <title>Deliverable Testing Tool </title> 
    
    <div>
      <h1>Deliverable Testing Tool Report</h1>
    </div>

    <body>
    """
    f.write(message)

    message = """
    <style>
      head {color:#000000; font-family: Tahoma, sans-serif;}
      body {background-color: #white; color:#000000; font-family: Tahoma, sans-serif;}
      div {display: flex; flex-direction: column; justify-content: center; text-align: center;}
      p {line-height: .6;}
      .tab {display: inline-block; margin-left: 25px;}
    </style>
    """
    f.write(message)
    
  #------------print correct deliverables---------------
    f.write("<p>")  
    f.write(""" 
    """) 
    f.write(" <b>Correct Deliverables:</b> <br></br>")  
    f.write(""" 
    """)
    for i in self.correct:
      if(i[0].endswith('/') and len(i) > 1):
        f.write(i[0] + "<br></br>")
        f.write("""
        """)
        f.write("""
        """)
        for j in range(1,len(i)):
          f.write("<span class=tab></span>" + i[j] + "<br></br>")
          f.write(""" 
          """)
      #  f.write(""" 
      #  """)
      else:    
        f.write(i + "<br></br>" )
        f.write(""" 
        """)
    f.write("</p>")
    f.write(""" 
    """)
    
  #------------print incorrect deliverables---------------   
    f.write("<p>")
    f.write(""" 
    """) 
    f.write("<b>Errors:</b>" + "<br></br>") 
    f.write(""" 
    """)
    for i in self.errors:
      if(i[0].endswith('/') and len(i) > 1):
        f.write(i[0] + "<br></br>")
        f.write(""" 
        """)
        f.write(""" 
        """)
        for j in range(1, len(i),2):
          f.write("<span class=tab></span>" + i[j] + ": " + i[j+1] + "<br></br>")
          f.write(""" 
          """)
        f.write(""" 
        """)
      else:
        f.write(i[0] + ": " + i[1] + "<br></br>")
        f.write(""" 
        """)
    f.write("</p>")
    f.write(""" 
    """)
    
    #------------print missing deliverables---------------       
    f.write("<p>")
    f.write(""" 
    """)  
    f.write("<b>Missing Deliverables:</b> <br></br>")
    f.write(""" 
    """)  
    for i in self.missing:
      if(i[0].endswith('/') and len(i) > 1 ):
        f.write(i[0] + "<br></br>") 
        f.write(""" 
        """)
        f.write(""" 
        """) 
        for j in range(1,len(i)):
          f.write("<span class=tab></span>" + i[j] + "<br></br>")
          f.write(""" 
          """) 
        f.write(""" 
        """)
      else:        
        f.write(i + "<br></br>")
        f.write(""" 
        """)
    f.write("</p>")
    f.write(""" 
    """)

    #-------------------print junk--------------------
    f.write("<p>")
    f.write(""" 
    """) 
    f.write( "<b>Junk Files:</b> <br></br>")
    f.write(""" 
    """) 
    for i in range(len(self.junk)):
      if (self.junk[i] == 0):
        f.write(self.files[i] + "<br></br>")
        f.write(""" 
        """)
    f.write("</p>")
    f.write(""" 
    """)
   #-----------------print ending tags----------------
    message = """
    </body>
    </html>"""
    f.write(message)
   
    f.close()       
    os.chdir(wd)
    
  #-----------------Prints Report--------------------
  def report(self):  
    #initialize junk
    self.junk = [0]*len(self.files)
    #checks requirements with required flag
    self.checkrequirements(self.requirements, 'r')
    #checks requirements with optional flag
    self.checkrequirements(self.optional, 'o')
    
    #-------------------PRINT RESULT----------------------
    self.printhtml()          
                
                
                
                
                
                
                
                
      
         