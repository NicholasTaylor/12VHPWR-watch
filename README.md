# 12 Volt High Power Adapter Watcher
## Disclaimer
I guarantee and promise nothing. Use at your own risk. Know what you're doing (or consult someone who does) before attempting to use this. I assume no liability or responsibility for your use of this script. Just putting it up here in case others would like to set it up themselves.
## FAQ
### What does this thing do?
This is just a simple Python script for Corsair consumers who are having a rough time getting their hands on that elusive 12VHPWR cable from Corsair's US site.
### Isn't this redundant? Why not just use the Notify When In Stock Button?**
In my experience, such features don't actually notify the user in time (or even at all, in some cases) that a sought-after item is in stock. By the time you get the news, you're often stuck staring at another "Sold Out" button. And according to frustrated Reddit users, this Notify button is no exception. 
## Installation
### Prerequisites
* Basic familiarity with:
	* Cron, Crontab
	* Python, Pip, Virtualenv
	* Twilio
	* Command Line Interface, preferably Bash
	* JSON
	* Github
* A Raspberry Pi, Droplet, or any other simple, low-cost dedicated solution that can automatically run the scripts 24/7
* A Twilio account
* A text editor like Nano or Vim
* A phone (preferably a smartphone) with a number you can text
* 20 USD. For the cable. When you finally get a chance to buy the thing ;)

Again, I stress this should be a machine you're comfortable running 24/7. A Raspberry Pi could do it, but a little space on a IaaS (ex. DigitalOcean, AWS, Microsoft Azure, Google Compute) is recommended. Log into or boot up whatever you'll be using, open a terminal window, and get started.
### Downloading the Project
**Bash**
```
git clone https://github.com/NicholasTaylor/12VHPWR-watch.git
cd 12VHPWR-watch
```
### Installing Python Dependencies
**Note:** I use Ubuntu 20.04, Python 3.10, Virtualenv, and a DigitalOcean droplet in my setup which I'll be demonstrating here. Feel free to deviate from this as you see fit, but at your own risk.

**Bash (/)**
```
python3.10 -m venv venv
. venv/bin/activate
# For Windows/Powershell users, this will be ". venv/Scripts/activate"
pip install -r requirements.txt
cp config_template.py config.py
```
### Fill in config.py
Next, open `config.py` in the root of your `12VHPWR-watch` directory. It should look like this:

**Text Editor (/config.py)**
```
twilio_sid = "abcdef0123456789"
twilio_auth_token = "abcdef0123456789"
twilio_msg_svc = "abcdef0123456789"
twilio_phone = "+12345678901"
```
Let's go over what you need and where to enter it all in. First, access your Twilio account (Should be [here](https://www.twilio.com/console)). If you don't have a Twilio account, setting up one is beyond the scope of this readme. I recommend [setting up a Twilio account](https://www.twilio.com/try-twilio) then [following their tutorial](https://www.twilio.com/docs/usage/tutorials/how-to-use-your-free-trial-account).

That done, you'll need 4 things:
*  **Your account SID**
	* Should be right on the console dashboard if you click the link above
	* Copy/paste this to the `twilio_sid` variable in `config.py`
*  **Your auth token**
	* Right under the SID on the console dashboard
	* Copy/paste this to the `twilio_auth_token` variable in `config.py`
*  **Your message service SID**
	* Set up a service or use an existing one
	* Go to **Messaging** > **Services** in the left sidebar
	* Should be under the "SID" column for the service you want to use
	* Copy/paste this to the `twilio_msg_svc` variable in `config.py`
*  **Your phone number** (The one you want to be texted at. Your personal phone number. **Not** your Twilio account's phone number)
	* I really hope you don't need help finding this.
	* Wait, you need help finding your own phone number?
	* Seriously?
	* Damn.
	* Okay, if this is giving you a serious problem:
		1. Find a friend who also has a phone
		2. Call or text this friend
		3. See that big, scary 10-digit number that just appeared on the display of your friend's phone? 		
	* Congratulations, you found your number! Good job! Gold star!
	* Okay, all joking aside, there is a bit of trickery you have to do with your phone number. You have to preface the number with `+1` (or if you're not in the US or Canada, whatever country code you have), then your phone number **minus** any spaces or dashes. So, if your phone number is 415-555-1234, you'll need to enter it in the `twilio_phone` section as `+14155551234`.

Once you've entered in all you need, save and close `config.py`.
## Testing (Optional, but Recommended)
### Checking if the script can scan Corsair's site
Presumably, you still have the virtual environment activated. If so, you should have something like `(venv)` at the start of your command line prompt. If you don't, just run `. venv/bin/activate` again. Then, run:

**Bash (/)**
```
python app.py
```
#### If no output appears in the command line
This is normal! The script checked Corsair's site, found nothing, and logged the attempt. Check to see if you have a new file in the root directory - `log.csv`. There should be two columns - `date` and `in_stock` and two rows - a header row and one row of data. That one data row should have the date and time you just ran the script in the first column, then `False` in the next.
#### If you see a string of letters and numbers
You just lucked out in the best way imaginable. The script found a cord in stock in its test run. Hurry! Go and buy one before they go away again!
### Checking if the script can text your phone
In your text editor, open `app.py` in the root directory. Look for this line:
**Text Editor (/app.py)**
```
in_stock  =  True  if  get_status() !=  'outOfStock'  else  False
```
Make a new line under this one and enter this:

**Text Editor (/app.py)**
```
in_stock = True
```
Now, run `app.py` again:

**Bash (/)**
```
python app.py
```
The terminal should output a long string of letters and numbers. You phone should then get a text moments later. If so, everything is in good working order! Delete the `in_stock = True` line you just created. Then, save and close `app.py`.
### Checking if the lock file works
I built a simple locking mechanism, so that when this does find cords in stock, it texts you once and stops after that. If you open `lock.json` in your root folder via your text editor, you should see something like this:

**Text Editor (/lock.json)**
```
{"status":  true}
```
Try running the app again:

**Bash (/)**
```
python app.py
```
It should throw an error:

**Bash (/)**
```
Traceback (most recent call last):
  File "/home/nicholas/Code/12VHPWR-watch/app.py", line 12, in <module>
    functions.validate()
  File "/home/nicholas/Code/12VHPWR-watch/functions.py", line 32, in validate
    assert checkLock() == False, 'Not unlocked. Or something is wrong with lock.json. Exiting.'
AssertionError: Not unlocked. Or something is wrong with lock.json. Exiting.
```
This is working exactly as designed.
### Unlocking the lock file to re-enable the app
Just go back into `lock.json` and change `true` to `false`. Save `lock.json` and close. Run the app again. This time, there should be no errors.
## Deployment
This is pretty simple script that doesn't need a ton of bells and whistles, so I just used Cron to automate this. I just put in `crontab -e` and set it to run every 60 seconds at the top of every minute:

**Bash (running `crontab -e`)**
```
# */1 * * * * cd /home/nicholas/12VHPWR-watch/ && /home/nicholas/12VHPWR-watch/venv/bin/python /home/nicholas/12VHPWR-watch/app.py
```
Obviously, change all 3 instances of `/home/nicholas/` to the path of the parent directory for `12VHPWR-watch`.
If you want a different timing, just use [crontab.guru](https://crontab.guru/).
Once you're done, save and close the crontab file.
### Confirming the Cron Job Works
A few seconds after the top of the minute, open `log.json`. There should be new rows that indicate the script is running automatically.
## After a (Hopefully) Successful Session
Let's say the script finds something and lets you know. You bought your cord and are awaiting its shipment. Congrats! The lock file will keep the script from texting you over and over, but the script itself will still be running every 60 seconds. It'll just error out and do nothing. To save computing resources, reopen `crontab -e` in a terminal. At the start of the line you wrote, just add a `#` to comment out the cron job, save, and exit crontab.