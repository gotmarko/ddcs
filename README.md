# Mark Osbourne Code Screen

## Setup
For MacOS or Linux, Windows is left as an exercise for the reader.
```
git clone https://github.com/gotmarko/ddcs.git
cd ddcs
virtualenv -p python3 venv
source venv/bin/activate
```

## Usage
```
[venv] $ ./codescreen.py -h
usage: codescreen.py [-h] [-f FILE] SN

newserver serial number lookup tool

positional arguments:
  SN                    serial number to search for

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  filename to read, defaults to newservers.csv
```

## Examples
```
[venv] $ ./codescreen.py sn1012 # returns valid json on stdout
{"hostname": "server04", "serial": "sn1012", "ip": "192.168.18.22", "netmask": "255.255.255.0", "gateway": "192.168.18.1"}

[venv] $ ./codescreen.py sn9999 # not found, returns exit code 0, no output
[venv] $ echo $?
0
```
If there are errors in the network config, the record and error message are returned to stderr and return code is 1:
```
[venv] $ ./codescreen.py sn1021
{'hostname': 'server07', 'serial': 'sn1021', 'ip': '192.168.1.225', 'netmask': '255.255.255.0', 'gateway': '192.168.12.1'}
gateway 192.168.12.1 not in 192.168.1.0/24 network
[venv] $ echo $?
1
```
