#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import sys
import re

def getNav(fund):
    import urllib.request
#    url = 'https://www.morningstar.se/Funds/Quicktake/Overview.aspx?perfid=' + fund
    url = 'https://www.morningstar.se/se/funds/snapshot/snapshot.aspx?id=' + fund
    response = urllib.request.urlopen(url)

    name = None
    nav = None
    date = None
    for l in response:
        ul = l.decode('utf-8')
        if '<script' in ul and '<h1>' in ul:
            name = re.search('<h1>([^<]+)</h1>', ul).group(1)
        elif 'Andelskurs (NAV)' in ul:
            m = re.search('<br />([\d-]+)</span></td><td class="line"> </td><td class="line text">SEK ([\d,]+)</td>', ul)
            date = m.group(1)
            nav = m.group(2)
        if nav and date and name:
            return (name, nav, date)
    raise RuntimeError("Could not get nav " + str((name, nav, date)))

def getNavRetry(fund):
    for i in range(3):
        try:
            return getNav(fund)
        except RuntimeError as e:
            print(e)
            sys.stderr.write("Error getting " + fund + ", retrying\n")
    raise RuntimeError("Could not fetch nav, giving up")

def testOne():
    print(getNav('F0GBR04FT1'))


def putOutput(output):
    s = '\n'.join(output)
    if sys.platform == 'win32':
        import winclip
        winclip.paste(s)
        print(s)
    else:
        print(s)

with open(sys.argv[1]) as json_file:
    import json
    import concurrent.futures
    json_data = json.load(json_file)

    output = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        (funds, mynames) = zip(*json_data['navs'])
        for ((name, nav, date), myname) in zip(executor.map(getNavRetry, funds), mynames):
            output.append('\t'.join([name, nav, date]))
    putOutput(output)
