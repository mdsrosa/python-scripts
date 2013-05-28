# -*- coding: utf-8 -*-
"""
  Script to monitor a replication slave server mysql

  @author: Matheus Rosa <matheus.rosa@mltcorp.com.br>
  @date: 2013-01-10
"""
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import datetime,smtplib,os
import subprocess
import re
import socket
import fcntl
import struct

#MYSQL
MYSQL_USER = 'your_user'
MYSQL_PASSWD = 'your_password'

# EMAIL
FROM = "your_from_email"
SMTP_SERVER = 'your_smtp_server'
SMTP_PORT = 587
TO = ['emails_of_who_will_receive_the_notification']
AUTH_EMAIL = "your_auth_email"
AUTH_PASS = "your_auth_password"



def get_ip_address(ifname):
    """
    Returns the ip of the machine from which the script is running
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def get_slave_status(format_type='txt'):
   """
   Returns the plain/text message of the slave servers's current status
   """
   command = ["mysql", "-u%s" % MYSQL_USER, "-p %s" % MYSQL_PASSWD, "-e show slave status"]
   
   if format_type == 'html':
       command.append("-H")
       
   output = subprocess.check_output(command)

   return output

def slave_status_is_ok():
   """
   Runs a mysql command that returns a plain/text message of the
   slave server's current status. Then, searches for 2 occurrences
   of the word 'Yes' in that message. If there is 2 occurrences,
   it means that slave server is fine, otherwise, its fucked up.
   """
   output = get_slave_status()

   occurrences = [m.start() for m in re.finditer('Yes', output)]

   return (len(occurrences) == 2)

def send_email_notification(send_to, subject, text):
    """Sends a email"""
    assert type(send_to)==list
    
    msg = MIMEMultipart()
    msg['From'] = FROM
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    part = MIMEBase("text", "html")
    part.set_payload(text)
    msg.attach(part)

    mailServer = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(AUTH_EMAIL, AUTH_PASS)
    mailServer.sendmail(FROM, send_to, msg.as_string())
    mailServer.close()


if __name__ == '__main__':
    
   now = datetime.datetime.now()
   text = get_slave_status(format_type='html')
   slave_status_log = open("slave_status.log", "a")
   server = get_ip_address('eth0')
   
   if not slave_status_is_ok():
      msg = '[%s] Slave server %s\'s replication is NOT ok!' % (now, server)
      msg += '\nSending a email notification to %s' % (','.join(TO))
      send_email_notification(TO, 'Replication Server (%s): An error occurred!' % server, text)
   else:
      msg = '[%s] Slave server %s\'s replication is fine.\n' %  (now, server)

   slave_status_log.write(msg)
   slave_status_log.close()
