#### Set API keys here
ROCKETREACH_API_KEY=""
HUNTERIO_API_KEY=""

#### Some constants
# Web/requests
USER_AGENT="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0"
DEFAULT_WAIT=2

### API
# RocketReach
ROCKETREACH_ACCOUNT_URL="https://api.rocketreach.co/v1/api/account"
ROCKETREACH_SEARCH_URL="https://api.rocketreach.co/v1/api/search"
ROCKETREACH_STATUS_URL="https://api.rocketreach.co/v1/api/checkStatus"
ROCKETREACH_LOOKUP_URL="https://api.rocketreach.co/v1/api/lookupProfile"
# HunterIO
HUNTERIO_ACCOUNT_URL="https://api.hunter.io/v2/account"
HUNTERIO_DOMAIN_URL="https://api.hunter.io/v2/domain-search"

# Color
GREEN="\033[0;32m"
RED="\033[0;31m"
ORANGE="\033[0;33m"
NOCOLOR="\033[0m"

# Global variables
def init_datalist():
    global PEOPLE_DATA
    PEOPLE_DATA = []
