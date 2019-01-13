# coding=utf-8
from tabulate import tabulate

import settings
from functions.http import *
from functions.generic import *

class People:
    def __init__(self):
        self.fullname = ""
        self.job = ""
        self.employer = ""
        self.city = ""
        self.country_code = ""
        self.rocket_id = ""
        self.rocket_status = ""

    def prep4display(self):
        content = ""
        if self.job != None:
            content += "Job: %s\n" % (self.job.replace("\n",""))
        if self.employer != None:
            content += "Employer: %s\n" % (self.employer.replace("\n",""))
        if self.city != None:
            content += "City: %s\n" % (self.city.replace("\n",""))
        if self.country_code != None:
            content += "Country code: %s\n" % (self.country_code.replace("\n",""))
        if self.rocket_id != None:
            content += "RocketReach ID: %s" % (self.rocket_id)
        return [self.fullname, content]

    def __str__(self):
        return(self.fullname)

### API calls
def rocketReach_call_account(HTTP_REQ):
    HTTP_REQ["url"] = "%s?api_key=%s" % (ROCKETREACH_ACCOUNT_URL, ROCKETREACH_API_KEY)
    http_code, response = http_get_json(HTTP_REQ)
    return response

def rocketReach_call_search(HTTP_REQ, company, page_start=1,page_size=100):
    HTTP_REQ["url"] = "%s?api_key=%s&company=%s&page_size=%d&start=%d" % (ROCKETREACH_SEARCH_URL, ROCKETREACH_API_KEY, company, page_size, page_start)
    http_code, response = http_get_json(HTTP_REQ)
    pagination = dict_check_and_get(response, "pagination")
    return pagination, response

def rockeyReach_call_lookup(HTTP_REQ, id):
    HTTP_REQ["url"] = "%s?api_key=%s&id=%s" % (ROCKETREACH_LOOKUP_URL, ROCKETREACH_API_KEY, id)
    http_code, response = http_get_json(HTTP_REQ)
    detail = dict_check_and_get(response, "detail")
    if detail != None:
        print("[!] %s" % detail)
    else:
        # Get information
        pass

# Parsing
def rocketreach_parse_people(json_data):
    profiles = dict_check_and_get(json_data, "profiles")
    for profile in profiles:
        p = People()
        p.fullname = dict_check_and_get(profile, "name")
        p.job = dict_check_and_get(profile, "current_title")
        p.employer = dict_check_and_get(profile, "current_employer")
        p.city = dict_check_and_get(profile, "city")
        p.country_code = dict_check_and_get(profile, "country_code")
        p.rocket_id = dict_check_and_get(profile, "id")
        p.rocket_status = dict_check_and_get(profile, "status")
        settings.PEOPLE_DATA.append(p)

def rocketReach_fetch_people_from_company(HTTP_REQ, company):
    # Get data
    pagination, data  = rocketReach_call_search(HTTP_REQ, company)
    display_value_from_dict(pagination, "total", "[*] Total people: ")
    # Parse data (if only one page)
    rocketreach_parse_people(data)
    # Iterate over page(s), if necessary
    current_page = dict_check_and_get(pagination, "thisPage")
    next_page = dict_check_and_get(pagination, "nextPage")
    while current_page != next_page:
        print("[*] People: %d - %d" % (current_page, next_page))
        pagination, data = rocketReach_call_search(HTTP_REQ, company, next_page)
        rocketreach_parse_people(data)
        # Get pagination
        current_page = dict_check_and_get(pagination, "thisPage")
        next_page = dict_check_and_get(pagination, "nextPage")
        break

# Display info about account related to API key
def rocketReach_display_account_info(data_info):
    print("[*] RocketReach account info:")
    display_value_from_dict(data_info, "email", " - Email: ")
    display_value_from_dict(data_info, "lookup_credit_balance", " - Lookup credit: ")

# Checks
def rocketReach_check_account(HTTP_REQ):
    result = rocketReach_call_account(HTTP_REQ)
    if result != None:
        detail = dict_check_and_get(result, "detail")
        if detail != None: # Not good
            print("[!] %s " % detail)
        else:
            rocketReach_display_account_info(result)
            return 1
    return 0

# Display info gathered to user
def rocketReach_display_people():
    display_list = []
    for p in settings.PEOPLE_DATA:
        display_list.append(p.prep4display())
    print(tabulate(display_list, ["Full name", "RocketReach"], "grid"))

# Check if an API key has been set by user
def rocketReach_check_basic():
    if ROCKETREACH_API_KEY != "":
        return 1
    else:
        return 0

# Perform checks
def rocketReach_checks(HTTP_REQ):
    print("[*] RocketReach: Checking API key\n")
    if not (rocketReach_check_basic() and rocketReach_check_account(HTTP_REQ)):
        exiting("Error while checking RocketReach API key")
