#!/usr/bin/python2

"""
ec2-init.py
---------------------------
Initialize Amazon EC2 Host

Brian Parsons <brian@pmex.com>


Features:
-------------
Sets hostname based on instance user-data hostname
Sends email with hostname, instance type, and IP address
Will update DNS in Route53 if boto finds credentials or has IAM role and zone file is found


Requires:
------------
boto - https://github.com/boto/boto


Changelog:
---------------
2012-06-20 - bcp - added bootalert
2012-06-20 - bcp - grabs domain name from user-data and sets DNS for instance  ID
2012-09-15 - bcp - added additional grep for hostname and domainname in case both are returned
2012-12-14 - bcp - updated for systemd, bash functions moved to single python script
2013-01-14 - bcp - grabs public keys from metadata and creates or updates authorized_keys for root
2013-01-14 - bcp - pulls mailto, mailfrom from user metadata or config file /etc/conf.d/ec2-init

"""

import ConfigParser
import datetime
import os
import re
import socket
import smtplib
import sys
import subprocess
import urllib

from boto.route53.connection import Route53Connection
from boto.route53.record import ResourceRecordSets
from boto.route53.exception import DNSServerError
from boto.utils import get_instance_metadata, get_instance_userdata
from socket import gethostname

########
##
## updatedns - Updates DNS for given hostname to newip 
##
#

def updatedns(hostname, newip):
    try:
       hostname
    except NameError:
       print 'Hostname not specified and not able to detect.'
       return(1)

    # Add trailing dot to hostname if it doesn't have one
    if hostname[-1:] != ".":
        hostname += "."

    print 'Hostname: %s' % hostname
    print 'Current IP: %s' % newip

    # Initialize the connection to AWS Route53
    route53 = Route53Connection()

    # Get the zoneid
    try:
        route53zones = route53.get_all_hosted_zones()
    except DNSServerError,  e:
        print 'Connection error to AWS. Check your credentials.'
        print 'Error %s - %s' % (e.code,  str(e))
        return(1)

    for zone in route53zones['ListHostedZonesResponse']['HostedZones']:
        if zone['Name'][0:-1] in hostname:
            zoneid = zone['Id'].replace('/hostedzone/', '')
            print 'Found Route53 Zone %s for hostname %s' % (zoneid,  hostname)

    try:
        zoneid
    except NameError:
        print 'Unable to find Route53 Zone for %s' % hostname
        return(1)

    # Find the old record if it exists
    try:
        sets = route53.get_all_rrsets(zoneid)
    except DNSServerError,  e:
        print 'Connection error to AWS.'
        print 'Error %s - %s' % (e.code,  str(e))
        return(1)

    for rset in sets:
        if rset.name == hostname and rset.type == 'A':
            curiprecord = rset.resource_records
            if type(curiprecord) in [list, tuple, set]:
                for record in curiprecord:
                    curip = record
            print 'Current DNS IP: %s' % curip
            curttl = rset.ttl
            print 'Current DNS TTL: %s' % curttl

            if curip != newip:
                # Remove the old record
                print 'Removing old record...'
                change1 = ResourceRecordSets(route53, zoneid)
                removeold = change1.add_change("DELETE", hostname, "A", curttl)
                removeold.add_value(curip)
                change1.commit()
            else:
                print 'IPs match,  not making any changes in DNS.'
                return

    try:
        curip
    except NameError:
        print 'Hostname %s not found in current zone record' % hostname


    # Add the new record
    print 'Adding %s to DNS as %s...' % ( hostname,  newip)
    change2 = ResourceRecordSets(route53, zoneid)
    change = change2.add_change("CREATE", hostname, "A", 60)
    change.add_value(newip)
    change2.commit()

# Parse Config File
config = ConfigParser.ConfigParser()
config.read("/etc/conf.d/ec2-init")
try:
    confmailto = config.get("ec2-init", "mailto")
    confmailfrom = config.get("ec2-init", "mailfrom")
    sendemail = config.get("ec2-init",  "sendemail")
except ConfigParser.NoSectionError: 
    print("Config file /etc/conf.d/ec2-init not found")
    
# Collect Meta Data
inst_data = get_instance_metadata()
INSTANCETYPE=inst_data["instance-type"]
INSTANCEID=inst_data["instance-id"]
PUBLICIP=inst_data["public-ipv4"]
PUBLICKEYS=inst_data["public-keys"]
AVAILABILITYZONE=inst_data["placement"]["availability-zone"]
now = datetime.datetime.now()
user_data = get_instance_userdata(sep='|')

try:
    hostname = user_data['hostname']
except NameError:
    hostname = gethostname()

# set hostname in /etc/hostname
try:
    with open('/etc/hostname', 'w') as hostfile:
        hostfile.write(hostname)
        hostfile.write('\n')
        hostfile.close()
except IOError as e:
        print('Could not open /etc/hostname for writing' + e)

# set hostname with the system
subcmd = "hostname " + hostname
subprocess.call(subcmd,shell=True)

# make sure /root/.ssh exists
if not os.path.exists('/root/.ssh'):
    os.makedirs('/root/.ssh')
    os.chmod('/root/.ssh',0700)

# save public key to authorized_keys file
if type(PUBLICKEYS.items()) in [list, tuple, set]:
    try:
        currentkeys = open('/root/.ssh/authorized_keys').read()
    except IOError as e:
        currentkeys = ""
    try:
        with open('/root/.ssh/authorized_keys', 'a') as authkeyfile:
            for key in PUBLICKEYS.items():
                if  not key[1][0]  in currentkeys:
                    authkeyfile.write(key[1][0])
                    authkeyfile.write('\n')
            authkeyfile.close()
            os.chmod('/root/.ssh/authorized_keys',0600)
    except IOError as e:
            print 'Could not open authorized_keys file for writing!' + e

# update dns
updatedns(hostname, PUBLICIP)

if sendemail == True:

    # Get mail to address from user metadata or conf file or default to root
    try:
        mailto = user_data['mailto']
    except KeyError:
        mailto = confmailto
    except NameError:
        mailto = "root"
    
    # Get mail from address from user metadata or conf file or default to root
    try:
        mailfrom = user_data['mailfrom']
    except KeyError:
        mailfrom = confmailfrom
    except NameError:
        mailfrom = "root"
        
    # compose boot email
    messageheader = "From: EC2-Init <" + mailfrom + ">\n"
    messageheader += "To: " + mailto + "\n"
    messageheader += "Subject: " + hostname + "\n\n"
    message = messageheader + hostname + " booted " + now.strftime("%a %b %d %H:%M:%S %Z %Y") + ". A " + INSTANCETYPE + " in " + AVAILABILITYZONE + " with IP: " + PUBLICIP + ".\n\n"
    
    # send boot email
    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(mailfrom, mailto, message)
    except smtplib.SMTPException:
        print("Error: unable to send boot alert email")
    
