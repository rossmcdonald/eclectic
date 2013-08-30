eclectic
========

Streamlined python CLI and deployment tool for AWS EC2.

## Requirements ##
* boto.ec2

## Getting Started ##
You will need to create an eclectic configuration file, that can be located in your current or home directory. The naming convention for this file is '.eclectic' and it should contain:
* AWS Access Key
* AWS Secret Key
* AWS Region to start instances in
* Name of AWS SSH key to instantiate instances with
* Security group you would like to instantiate insances with

Your config file should look something like:
```
[eclectic]
access_key = XXXXXXXXXXXX
secret_key = XXXXXXXXXXXXXXXXXXXXXXXXXXXX
ssh_key = my_key
security_group = secgroup1
region = us-east-1
```