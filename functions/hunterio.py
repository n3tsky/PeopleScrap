# coding=utf-8
from tabulate import tabulate
from time import sleep

import settings
from functions.http import *
from functions.generic import *

OFFSET_VALUE=100
INSUFFICIENT_CREDS=0
MAX_INSUFFICIENT_CREDS=3

### API calls
def hunterIO_call_account(HTTP_REQ):
    HTTP_REQ["url"] = "%s?api_key=%s" % (HUNTERIO_ACCOUNT_URL, HUNTERIO_API_KEY)
    http_code, response = http_get_json(HTTP_REQ)
    return response

def hunterIO_call_domain_search(HTTP_REQ, domain, offset=0, limit=100):
    HTTP_REQ["url"] = "%s?api_key=%s&domain=%s&offset=%d&limit=%d" % (HUNTERIO_DOMAIN_URL, HUNTERIO_API_KEY, domain, offset, limit)
    http_code, response = http_get_json(HTTP_REQ)
    hunterIO_check_limit(response)
    return response
### /API calls

# Parsing
def hunterIO_parse_info(data):
    # Get emails
    emails = dict_check_and_get(data, "emails")
    if emails != None:
        for e in emails:
            # Maybe try to clear doublon, based on emails and/or name?
            p = People()
            p.parse_from_hunterIO(dict_check_and_get(e, "first_name"), dict_check_and_get(e, "last_name"),
                dict_check_and_get(e, "value"), dict_check_and_get(e, "phone_number"), dict_check_and_get(e, "twitter"))
            settings.PEOPLE_DATA.append(p)

def hunterIO_fetch_domain_info(HTTP_REQ, domain):
    # Get data
    print("\n[*] HunterIO - Starting...")
    current_offset = OFFSET_VALUE
    json_data = hunterIO_call_domain_search(HTTP_REQ, domain) # Default offset = 0
    ret_pattern = ""

    # Get data
    data = dict_check_and_get(json_data, "data")
    if data != None:
        print("[*] HunterIO - Info")
        display_value_from_dict(data, "webmail", " - Webmail: ")
        display_value_from_dict(data, "pattern", " - Mail pattern: ")
        ret_pattern = dict_check_and_get(data, "pattern")
        display_value_from_dict(data, "organization", " - Organization: ")
        # Parse info
        hunterIO_parse_info(data)

    # Get meta
    meta = dict_check_and_get(json_data, "meta")
    if meta != None:
        total_people = dict_check_and_get(meta, "results")
        display_value_from_dict(meta, "results", " - results: ")
        display_value_from_dict(meta, "limit", " - limit: ")
        # Loop and fetch people
        while total_people > current_offset:
            print("[*] HunterIO - People: %d - %d" % (current_offset, total_people))
            # Query (offset)
            json_data = hunterIO_call_domain_search(HTTP_REQ, domain, offset=current_offset)
            # Parse info
            data = dict_check_and_get(json_data, "data")
            if data != None:
                hunterIO_parse_info(data)

            if (INSUFFICIENT_CREDS > MAX_INSUFFICIENT_CREDS):
                print("[!] Insufficient lookup credits, aborting lookup search...")
                break
            current_offset += OFFSET_VALUE
            break
    return ret_pattern

# Display info about account related to API key
def hunterIO_display_account_info(data_info):
    print("*** HunterIO account info ***")
    display_value_from_dict(data_info, "email", " - Email: ")
    display_value_from_dict(data_info, "plan_name", " - Account type: ")
    display_value_from_dict(data_info, "reset_date", " - Reset date: ")
    display_value_from_dict(data_info, "calls", " - Calls: ")

def hunterIO_check_limit(json_data):
    global INSUFFICIENT_CREDS
    #{'errors': [{'id': 'too_many_requests', 'code': 429, 'details': "You've exceeded your monthly limit. Please upgrade your account."}]}
    errors = dict_check_and_get(json_data, "errors")
    if errors != None:
        errors = errors[0]
        details = dict_check_and_get(errors, "details")
        if "You've exceeded your monthly limit" in details:
            print("[!] HunterIO | %s" % details)
            INSUFFICIENT_CREDS+=1

# Check accounts (calls /account)
def hunterIO_check_account(HTTP_REQ):
    result = hunterIO_call_account(HTTP_REQ)
    if result != None:
        errors = dict_check_and_get(result, "errors")
        if errors != None: # Not good
            details =  dict_check_and_get(errors[0], "details")
            print("[!] HunterIO | Error: %s " % details)
        else:
            data = dict_check_and_get(result, "data")
            hunterIO_display_account_info(data)
            return 1
    return 0

# Check if an API key has been set by user
def hunterIO_check_basic():
    if HUNTERIO_API_KEY != "":
        return 1
    else:
        return 0

# Perform checks
def hunterIO_checks(HTTP_REQ):
    print("\n[*] HunterIO: Checking API key\n")
    if not (hunterIO_check_basic() and hunterIO_check_account(HTTP_REQ)):
        print("[!] HunterIO | Error while checking HunterIO API key (please provide a valid API key)")
