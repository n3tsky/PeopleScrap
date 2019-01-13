import sys

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

def exiting(message):
    print("[!] %s" % message)
    print("Exiting...")
    sys.exit(1)
