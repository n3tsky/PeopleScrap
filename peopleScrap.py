#!/usr/bin/env python3
import sys
from signal import signal, SIGINT
from argparse import ArgumentParser, RawTextHelpFormatter

import settings
from functions.generic import *
from functions.rocketreach import *

# SIGINT handler
def interruptHandler(signal, frame):
    exiting("Interrupted by user.")

# Parse arguments
def parse_args():
    parser = ArgumentParser(description="Python utility to query RocketReach API", formatter_class=RawTextHelpFormatter)
    parser.add_argument("-c", required=False, metavar="company", help="Search people in company (i.e.: mycompany)")
    parser.add_argument("-d", required=False, metavar="domain", help="Search people in domain (i.e.: mycompany.com)")
    parser.add_argument("-l", required=False, metavar="", help="Perform lookup search (i.e.: emails)")

    parser.add_argument("-t", required=False, metavar="time", default=DEFAULT_WAIT, type=int, help="Time to wait between requests (default: %ss.)" % DEFAULT_WAIT)
    parser.add_argument("--write", required=False, metavar="<file>", help="Output results to file (csv)")
    parser.add_argument("--user", required=False, metavar="User-agent", default=USER_AGENT, help="Change default user-agent (default: %s)" % USER_AGENT)
    parser.add_argument("--proxy", required=False, metavar="proxy", default="", help="Proxy to perform HTTP requests (ie.: http://localhost:8080, socks://localhost:8080)")
    parser.add_argument("--nocheck", required=False, action="store_true", help="Do not perform API checks")
    args = parser.parse_args()

    if (not args.c):
        print("[!] %s requires a company name (-c)\nExiting..." % (sys.argv[0]))
        sys.exit(1)
    return args

# Main function
def main(args):
    # Set HTTP_REQ
    HTTP_REQ = {}
    HTTP_REQ["user-agent"] = USER_AGENT
    HTTP_REQ["proxy"] = {} if (len(args.proxy) == 0) else {"https": args.proxy, "http": args.proxy}
    HTTP_REQ["time"] = args.t

    # Display some info
    print("[*] Starting %s" % (sys.argv[0]))
    print(" - User-Agent: %s" % (HTTP_REQ["user-agent"]))
    print(" - Proxy: %s" % (HTTP_REQ["proxy"]))
    print(" - Time: %ss.\n" % (HTTP_REQ["time"]))

    # Perform some checks to ensure RocketReach's API key is ok
    if not args.nocheck:
        rocketReach_checks(HTTP_REQ)
    else:
        print("[*] Not performing API checks")

    print()
    input("Searching for people in \"%s\", press any key to continue..." % (args.c))
    rocketReach_fetch_people_from_company(HTTP_REQ, args.c)
    if (args.l): # Perform lookup
        rocketReach_lookup_people(HTTP_REQ)
    rocketReach_display_people()

# Starts here
if __name__ == "__main__":
    signal(SIGINT, interruptHandler)
    args = parse_args()
    init_datalist()
    # Main
    main(args)
