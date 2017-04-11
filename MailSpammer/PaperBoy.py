"""
Author: Jasper Lelijveld
Date: april 2017
PaperBoy is a script that uses an excel sheet with info to send emails to people.
"""
import smtplib
import csv

def load():
    infotable = []
    with open('Data.csv', 'r') as csvfile:
        print 'Data opened'
        info = csv.reader(csvfile, delimiter=',')
        for row in info:
            infotable.append(row)
        print infotable
        csvfile.close()
        print 'Data loaded'
    return infotable

def main():
    infotable = load()
    while True:
        print 'Do you use:\nA) Gmail\nB) Outlook'
        mailProvider = str(raw_input())
        if mailProvider == 'A':
            server = 'smtp.gmail.com'
            break
        elif mailProvider == 'B':
            server = 'smtp-mail.outlook.com'
            break
    email = str(raw_input('Email adress: '))
    password = str(raw_input('Password: '))
    subject = str(raw_input('Subject: '))
    smtpObj = smtplib.SMTP(server, 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(email, password)
    for info in infotable:
        print 'sending email...'
        smtpObj.sendmail(email, info[1], 'Subject: %s\nHey %s,\n Volgens de borrellijst heb je nog $%s schuld.\n'
                                         'Met vriendelijke groet,\nJasper' % (subject, info[0], info[2]))
        print 'email send'
    smtpObj.quit()
    print 'Done'

main()