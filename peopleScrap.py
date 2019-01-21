#!/usr/bin/env python3
import sys
from signal import signal, SIGINT
from argparse import ArgumentParser, RawTextHelpFormatter

import settings
from functions.generic import *
from functions.rocketreach import *
from functions.hunterio import *

# SIGINT handler
def interruptHandler(signal, frame):
    display_people()
    exiting("Interrupted by user.")

# Parse arguments
def parse_args():
    parser = ArgumentParser(description="Python utility to query RocketReach API", formatter_class=RawTextHelpFormatter)
    parser.add_argument("-c", required=False, metavar="company", help="Search people in company (i.e.: mycompany)")
    parser.add_argument("-d", required=False, metavar="domain", help="Search people in domain (i.e.: mycompany.com)")
    parser.add_argument("-l", required=False, action="store_true", help="Perform lookup search (i.e.: emails)")

    parser.add_argument("-t", required=False, metavar="time", default=DEFAULT_WAIT, type=int, help="Time to wait between requests (default: %ss.)" % DEFAULT_WAIT)
    parser.add_argument("--write", required=False, metavar="<file>", help="Output results to file (csv); beware as it will overwrite any data in file")
    parser.add_argument("--user", required=False, metavar="User-agent", default=USER_AGENT, help="Change default user-agent (default: %s)" % USER_AGENT)
    parser.add_argument("--proxy", required=False, metavar="proxy", default="", help="Proxy to perform HTTP requests (ie.: http://localhost:8080, socks5://localhost:8080)")
    parser.add_argument("--nocheck", required=False, action="store_true", help="Do not perform API checks")
    args = parser.parse_args()

    if not (args.c or args.d):
        print("[!] %s requires a company name (-c) or company domain (-d)\nExiting..." % (sys.argv[0]))
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
    print("[*] Options")
    if (args.write):
        print(" - Output file: \"%s\"" % (args.write))
    print(" - User-Agent: %s" % (HTTP_REQ["user-agent"]))
    print(" - Proxy: %s" % (HTTP_REQ["proxy"]))
    print(" - Time: %ss.\n" % (HTTP_REQ["time"]))

    # Perform some checks to ensure RocketReach's API key is ok
    if not args.nocheck:
        rocketReach_checks(HTTP_REQ)
        hunterIO_checks(HTTP_REQ)
    else:
        print("[*] Not performing API checks")

    input("""\nSearching for people in company: \"%s\" and/or domain: \"%s\"\npress any key to continue...\n""" %
        ("" if args.c == None else args.c, "" if args.d == None else args.d))

    # RocketReach
    if (args.c): # If a company name was provided
        rocketReach_fetch_people_from_company(HTTP_REQ, args.c)

    # HunterIO
    possible_mail_pattern = ""
    if (args.d): # If a company domain was provided
        possible_mail_pattern = hunterIO_fetch_domain_info(HTTP_REQ, args.d)

    if (args.c and args.l): # Perform lookup
        rocketReach_lookup_people(HTTP_REQ)

    # Ask user for pattern validation
    if ask_for_mail_pattern():
        find_mail_pattern(possible_mail_pattern, args.d)

    print("\n[*] Total people found: %d" % (len(settings.PEOPLE_DATA)))
    input("\npress any key to continue...\n")
    
    # Display to user
    print("\n[*] Now displaying info to user: \n")
    display_people()

    # Write output to file
    if (args.write):
        write_people(args.write)

# Starts here
if __name__ == "__main__":
    print(" _____                 _       _____                      ")
    print("|  __ \               | |     / ____|                     ")
    print("| |__) |__  ___  _ __ | | ___| (___   ___ _ __ __ _ _ __  ")
    print("|  ___/ _ \/ _ \| '_ \| |/ _ \\___ \  / __| '__/ _` | '_ \ ")
    print("| |  |  __/ (_) | |_) | |  __/____) | (__| | | (_| | |_) |")
    print("|_|   \___|\___/| .__/|_|\___|_____/ \___|_|  \__,_| .__/ ")
    print("                | |                                | |    ")
    print("                |_|                                |_|    ")
    print()
    signal(SIGINT, interruptHandler)
    args = parse_args()
    init_datalist()
    # Main
    main(args)
