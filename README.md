# urlcheck

UrlCheck is little script that verifies if a site has changed since last check.

You can setup a MailGun account to send emails. Please refer to https://www.mailgun.com/

# Usage

  ./urlcheck.py http://wwww.google.com/
  
To enable periodic checks, please add it as a crontab task, this example will check http://camas.sedelectronica.es/board every day at 9:00 am:

0 9 * * * /home/pi/urlcheck.py http://camas.sedelectronica.es/board

  
 
