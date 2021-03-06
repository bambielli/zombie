import requests
import os

"""
This script will be run by the cronjob every 30 minutes,
to check and make sure that zombie is available for purchase at the brewpub.
"""

def main ():
	"""
	This is where the magic happens...
	"""

	hdrs = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		'Accept-Encoding': 'none',
		'Accept-Language': 'en-US,en;q=0.8',
		'Connection': 'keep-alive'} # pass headers so we don't look like a robot.

	url = "https://www.3floyds.com/beers-to-go/"

	beer_string = requests.get(url, headers=hdrs).text;

	#try to find the zombie-dust URL
	try:
		beer_string.index('https://www.3floyds.com/beer/zombie-dust/')
		return 1
	except ValueError:
		return 0


if main(): # if main returns 0 (success), then hit the success url
	print ('Zombie')
	requests.get(os.environ.get('BASE_URL') + os.environ.get('zombie_on'))
else: # main did not find zombie, so hit the unsuccessful url
	print ('No zombie')
	requests.get(os.environ.get('BASE_URL') + os.environ.get('zombie_off'))

