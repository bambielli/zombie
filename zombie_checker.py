import urllib.request
import os

"""
This script will be run by the cronjob every 30 minutes,
to check and make sure that zombie is available for purchase at the brewpub.
"""

def main():
	"""
	This is where the magic happens...
	"""

	beer_string = str(urllib.request.urlopen("http://www.3floyds.com/beers-to-go/").read())

	# cut the response string down to the section where they list the available beers for pickup
	delete_index_pre = beer_string.index('6-Packs')
	delete_index_post = beer_string.index('22-OZ')
	beer_string = beer_string[delete_index_pre:delete_index_post]

	if 'zombie' in beer_string or 'Zombie' in beer_string:
		return 0
	else:
		return 1


if not main(): # if main returns 0 (success), then hit the success url
	print ('Zombie')
	urllib.request.urlopen('http://www.doesfloydshavezombie.com/'+os.environ.get('zombie_on'))
else: # main did not find zombie, so hit the unsuccessful url
	print ('No zombie')
	urllib.request.urlopen('http://www.doesfloydshavezombie.com/'+os.environ.get('zombie_off'))

