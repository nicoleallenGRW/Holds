# -*- coding: utf-8 -*-
#!/usr/bin/python2.7
#
# Test being run to export shelf list to collection managers
# Email Excel Spreadhseet to manager and supervisor 
# Use XlsxWriter to create spreadsheet from SQL Query
# 
#

import psycopg2
import xlsxwriter
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from datetime import datetime



excelfile =  'HoldsOnBibsWithItemsMarkedMissing.xlsx'



#Set variables for email

emailhost = 'mail.greenwichlibrary.org'
emailport = '25'
emailsubject = 'Holds With Items Marked Missing'
emailmessage = '''Attached are all bib level holds with items attached that have been marked missing.'''
emailfrom = 'nallen@greenwichlibrary.org'
emailto = ['nallen@greenwichlibrary.org']


try:
    conn = psycopg2.connect("dbname= user= host= port= password= sslmode=require")
except psycopg2.Error as e:
    print ("Unable to connect to database: " + str(e))
    
cursor = conn.cursor()
cursor.execute(open("HoldsOnBibsWithItemsMarkedMissing.sql","r",).read())
rows = cursor.fetchall()
conn.close()


workbook = xlsxwriter.Workbook(excelfile, {'remove_timezone': True})
worksheet = workbook.add_worksheet()


worksheet.set_landscape()
worksheet.hide_gridlines(0)



eformat= workbook.add_format({'text_wrap': True, 'valign': 'top' , 'num_format': 'mm/dd/yy'})
eformatlabel= workbook.add_format({'text_wrap': False, 'valign': 'top', 'bold': True})


worksheet.set_column(0,0,10.56)
worksheet.set_column(1,1,61.33)
worksheet.set_column(2,2,14.56)
worksheet.set_column(3,3,22.78)
worksheet.set_column(4,4,23.89)
worksheet.set_column(5,5,24.44)
worksheet.set_column(6,6,9)
worksheet.set_column(7,7,16)
worksheet.set_column(8,8,16.89)
worksheet.set_column(9,9,26.67)
worksheet.set_column(10,10,10)

worksheet.set_header('Holds With Items Marked Missing')

worksheet.write(0,0,'Bib Number', eformatlabel)
worksheet.write(0,1,'Title', eformatlabel)
worksheet.write(0,2,'Patron Number', eformatlabel)
worksheet.write(0,3,'Patron Name', eformatlabel)
worksheet.write(0,4,'Hold Placed', eformatlabel)
worksheet.write(0,5,'Hold Expires', eformatlabel)
worksheet.write(0,6,'Frozen', eformatlabel)
worksheet.write(0,7,'Pickup Location')
worksheet.write(0,8,'Item Number', eformatlabel)
worksheet.write(0,9,'Item Location')
worksheet.write(0,10,'Item Status')

for rownum, row in enumerate(rows):
    worksheet.write(rownum+1,0,row[0], eformat)
    worksheet.write(rownum+1,1,row[1], eformat)
    worksheet.write(rownum+1,2,row[2])
    worksheet.write(rownum+1,3,row[3], eformat)
    worksheet.write(rownum+1,4,row[4], eformat)
    worksheet.write(rownum+1,5,row[5], eformat)
    worksheet.write(rownum+1,6,row[6], eformat)
    worksheet.write(rownum+1,7,row[7])
    worksheet.write(rownum+1,8,row[8], eformat)
    worksheet.write(rownum+1,9,row[9])
    worksheet.write(rownum+1,10,row[10])

    
    

workbook.close()


#Creating the email message
msg = MIMEMultipart()
msg['From'] = emailfrom
if type(emailto) is list:
    msg['To'] = ','.join(emailto)
else:
    msg['To'] = emailto
msg['Date'] = formatdate(localtime = True)
msg['Subject'] = emailsubject
msg.attach (MIMEText(emailmessage))
part = MIMEBase('application', "octet-stream")
part.set_payload(open(excelfile,"rb").read())
encoders.encode_base64(part)
part.add_header('Content-Disposition','attachment; filename=%s' % excelfile)
msg.attach(part)

#Sending the email message
smtp = smtplib.SMTP(emailhost, emailport)
smtp.sendmail(emailfrom, emailto, msg.as_string())
smtp.quit()








