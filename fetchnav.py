#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import sys

def getNav(fund):
    import urllib.request
    url = 'https://www.morningstar.se/Funds/Quicktake/Overview.aspx?perfid=' + fund
    response = urllib.request.urlopen(url)

    name = None
    nav = None
    date = None
    for l in response:
        ul = l.decode('utf-8')
        if '<h2>' in ul:
            name = ul.split('>')[1].split('<')[0]
        elif 'Senaste NAV' in ul:
            s = [x.split('<')[0].strip() for x in ul.split('>')]
            nav = ''.join([x for x in s[3] if x in '0123456789,'])
            date = s[5]
        if nav and date and name:
            return (name, nav, date)
    raise RuntimeError("Could not get nav")

def getNavRetry(fund):
    for i in range(3):
        try:
            return getNav(fund)
        except RuntimeError:
            sys.stderr.write("Error getting " + fund + ", retrying\n")
    raise RuntimeError("Could not fetch nav, giving up")

def testOne():
    print(getNav("0P000148YN"))

with open(sys.argv[1]) as json_file:
    import json
    import concurrent.futures
    json_data = json.load(json_file)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        (funds, mynames) = zip(*json_data['navs'])
        for ((_, nav, date), myname) in zip(executor.map(getNavRetry, funds), mynames):
            print('\t'.join([myname, nav, date]))
