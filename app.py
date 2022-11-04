import requests
import functions
import config

URL = 'https://www.corsair.com/us/en/p/json/CP-8920284'

def get_status():
    r = requests.get(URL)
    j = r.json()
    return j['stock']['stockLevelStatus']['code']

functions.validate()
in_stock = True if get_status() != 'outOfStock' else False
if in_stock:
    msg = 'Update on 12VHPWR cable. Change detected on Corsair\'s website. Check %s' % URL
    print(functions.sendTxt(config.twilio_phone, msg))
    functions.lockScript()
functions.logData(['in_stock'],{'in_stock': in_stock})