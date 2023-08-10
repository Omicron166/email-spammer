import smtplib
from sys import exit
import json
from os.path import isfile
from time import sleep

#parse tool settings
if isfile('config.json'):
    with open('config.json', 'r') as f:
        settings = json.load(f)
else:
    settings = {
        "credentials": {
            "email": "",
            "password": ""
        },
        "server": {
            "ip": "smtp.gmail.com",
            "port": 587
        },
        "template": ""
    }
    with open('config.json', 'w') as f:
        json.dump(settings, f)
    print('[!] Please check and fill config.json')
    exit()

#parse victim list
if isfile('victims.txt'):
    with open('victims.txt') as f:
        raw_victims = f.readlines()
        victims = []
        for victim in raw_victims:
            if victim.startswith('#'): continue #skip lines with #
            if victim.replace('\n', '') != '': #check if empty line
                victims.append(
                    victim.replace('\n', '')
                )
else:
    with open('victims.txt', 'w') as f:
        f.writelines(["#Add an email per line\n"])
    print('[!] Please fill victims.txt')
    exit()


try:
    server = smtplib.SMTP(settings['server']['ip'], settings['server']['port'])
    server.ehlo()
    server.starttls()
    server.login(settings['credentials']['email'], settings['credentials']['password'])

    #parse the template
    msg = settings['template']

    #iterate throught the victim list
    for victim in victims:
        victim_user = victim.split('@')[0]

        #send the mail
        try:
            server.sendmail(
                settings['credentials']['email'], #attacker email addr
                victim, #victim email addr
                msg.replace('%victim%', victim_user) #in the template, %victim% is replaced by the victim user
            )
        except Exception as e:
            #set webhook telemetry
            print(e)
            print('[!] Server error')
            break

        #timeout to avoid connection ban
        sleep(1)
except KeyboardInterrupt:
    print('[-] Canceled')
    exit()
except smtplib.SMTPAuthenticationError:
    print('[!] Login error, check the email and password')
    exit()