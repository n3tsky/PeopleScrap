# PeopleScrap

PeopleScrap helps gathering information about people in a company (i.e.: mycompany) or domain (i.e.: mycompany.com).

### Features
- Find emails, first name, last name, job position, city/location, phone numbers, etc.
- Uses RocketReach & Hunter.io APIs to gather information
- Generate emails according to user's choice
- Output result to CSV file
- Developped in Python3
- Handle user interruption (in case of network issues) and display current results anyway

### Installation
* Install Python3 dependencies
```
pip3 install --user -r requirements.txt
```
* Set up your API keys in "settings.py"
* Run
```
./peopleScrap.py
```

### Usage
```
 _____                 _       _____                      
|  __ \               | |     / ____|                     
| |__) |__  ___  _ __ | | ___| (___   ___ _ __ __ _ _ __  
|  ___/ _ \/ _ \| '_ \| |/ _ \___ \  / __| '__/ _` | '_ \ 
| |  |  __/ (_) | |_) | |  __/____) | (__| | | (_| | |_) |
|_|   \___|\___/| .__/|_|\___|_____/ \___|_|  \__,_| .__/ 
                | |                                | |    
                |_|                                |_|    

usage: peopleScrap.py [-h] [-c company] [-d domain] [-l] [-o <file>]
                      [--wait <time>] [--timeout <time>] [--user <user-agent>]
                      [--proxy <proxy>] [--nocheck]

Python utility to query RocketReach API

optional arguments:
  -h, --help           show this help message and exit
  -c company           Search people in company (i.e.: mycompany)
  -d domain            Search people in domain (i.e.: mycompany.com)
  -l                   Perform lookup search (i.e.: emails)
  -o <file>            Output results to file (csv), beware as it will overwrite any data in file
  --wait <time>        Time to wait between requests (default: 2s.)
  --timeout <time>     Timeout for HTTP requests (default: 3s.)
  --user <user-agent>  Change default user-agent (default: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0)
  --proxy <proxy>      Proxy to perform HTTP requests (ie.: http://localhost:8080, socks5://localhost:8080)
  --nocheck            Do not perform API checks
```

### ToDo
- Finish lookup (RocketReach)
- Try to sort|uniq results
- Add LinkedIn (API or website)
