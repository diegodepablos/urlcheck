#! /usr/bin/env python

# imports
import  sys, urllib2, hashlib, os, ssl, requests
from urlparse import urlparse
from bs4 import BeautifulSoup

data_file = ".urlcheck.data"
mailgun_url = "MAILGUN API_URL"
mailgun_apikey = "MAILGUN API_KEY"
mailgun_from = "John Doe <mailgun@MAILGUN_DOMAIN>"
mailgun_to = ["example1@gmail.com", "example2@gmail.com"]

def uri_ok(url):
    try:
	result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False

def write_data(file, url, checksum):
	file = open(file, "a")
        file.write("%s;%s\n" % (url,checksum))
        file.close()
 
if len(sys.argv) == 2:
	if (uri_ok(sys.argv[1])):
		ssl._create_default_https_context = ssl._create_unverified_context
		response = urllib2.urlopen(sys.argv[1])
		html = response.read()
		soup = BeautifulSoup(html, "html.parser")
		
		# Add custom filters here
		custom_html = soup.find("td", {"class": "class_dateFrom"})
		if custom_html:
			html = str(custom_html)
		
		checksum = hashlib.md5(html).hexdigest()
		# check if we have a previous version of the site
		if os.path.isfile(data_file) and os.access(data_file, os.R_OK):
			data = open(data_file).read().splitlines()
			if not data:
				print "no data in file"
				write_data(data_file, sys.argv[1], checksum)
			else:
				#search for the site
				#print '[%s]' % ', '.join(map(str, data))
				site_dictionary = {}
				for site in data:
					site_data = site.split(";")
					site_dictionary[site_data[0]] = site_data[1]
								 
				if (sys.argv[1] in site_dictionary):
					print "site exists! checksum is %s" % site_dictionary[sys.argv[1]]
					if checksum == site_dictionary[sys.argv[1]]:
						print "no changes in site"
					else:
						print "site has changed! new checksum is %s" % checksum
						site_dictionary[sys.argv[1]] = checksum
						#update file
						os.remove(data_file)
						for s in site_dictionary:
							write_data(data_file, s, site_dictionary[s])

						#Send email
						print "sending email..."
						print requests.post(
        						mailgun_url,
        						auth=("api", mailgun_apikey),
        						data={"from": mailgun_from,
              						"to": mailgun_to,
      							"subject": "Site %s has changes!" % sys.argv[1],
              						"text": "Please visit %s for recent changes." % sys.argv[1]})
				else:
					print "site doesn't exist!"
					write_data(data_file, sys.argv[1], checksum)
		else:
			print "file %s is not accesible, creating new one.." % data_file
			file = open(data_file, "w")
         		file.close()

			write_data(data_file, sys.argv[1], checksum) 

		sys.exit(0)
	else:
		print "%s is not a valid url" % sys.argv[1]
		sys.exit(2)
else:
	print "usage: %s url" % sys.argv[0]
	sys.exit(2)
