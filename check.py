#!/usr/bin/env python3

import requests
import json
from pprint import pprint
try:
    import smtplib
except:
    print("Bitte das Modul smtplib installieren mit \"pip3 install smtplib\"")

try:
    import config
except:
    print("Bitte das Modul config installieren mit \"pip3 install config\"")



def checkAvailability():
    url = "https://impfterminradar.de/api/vaccinations/availability"
    head = {
        "Accept": "application/json"
    }


    with open("patch.json") as f:
        data = json.load(f)

    r = requests.patch(url, json=data, headers=head)
    result = r.json()
    pprint(result)

    available = [x for x in result if x["Available"] ]

    print("Vefügbar:")
    pprint(available)
    return available



def sendmail(available):
    gmail_user = config.username
    gmail_password = config.password
    sent_from = gmail_user
    to = gmail_user
    subject = "Impftermin"
    body = available

    email_text = "From: " + str(sent_from) + "\nTo: " + str(to) + "\nSubject: " + str(subject) + "\n\n" +  str(body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print("Email sent!")
    except Exception as e:
        print("Something went wrong: " + str(e))


available = checkAvailability()

if available != []:
    sendmail(available)
else:
    print("Es sind keine Termine verfügbar")