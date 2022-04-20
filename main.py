import smtplib
from sys import exit
import json
from time import sleep

#parse tool settings
with open('settings.json') as f:
    settings = json.load(f)

#parse victim list
with open('victims.txt') as f:
    raw_victims = f.readlines()
    victims = []
    for victim in raw_victims:
        if victim.replace('\n', '') != '':
            victims.append(
                victim.replace('\n', '')
            )


try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
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
                msg.replace('%victim%', victim_user)#message
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