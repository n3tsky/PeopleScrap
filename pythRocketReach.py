#!/usr/bin/env python
import sys
from argparse import ArgumentParser, RawTextHelpFormatter
import requests
from signal import signal, SIGINT
import json
from time import sleep
from tabulate import tabulate

# Constant
API_KEY=""
URL_BASE="https://api.rocketreach.co/v1/api/search"
USER_AGENT="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0"
DEFAULT_WAIT=2
# Color
GREEN="\033[0;32m"
RED="\033[0;31m"
ORANGE="\033[0;33m"
NOCOLOR="\033[0m"
# Global
USER_DATA = list()

## Functions
# Perform HTTP query
def make_query(HTTP_REQ):
    headers = {
        "User-Agent": "%s" % (HTTP_REQ["user-agent"]),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept_language": "en-US,en;q=0.5",
        "Accept_encoding": "gzip, deflate, br"
    }
    return requests.get(HTTP_REQ["url"], headers=headers, proxies=HTTP_REQ["proxy"])

def http_query(HTTP_REQ):
    try:
        return make_query(HTTP_REQ)
    except requests.exceptions.HTTPError as e:
        print "[!] Exception while performing HTTP request to %s" % (HTTP_REQ["url"])
        return None

def encode(value):
    if type(value) == str or type(value)==unicode:
        return value.encode("utf-8", "ignore")
    elif value == None:
        return ""
    else:
        return str(value)

# End function - write results in file
def end_write(filename):
    print "[*] Writing data to \"%s\"" % (filename)
    write_2_file(filename, "Id;Name;City;Country;Job title;Employer", "w")
    for a in USER_DATA:
        del a[2]
        # Ought to find a better way than this
        a[0] = encode(a[0])
        a[1] = encode(a[1])
        a[2] = encode(a[2])
        a[3] = encode(a[3])
        a[4] = encode(a[4])
        data_out = ";".join(map(str,a)).replace("\n","")
        write_2_file(filename, data_out)

# End function - display results to user
def end_display():
    print "[*] Display results:"
    for a in USER_DATA:
        del a[2] # Remove status
        if a[4] != None:
            a[4] = a[4][0:30]
    display_data(USER_DATA, ["ID", "Name", "City", "Country", "Job title", "Employer"])

# Display data to user (grid)
def display_data(data, headers):
    print(tabulate(data, headers, "grid"))

# Check if value is in given dictionary or return None
def check_and_get(d, value):
    return d[value] if value in d else None

# Parse JSON result
def parse_json(data, needed):
    g = list()
    for d in data:
        l = list()
        for n in needed:
            l.append(check_and_get(d, n))
        g.append(l)
    return g

def parse_RR_API(json_data):
    profiles = check_and_get(json_data, "profiles")
    NEEDED = ["id", "name", "status", "city", "country_code", "current_title", "current_employer"]
    return parse_json(profiles, NEEDED)

def fetch_people_RR(HTTP_REQ, company, page_start=1, page_size=100):
    HTTP_REQ["url"] = "%s?api_key=%s&company=%s&page_size=%d&start=%d" % (URL_BASE, API_KEY, company, page_size, page_start)
    req = http_query(HTTP_REQ)
    if req.status_code == 200:
        try:
            json_data = json.loads(req.text)
            return json_data
        except ValueError as e:
            print e
    else:
        print "Error"
        print req.text
    return None

def fetch_RR(HTTP_REQ, company):
    global USER_DATA
    json_data = fetch_people_RR(HTTP_REQ, company)
    if json_data != None:
        pagination = check_and_get(json_data, "pagination")
        print "[*] Total people: %d" % (pagination["total"])
        current_page = pagination["thisPage"]
        next_page = pagination["nextPage"]
        while current_page != next_page:
            print "[*] People: %d - %d" % (current_page, next_page)
            USER_DATA += parse_RR_API(json_data)
            json_data = fetch_people_RR(HTTP_REQ, company, next_page)
            # Get new page
            pagination = check_and_get(json_data, "pagination")
            current_page = pagination["thisPage"]
            next_page = pagination["nextPage"]

## Generic functions
# SIGINT handler
def interruptHandler(signal, frame):
    end_display()
    print "\n[!] Interrupted by user.\nStopping..."
    sys.exit(0)

# Write data to file
def write_2_file(filename, data, access="a"):
    with open(filename, access) as fout:
        fout.write(data+"\n")
# Main
def main(args):
    global USER_DATA
    # Set up HTTP_REQ
    HTTP_REQ = {}
    HTTP_REQ["user-agent"] = USER_AGENT #args.user
    HTTP_REQ["proxy"] = {} if (len(args.proxy) == 0) else {"https": args.proxy, "http": args.proxy}
    HTTP_REQ["time"] = args.t

    print "[-] Starting %s" % (sys.argv[0])
    print "[*]   User-Agent: %s" % (HTTP_REQ["user-agent"])
    print "[*]   Proxy: %s" % (HTTP_REQ["proxy"])
    print "[*]   Time: %ss." % (HTTP_REQ["time"])
    if args.write:
        print "[*]   Write to file: \"%s\"\n" % (args.write)

    company = args.c
    
    print "\n[*] Looking for people in \"%s%s%s\"" % (ORANGE, company, NOCOLOR)
    fetch_RR(HTTP_REQ, company)
    end_display()
    if args.write:
        end_write(args.write)

# Parse arguments
def parse_args():
    parser = ArgumentParser(description="Python utility to query RocketReach API", formatter_class=RawTextHelpFormatter)
    parser.add_argument("-c", required=False, metavar="company", help="Search people in company")
    parser.add_argument("-t", required=False, metavar="time", default=DEFAULT_WAIT, type=int, help="Time to wait between requests (default: %ss.)" % DEFAULT_WAIT)
    parser.add_argument("--write", required=False, metavar="<file>", help="Output results to file (csv)")
    parser.add_argument("--user", required=False, metavar="User-agent", default=USER_AGENT, help="Change default user-agent (default: %s)" % USER_AGENT)
    parser.add_argument("--proxy", required=False, metavar="proxy", default="", help="Proxy to perform HTTP requests (ie.: http://localhost:8080, socks://localhost:8080)")
    args = parser.parse_args()
   
    if (not args.c):
        print "[!] %s requires a company name (-c)\nExiting..." % (sys.argv[0])
        sys.exit(1)
    return args

if __name__ == "__main__":
    signal(SIGINT, interruptHandler)
    args = parse_args()
    main(args)
