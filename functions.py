from pathlib import Path

from classes import Contact
from datetime import datetime
import json, config, csv, os

def logData(fieldnames, row):
    logname = 'log.csv'
    flag_exists = True if os.path.isfile(logname) else False
    with open('log.csv', 'a+') as csvfile:
        fieldnames = fieldnames
        fieldnames.insert(0,'date')
        date_dict = {'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        row.update(date_dict)
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not flag_exists:
            csvwriter.writeheader()
        csvwriter.writerow(row)

def lockScript():
    lockJson = {'status': True}
    with open('lock.json', 'w') as output:
        json.dump(lockJson, output)

def checkLock():
    return json.loads(Path('lock.json').read_text())['status']

def configCheck(configField, configName):
    assert len(configField) > 0, configName +' not provided. Exiting'

def validate():
    assert checkLock() == False, 'Not unlocked. Or something is wrong with lock.json. Exiting.'
    try:
        checks = [(config.twilio_sid, 'Twilio SID'), (config.twilio_auth_token, 'Twilio Auth Token'), (config.twilio_msg_svc, 'Twilio Message Service')]
        for check in checks:
            cField, cName = check
            configCheck(cField, cName)
    except AttributeError:
        print('Config.py is missing attributes. Check config.py. Exiting.')
    except NameError:
        print('Check config.py. Something is undefined. Exiting.')

def genContacts(contacts):
    output = []
    for contact in contacts:
        output.append(Contact(contact['number'], contact['optins']))
    return output

def sendTxt(number,msg):
    from twilio.rest import Client
    client = Client(config.twilio_sid, config.twilio_auth_token)
    message = client.messages.create(
        messaging_service_sid = config.twilio_msg_svc,
        body = msg,
        to = number
    )
    return(message.sid)