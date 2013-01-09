#!/usr/bin/python2

"""
ec2-init.py
---------------------------
Initialize Amazon EC2 Host

Brian Parsons <brian@pmex.com>

Originally Forked from ec2arch by Yejun Yang <yejunx AT gmail DOT com>
https://github.com/yejun/ec2arch/raw/master/ec2
https://aur.archlinux.org/packages.php?ID=40083


Features:
---------
Sets hostname based on instance user-data hostname


Requires:
---------
boto - https://github.com/boto/boto


Changelog:
----------
2012-06-20 - bcp - added bootalert
2012-06-20 - bcp - grabs domain name from user-data and sets DNS for instance  ID
2012-09-15 - bcp - added additional grep for hostname and domainname in case both are returned
2012-      - bcp - updated for systemd, bash functions moved to single python script


"""

import datetime
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

# TODO
# Move variables to /etc/systemd/ec2-init.conf
#
mailto = "brian@pmex.com"
mailfrom = "bootalert@brianparsons.net"

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
hostfile = open('/etc/hostname', 'w')
hostfile.write(hostname)
hostfile.write('\n')
hostfile.close()

# set hostname with the system
subcmd = "hostname " + hostname
subprocess.call(subcmd,shell=True)

# TODO
# set root key if it doesn't exist
# if file not exist  /root/.ssh/authorized_keys
# loop through public-keys, save to file
#

updatedns(hostname, PUBLICIP)

messageheader = "From: EC2-Init <" + mailfrom + ">\n"
messageheader += "To: " + mailto + "\n"
messageheader += "Subject: " + hostname + "\n\n"
message = messageheader + hostname + " booted " + now.strftime("%a %b %d %H:%M:%S %Z %Y") + ". A " + INSTANCETYPE + " in " + AVAILABILITYZONE + " with IP: " + PUBLICIP + ".\n\n"

try:
   smtpObj = smtplib.SMTP('localhost')
   smtpObj.sendmail(mailfrom, mailto, message)
   print "Successfully sent boot alert email"
except SMTPException:
   print "Error: unable to send boot alert email"

