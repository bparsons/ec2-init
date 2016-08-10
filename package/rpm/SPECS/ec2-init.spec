# ec2-init 
#
# Maintainer: Brian Parsons <brian@pmex.com>
#
Summary: Initializes an EC2 Instance
Name: ec2-init
Version: 3.8
Release: 1
License: MIT
Source: ec2-init.tgz
URL: https://github.com/bparsons/ec2-init
Packager: Brian Parsons <brian@pmex.com>
requires: python, python-boto

%description
This initialization script performs the following operations:

Reads instance metadata for key value pairs delimited by pipes (|):

hostname - the hostname to set for the instance
mailto - the address to email with a message listing the instance information and ip address
mailfrom - the from address of the message
sendemail - 1 or 0 on whether or not to send the email (Default: 1)

If the hostname is defined, the script will creates or update the system hostname 
and update a corresponding DNS entry in Route53. In order for the DNS update to 
succeed, the instance needs to have an IAM permission to Route53 or boto credentials in /root/.boto. 
(See the boto documentation for more information)

Finally, the script will send an email to the defined address alerting that the instance is up 
along with the instance type and ip address.

%prep
rm -rf $RPM_BUILD_DIR/ec2-init
zcat $RPM_SOURCE_DIR/ec2-init.tgz | tar -xvf -

%files
%doc README.md
/usr/bin/ec2-init.py
/etc/default/ec2-init
/usr/lib/systemd/system/ec2-init.service

%install
install -D -m 600 ec2-init %{buildroot}/etc/default/ec2-init
install -D -m 700 ec2-init.py %{buildroot}/usr/bin/ec2-init.py
install -D -m 644 ec2-init.service %{buildroot}/usr/lib/systemd/system/ec2-init.service

