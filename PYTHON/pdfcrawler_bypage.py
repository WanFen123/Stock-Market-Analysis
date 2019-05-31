# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 20:49:37 2019

@author: user
"""

import PyPDF2
import re
import os

#set directory to where you store all PDF files
files = os.listdir('PDF/PDF6')

#specify the string to be find in PDF files
String = ["STATEMENT OF COMPREHENSIVE INCOME", "STATEMENTS OF COMPREHENSIVE INCOME",
          "STATEMENT OF FINANCIAL POSITION", "STATEMENTS OF FINANCIAL POSITION",
          "STATEMENT OF CHANGES IN EQUITY", "STATEMENTS OF CHANGES IN EQUITY",
          "STATEMENT OF CASH FLOWS", "STATEMENTS OF CASH FLOWS",
          "STATEMENT OF PROFIT OR LOSS", "STATEMENTS OF PROFIT OR LOSS"]

for file in files:
    try:
        file.encode('UTF-8')
        filename = file.split(".")[0]
        object = PyPDF2.PdfFileReader(file)
        #to get the total number of pages for PDF
        NumPages = object.getNumPages()
        pdf_writer = PyPDF2.PdfFileWriter()
    
        pageList = []
        for i in String:
            for j in range(1, NumPages):
                #to get access to the page
                PageObj = object.getPage(j)
                #to extract text by page from PDF
                Text = PageObj.extractText()
                #to search string whether is inside the text, if yes save the pagenumber
                if re.search(i, Text) is not None:
                    pageList.append(j)
    
        for page in pageList:
            pdf_writer.addPage(object.getPage(page))
            output_filename = '{}_Statements.pdf'.format(filename)
            #to output a new pdf with only selected pages that contain string
            with open(output_filename, 'wb') as f:
                 pdf_writer.write(f)      
    except KeyError:
        pass
