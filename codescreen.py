#!/usr/bin/env python3

import argparse
import csv
import ipaddress
import json
import sys


def read_server_csv_file(fname):
    """
    Read a server csv file

    Expects a csv file of the format
        hostname, serial_number, ip_address, netmask, gateway_ip
    
    Arguments:
        fname {str} -- file name of server csv file to read
    
    Returns:
        data -- dict of servers indexed by serial number
    """
    data = {}
    with open(fname) as csv_data:
        csv_reader = csv.reader(csv_data)
        row_num = 0
        for row in csv_reader:
            row_num += 1
            if row[0] == 'hostname' and row_num == 1:
                continue  # ignore first line if first field looks like header
            # no leading/trailing spaces in hostnames
            row[0] = row[0].strip()
            data[row[1]] = {'hostname': row[0],
                            'serial': row[1],
                            'ip': row[2],
                            'netmask': row[3],
                            'gateway': row[4]}
    return data


def is_valid_network_data(server):
    """
    Check validity of ip, netmask and gateway information

    Arguments:
        server {dict} -- server data in a dictionary
    
    Returns:
        {bool} -- True if valid network information

    """
    # good ip?
    try:
        good_ip = ipaddress.ip_address(server['ip'])
    except ValueError:
        print(server, file=sys.stderr)
        print('invalid IP: "{}"'.format(server['ip']), file=sys.stderr)
        return False

    # good gateway ip?
    try:
        good_gateway_ip = ipaddress.ip_address(server['gateway'])
    except ValueError:
        print(server, file=sys.stderr)
        print('invalid gateway IP: "{}"'.format(server['gateway']), file=sys.stderr)
        return False

    # good netmask?
    try:
        good_ip_network = ipaddress.ip_network('{}/{}'.format(server['ip'], server['netmask']), strict=False)
    except ValueError:
        print(server, file=sys.stderr)
        print('invalid netmask: "{}"'.format(server['netmask']), file=sys.stderr)
        return False

    # gateway is in network?
    if good_gateway_ip in good_ip_network:
        return True
    else:
        print(server, file=sys.stderr)
        print('invalid: gateway {} not in {} network'.format(good_gateway_ip, good_ip_network), file=sys.stderr)
        return False


def get_args():
    parser = argparse.ArgumentParser(description="newserver serial number lookup tool")
    parser.add_argument('-f', '--file', action='store', default='newservers.csv',
                        help='filename to read, defaults to newservers.csv')
    parser.add_argument('serial_number', metavar='SN', help='serial number to search for')
    args = parser.parse_args()
    return args
    

def main():
    args = get_args()
    server_data = read_server_csv_file(args.file)
    if args.serial_number in server_data:
        if is_valid_network_data(server_data[args.serial_number]):
            print(json.dumps(server_data[args.serial_number]))
        else:
            sys.exit(1)
    else:
        print('serial number {} not found'.format(args.serial_number), file=sys.stderr)
        sys.exit(0)

if __name__ == '__main__':
    main()
