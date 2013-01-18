
# Initialize Amazon EC2 Arch Linux Instance

This script is meant to run on boot of an Arch Linux Amazon EC2 server image.

It creates or updates the hostname and root ssh access keys upon boot.

## Requirements

#### boto - Arch Package: python2-boto 

#### python2 - Arch Package python2

#### postfix - Arch Package postfix

## Features

Sets hostname based on instance user-data hostname
Sends email with hostname, instance type, and IP address
Will update DNS in Route53 if boto finds credentials or has IAM role and zone file is found

## Usage

This script will find the following metadata if listed in the user-metadata
field of the instance as key value pairs delimited by pipes (|):

* hostname - the hostname to set for the instance
* mailto - the address to email with a message listing the instance information and ip address
* mailfrom - the from address of the message
* sendemail - 1 or 0 on whether or not to send the email (Default: 1)

Additionally if IAM role is granted permission to Route53 or
if boto credentials are found in /root/.boto, the script will
create or update a DNS entry for the hostname if it finds a matching zone
in Route53

Finally, the script sends an email message to a specified address listing the
hostname, instance type, and external IP address of the instance. This requires
a functioning MTA on the image.

The script will attempt to get mailto, mailfrom and sendemail from a configuration file: /etc/conf.d/ec2-init

If no configuration file is found and mailto, mailfrom are not specified in user-metadata for the instance,
it will send the message to root from root.

## License

This script is distributed under the MIT License (see LICENSE)
