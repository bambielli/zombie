import urllib.request

"""
This script will be run by the cronjob every 5 minutes, to check and make sure that zombie is available for purchase.
"""

def main():
	beer_string = str(urllib.request.urlopen("http://www.3floyds.com/beers-to-go/").read())

	# find the position of the FAQs string, and delete everything after it in the response.
	# the current beer offerings are before the FAQs section.
	delete_index_post = beer_string.index('22-OZ')
	delete_index_pre = beer_string.index('6-Packs')
	beer_string = beer_string[delete_index_pre:delete_index_post]

	if 'zombie' in beer_string or 'Zombie' in beer_string:
		return 0
	else:
		return 1

if not main():
	print ('Zombie')
else:
	print ('No Zombie')
