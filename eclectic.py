#!/usr/bin/python

import boto.ec2
from time import sleep
from ConfigParser import RawConfigParser

debug = False

class Context:
    access_key = None
    secret_key = None
    ssh_key = None
    security_group = None
    region = None
    os = None
    
    def get_ami(self):
        return self.ami_id.get(self.os.lower())
    
    ami_id = {
        'ubuntu 12.04': 'ami-d0f89fb9',
        'centos 6.4': 'ami-bf5021d6',
        'rhel 6.4': 'ami-7d0c6314',
        'rhel 5.9': 'ami-cf5b32a6',
        'amazon': 'ami-05355a6c',
    }

def debug(func):
    def decorator(*args, **kwargs):
        if debug:
            print '[debug] calling {0}'.format(func.__name__)
            for thing in args:
                print '\t-- {0}'.format(thing)
            for name, value in kwargs.items():
                print '\t-- {0} = {1}'.format(name, value)
        return func(*args, **kwargs)
    return decorator

@debug
def initiate(region, access_key, secret_key):
    conn = boto.ec2.connect_to_region(region,
                                    aws_access_key_id = access_key,
                                    aws_secret_access_key = secret_key)
    return conn

@debug
def spawn(conn, ami_id, size, key, sec, count):
    reservation = conn.run_instances(ami_id,
                                    min_count = 1,
                                    max_count = count,
                                    key_name = key,
                                    instance_type = size,
                                    security_groups = [sec])
    return reservation

@debug
def collect_info(reservation):
    hostnames = []
    for instance in reservation.instances:
        public_dns = instance.public_dns_name
        while public_dns == '':
            sleep(1)
            instance.update()
            public_dns = instance.public_dns_name
        hostnames.append(public_dns)
    return hostnames

@debug
def run(cxt):
    conn = initiate(cxt.region, cxt.access_key, cxt.secret_key)
    res = spawn(conn, cxt.get_ami(), cxt.size, cxt.ssh_key, cxt.security_group, cxt.count)
    collect_info(res)

@debug
def get_config(cxt):
    import ConfigParser, os
    config = ConfigParser.ConfigParser()
    config.read(['.eclectic', os.path.expanduser('~/.eclectic')])
    
    cxt.access_key = config.get('eclectic', 'access_key')
    cxt.secret_key = config.get('eclectic', 'secret_key')
    cxt.ssh_key = config.get('eclectic', 'ssh_key')
    cxt.security_group = config.get('eclectic', 'security_group')
    cxt.region = config.get('eclectic', 'region')
    return cxt

@debug
def get_args(cxt):
    from argparse import ArgumentParser
    main_parser = ArgumentParser(description='Streamlined CLI and deployment tool for AWS EC2')
    main_parser.add_argument('-c',
                            '--count',
                            help = 'Number of servers to instantiate (defaults to 1)',
                            default = 1,
                            required = False,
                            type = int)
    main_parser.add_argument('-o',
                            '--os',
                            help = 'Operating system to spawn (defaults to Ubuntu 12.04)',
                            default = 'ubuntu 12.04',
                            nargs = '+',
                            required = False)
    main_parser.add_argument('-s',
                            '--size',
                            help = 'Size of instance (defaults to m1.small)',
                            default = 'm1.small',
                            required = False)
    args = main_parser.parse_args()
    cxt.os = args.os
    cxt.size = args.size
    cxt.count = args.count
    return cxt

def main():
    cxt = Context()
    get_config(cxt)
    get_args(cxt)
    run(cxt)

if __name__ == "__main__":
    main()