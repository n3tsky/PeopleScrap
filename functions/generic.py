import sys
import settings
from tabulate import tabulate

MAX_CHARS=75
MAIL_PATTERNS = [(1, "{first}.{last}"), (2, "{f}.{last}"), (3, "{first}{last}"), (4, "{f}{last}"), (5, "{first}")]

# Check if value is in given dictionary or return None
def dict_check_and_get(d, value):
    return d[value] if value in d else None

def display_value_from_dict(d, value, pre="", post=""):
    result = dict_check_and_get(d, value)
    if result != None:
        print("%s%s%s" % (pre, result, post))

# Parse JSON result
def parse_json(data, needed):
    g = list()
    for d in data:
        l = list()
        for n in needed:
            l.append(check_and_get(d, n))
        g.append(l)
    return g

def split_long_string(string, max_len):
    if (string != None) and (len(string) > max_len):
        return "\n".join([string[i:i+max_len] for i in range(0, len(string), max_len)])
    else:
        return string

def properly_add_to_list(m_list, value):
    if value != None:
        if value not in m_list:
            m_list.append(value)

def ask_for_mail_pattern():
    print("\n[*] Mail pattern")
    while True:
        response = input("   Do you want to generate mail pattern (y/n)? ")
        if response.lower() == "y":
            return 1
        elif response.lower() == "n":
            return 0
        else:
            continue

def find_mail_pattern(possible_value):
    print("\n[*] Mail pattern:")
    if possible_value != None or possible_value != "":
        print(" - HunterIO find the following mail pattern: \"%s\"" % (possible_value))
    print(" - We propose the following mail pattern for generation:")
    for mi, mp in MAIL_PATTERNS: print("  - %d/ %s" % (mi, mp))
    # Wait for user confirmation
    while True:
        pattern_result = input("\nWich pattern do you want to choose? ")
        if pattern_result.isdigit():
            if int(pattern_result) > 0 and (int(pattern_result) <= len(MAIL_PATTERNS)):
                break

    # Let's generate
    generating_mail_with_pattern(MAIL_PATTERNS[int(pattern_result)][1])

def generating_mail_with_pattern(pattern):
    print(" - Generating e-mails with the following pattern: \"%s\"" % (pattern))

# Display info gathered to user
def display_people():
    display_list = []
    for p in settings.PEOPLE_DATA:
        display_list.append(p.prep4display())
    print(tabulate(display_list, ["Full name", "RocketReach"], "grid"))
    print("\n[*] Total people found: %d" % (len(settings.PEOPLE_DATA)))

# Exiting program with custom message
def exiting(message):
    print("[!] %s" % message)
    print("Exiting...")
    sys.exit(1)

### Class
class People:
    def __init__(self):
        self.fullname = ""
        self.firstname = ""
        self.lastname = ""
        self.job = ""
        self.employer = ""
        self.emails = []
        self.phones = []
        self.twitter = ""
        self.city = ""
        self.country_code = ""
        self.rocket_id = ""
        self.rocket_status = ""

    # Parse info from RocketReach API
    def parse_from_rocketReach(self, fullname, job, employer, city, country_code, r_id, r_status):
        if fullname != None:
            self.fullname = fullname
            self.split_lastname()
        if job != None:
            self.job = job
        if employer != None:
            self.employer = employer
        if city != None:
            self.city = city
        if country_code != None:
            self.country_code = country_code
        if r_id != None:
            self.rocket_id = int(r_id)
        if r_status != None:
            self.rocket_status = r_status

    def parse_from_hunterIO(self, first_name, last_name, email, phone_number, twitter):
        if first_name != None:
            self.firstname = first_name
        if last_name != None:
            self.lastname = last_name
        self.fullname = "%s %s" % (self.firstname, self.lastname)
        if email != None:
            properly_add_to_list(self.emails, email)
        if phone_number != None:
            properly_add_to_list(self.phones, phone_number)
        if twitter != None:
            self.twitter = twitter

    # Try to determine first and last names
    def split_lastname(self):
        if(len(self.fullname.split(" ")) == 2): # Don't handle more than split(" ") == 2
            first = self.fullname.split(" ")[0] #
            second = self.fullname.split(" ")[1]
            if (first.isupper()) and not (second.isupper()): # If LASTNAME and firstname
                self.firstname = second
                self.lastname = first
            else:
                self.firstname = first
                self.lastname = second

    # Prep. in order to display info to user
    def prep4display(self):
        content = ""
        if self.job != None:
            t_job = self.job.replace("\n","")
            content += "Job: %s\n" % (split_long_string(self.job, MAX_CHARS))
        if self.employer != None:
            content += "Employer: %s\n" % (self.employer.replace("\n",""))
        if self.city != None:
            content += "Country code: %s\n" % (self.country_code.replace("\n",""))
        if self.rocket_id != None:
            content += "RocketReach ID: %s\n" % (self.rocket_id)
        if self.emails != None:
            content += "Emails: %s" % (", ".join(self.emails))

        info_name = "%s\n\nFirst name: %s\nLast name: %s" % (self.fullname, self.firstname, self.lastname)
        return [info_name, content]

    # __str__
    def __str__(self):
        return(self.fullname)
