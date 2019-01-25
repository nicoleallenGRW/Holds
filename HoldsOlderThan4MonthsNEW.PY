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



excelfile =  'HoldsOlderThan4Months.xlsx'



#Set variables for email

emailhost = 'mail.greenwichlibrary.org'
emailport = '25'
emailsubject = 'Holds Older Than 4 Months'
emailmessage = '''Attached is a list of all holds that were placed more than 120 days ago. The list is sorted by call number, then material type, then title. If an item shows up more than once it is because it has multiple holds. If the hold cannot be fulfilled please open the record in Sierra, click on the bib-level hold tab, click on “modify holds” and add cancel to the hold note. Any amount of information can be added to the hold note as long as the word “cancel” is included.  Joan will be notified automatically once a week of all holds that will need to be canceled. Please let Nicole know if you have any questions.'''
emailfrom = 'nallen@greenwichlibrary.org'
emailto = ['nallen@greenwichlibrary.org','EMcCarthy@greenwichlibrary.org','MWeill@greenwichlibrary.org','JTrivedi@greenwichlibrary.org','DWaring@greenwichlibrary.org','MCurcio@greenwichlibrary.org','mjinno@greenwichlibrary.org','SSchugmann@greenwichlibrary.org','SSchmidt@greenwichlibrary.org']
#,

try:
    conn = psycopg2.connect("dbname= user= host= port= password= sslmode=require")
except psycopg2.Error as e:
    print ("Unable to connect to database: " + str(e))
    
cursor = conn.cursor()
cursor.execute(open("HoldsOlderThan4Monthsnew.sql","r",).read())
rows = cursor.fetchall()
conn.close()


workbook = xlsxwriter.Workbook(excelfile, {'remove_timezone': True})
worksheet = workbook.add_worksheet()


worksheet.set_landscape()
worksheet.hide_gridlines(0)



eformat= workbook.add_format({'text_wrap': True, 'valign': 'top' , 'num_format': 'mm/dd/yy'})
eformatlabel= workbook.add_format({'text_wrap': False, 'valign': 'top', 'bold': True})


worksheet.set_column(0,0,19.89)
worksheet.set_column(1,1,8.11)
worksheet.set_column(2,2,8.11)
worksheet.set_column(3,3,26.44)
worksheet.set_column(4,4,21.22)
worksheet.set_column(5,5,15.56)
worksheet.set_column(6,6,17)
worksheet.set_column(7,7,20)



worksheet.set_header('HoldsOlderThan4Months')

worksheet.write(0,0,'Call #', eformatlabel)
worksheet.write(0,1,'Bib No.')
worksheet.write(0,2,'Mat Type', eformatlabel)
worksheet.write(0,3,'Title', eformatlabel)
worksheet.write(0,4,'Author', eformatlabel)
worksheet.write(0,5,'Hold Placed', eformatlabel)
worksheet.write(0,6,'Hold Note', eformatlabel)
worksheet.write(0,7,'Pub Date', eformatlabel)

for rownum, row in enumerate(rows):
    worksheet.write(rownum+1,0,row[0], eformat)
    worksheet.write(rownum+1,1,row[1])
    worksheet.write(rownum+1,2,row[2], eformat)
    worksheet.write(rownum+1,3,row[3], eformat)
    worksheet.write(rownum+1,4,row[4], eformat)
    worksheet.write(rownum+1,5,row[5], eformat)
    worksheet.write(rownum+1,6,row[6], eformat)
    worksheet.write(rownum+1,7,row[7], eformat)
    
    

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








