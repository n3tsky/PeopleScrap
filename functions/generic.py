import sys
import settings
from tabulate import tabulate
from unidecode import unidecode

MAX_CHARS=80
MAIL_PATTERNS = [(1, "{first}.{last}"), (2, "{f}.{last}"), (3, "{first}{last}"), (4, "{first}-{last}"), (5, "{f}{last}"), (6, "{first}")]

# Check if value is in given dictionary or return None
def dict_check_and_get(d, value):
    return d[value] if value in d else None

def display_value_from_dict(d, value, pre="", post=""):
    result = dict_check_and_get(d, value)
    if result != None:
        print("%s%s%s" % (pre, result, post))

def write_to_file(output_file, mode, data):
    with open(output_file, mode) as fout:
        fout.write("%s\n" % (data))

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

# Ask user whether to generate mail pattern or not
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

# Try to figure out the mail pattern (HunterIO + user input)
def find_mail_pattern(possible_value, possible_domain = ""):
    if possible_value != None and possible_value != "":
        print(" - HunterIO find the following mail pattern: \"%s\"" % (possible_value))
    print(" - We propose the following mail pattern for generation:")
    for mi, mp in MAIL_PATTERNS: print("  - %d/ %s" % (mi, mp))
    # Wait for user confirmation
    while True:
        pattern_result = input("\nWich pattern do you want to choose? ")
        if pattern_result.isdigit():
            if int(pattern_result) > 0 and (int(pattern_result) <= len(MAIL_PATTERNS)):
                break

    if (possible_domain == None or possible_domain == ""):
        possible_domain = input("\nPlease provide a domain (@company.com): ")

    # Let's generate
    generate_mail_with_pattern(MAIL_PATTERNS[int(pattern_result)-1][1], possible_domain)

# Iterate over PEOPLE_DATA to generate email address according to pattern
# and add to "gen_email"
# return: nothing
def generate_mail_with_pattern(pattern, possible_domain):
    print(" - Generating e-mails with the following pattern: \"%s\"" % (pattern))
    for p in settings.PEOPLE_DATA:
        if (p.firstname != "") and (p.lastname != ""):
            email = build_mail(p.firstname, p.lastname, pattern)
            p.gen_email = "%s@%s" % (email, possible_domain)
    print(" - Done generating e-mails!")

# Build email address according to a specific (user selected) pattern
# return: email address
def build_mail(firstname, lastname, pattern):
    email = pattern
    # Correct accents
    u_firstname = unidecode(firstname).lower()
    u_lastname = unidecode(lastname).lower()
    # Replacement
    email = email.replace("{first}", u_firstname)
    email = email.replace("{last}", u_lastname)
    email = email.replace("{f}", u_lastname)
    return email

# Display info gathered to user
def display_people():
    display_list = []
    for p in settings.PEOPLE_DATA:
        display_list.append(p.prep4display())
    print(tabulate(display_list, ["Full name", "RocketReach"], "grid"))

# Write output to file
def write_people(output_file):
    print("\n[!] Writing data to file")
    HEADERS = "fullname;first name;last name;valid emails;generated email;phones;city;country;job;employer;twitter;rocket ID;"
    # Write headers
    write_to_file(output_file, "w", HEADERS)
    for p in settings.PEOPLE_DATA:
        write_to_file(output_file, "a", p.prep4write())
    print("[!] Done writing!")

# Clean data before writing to file
def clean_data(data):
    if data != None:
        if type(data) == list:
            data = ",".join(data)
        if type(data) == str:
            data = data.replace("\n","")
        return data
    else:
        return ""

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
        self.gen_email = ""
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

    # Parse info from HunterIO API
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
        if self.job != None and self.job != "":
            t_job = self.job.replace("\n","")
            content += "Job: %s\n" % (split_long_string(self.job, MAX_CHARS))
        if self.employer != None and self.employer != "":
            content += "Employer: %s\n" % (self.employer.replace("\n",""))
        if self.country_code != None and self.country_code != "":
            content += "Country code: %s\n" % (self.country_code.replace("\n",""))
        if self.city != None and self.city != "":
            content += "City: %s\n" % (self.city.replace("\n",""))
        if self.rocket_id != None and self.rocket_id != "":
            content += "RocketReach ID: %s\n" % (self.rocket_id)
        if self.emails != None and len(self.emails) > 0:
            content += "Valid emails: %s\n" % (", ".join(self.emails))
        if self.gen_email != None and self.gen_email != "":
            content += "Generated email: %s\n" % (self.gen_email)
        if self.phones != None and len(self.phones) > 0:
            content += "Phone number(s): %s\n" % (", ".join(self.phones))
        if self.twitter != None and self.twitter != "":
            content += "Twitter account: %s" % (self.twitter)

        info_name = "%s\n\nFirst name: %s\nLast name: %s" % (self.fullname, self.firstname, self.lastname)
        return [info_name, content]

    # Prep. in order to write data to file
    def prep4write(self):
        content = ""
        for elt in [self.fullname, self.firstname, self.lastname, self.emails, self.gen_email, self.phones, self.city, self.country_code,
            self.job, self.employer, self.twitter, self.rocket_id]:
            content += "%s;" % clean_data(elt)
        return content

    # __str__
    def __str__(self):
        return(self.fullname)
