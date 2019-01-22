import requests
import json
from settings import *

# Get JSON loaded data from HTTP GET request
def http_get_json(HTTP_REQ):
    req = http_get(HTTP_REQ)
    if req != None:
        http_code = req.status_code
        try: # Try and parse JSON data
            json_data = json.loads(req.content)
            return http_code, json_data
        except ValueError as e:
            return http_code, e
    return None, None

# Perform HTTP query
def http_get(HTTP_REQ):
    # Define headers
    headers = {
        "User-Agent": "%s" % (HTTP_REQ["user-agent"]),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept_language": "en-US,en;q=0.5",
        "Accept_encoding": "gzip, deflate, br"
    }

    try:
        return requests.get(HTTP_REQ["url"], headers=headers, proxies=HTTP_REQ["proxy"], timeout=5)
    except requests.exceptions.ConnectionError as e:
        print("[!] No connection to the Internet")
    except requests.exceptions.HTTPError as e:
        print("[!] Exception while performing HTTP request to %s" % (HTTP_REQ["url"]))
    except requests.exceptions.ReadTimeout as e:
        print("[!] Timeout while performing HTTP request to %s" % (HTTP_REQ["url"]))

    return None
