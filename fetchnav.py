#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import sys

def getNav(fund):
    import urllib.request
    url = 'https://www.morningstar.se/Funds/Quicktake/Overview.aspx?perfid=' + fund
    print('Requesting ' + url)
    response = urllib.request.urlopen(url)

    for l in response:
        ul = l.decode('utf-8')
        if '<h2>' in ul:
            name = ul.split('>')[1].split('<')[0]
        elif 'Senaste NAV' in ul:
            s = [x.split('<')[0].strip() for x in ul.split('>')]
            nav = s[3]
            nav = ''.join([x for x in nav if x in '0123456789,'])
            date = s[5]
    print('Done ' + url)
    return (name, nav, date)

with open(sys.argv[1]) as json_file:
    import json
    json_data = json.load(json_file)
    for i in [getNav(x) + (y,) for (x, y) in json_data['navs']]:
        (fullname, nav, date, myname) = i
        print(';'.join([myname, nav, date]))
