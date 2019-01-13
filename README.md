# PeopleScrap

PeopleScrap helps gathering information about people in a company (i.e.: mycompany) or domain (i.e.: mycompany.com).

### Features
- Developped in Python3
- Uses RocketReach API to gather information

### Installation


### Usage
```
usage: peopleScrap.py [-h] [-c company] [-d domain] [-l] [-t time]
                      [--write <file>] [--user User-agent] [--proxy proxy]
                      [--nocheck]

Python utility to query RocketReach API

optional arguments:
  -h, --help         show this help message and exit
  -c company         Search people in company (i.e.: mycompany)
  -d domain          Search people in domain (i.e.: mycompany.com)
  -l                 Perform lookup search (i.e.: emails)
  -t time            Time to wait between requests (default: 2s.)
  --write <file>     Output results to file (csv)
  --user User-agent  Change default user-agent (default: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0)
  --proxy proxy      Proxy to perform HTTP requests (ie.: http://localhost:8080, socks://localhost:8080)
  --nocheck          Do not perform API checks
```

### ToDo
- Add Hunter.io
- Add LinkedIn (API or website)
