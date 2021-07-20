#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 15:13:19 2021

@author: dankovacevich
"""
#may need to install PyPDF2 to work
import re, sys, os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, ARCHIVES
from Deliverable import *

app = Flask(__name__)

zipf = UploadSet('zipf', ARCHIVES)
UPLOAD_FOLD = '/Users/dankovacevich/Desktop/DeliverableWebsite'
app.config['UPLOADED_ZIPF_DEST'] = UPLOAD_FOLD
configure_uploads(app, zipf)

filename = "2021-P2-blue-report.zip"

@app.route('/', methods=['GET', 'POST'])
def upload():
      if request.method == 'POST' and 'zipfile' in request.files:
          
        zipfile = request.files['zipfile']
        if zipfile:
            zipf.save(request.files['zipfile'])
            filename = secure_filename(zipfile.filename)
    
      return render_template('upload.html')
  
@app.route("/postresults",methods=["POST","GET"])
def postresults():
    
    if request.method == 'POST':
        skills = request.form.getlist('skill[]')
        zf = ZipFolder(filename)
        for names in skills:  
            zf.mustHave(names)
        zf.report() 
        del zf
        os.remove(filename)
    return render_template('Report.html')
 
    
if __name__ == '__main__':
	app.run(debug=True)
