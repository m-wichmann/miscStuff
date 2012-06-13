#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# TODO:
# - Add User Agent, so google won't ban us.


import json
import urllib
import urllib2


def pyplag():

    # open file with data under test
    fd = open('sample_data_1', 'r')

#    try:
        # go through all lines in file
    for line in fd:
        # tokenize line
        tokens = line.split()
        # if line is long enough check for plag
        if len(tokens) > 10:
            # search every segement of line
            for i in xrange(0,len(tokens) - 5):
                segment = ' '.join(tokens[i:i+6])
                print "[" + str(altgooglesearch(segment)).rjust(15) + "] " + segment


    # make sure file is closed if something happens
#    except Exception:
#        fd.close()
    fd.close()



def altgooglesearch(searchfor):
    url = 'https://www.google.com/search?q=%22' + str(searchfor).replace(" ", "+") + "%22"

    # set user agent, so we won't get banned...
    headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0' }
    request = urllib2.Request(url, None, headers)

    # open url
    search_response = urllib2.urlopen(request)
    search_results = search_response.read()

    temp1 = search_results.find("<div id=resultStats>")
    temp2 = search_results.find("Ergebnisse<nobr>")

    if temp1 != -1 and temp2 != -1:
        # TODO: this only works with german google...
        if search_results.find("Ungefähr") != -1:
            numstring = search_results[temp1 + 30:temp2 - 1]
        else:
            numstring = search_results[temp1 + 20:temp2 - 1]
        return int(numstring.replace(".",""))
    else:
        return 0


def googlesearch(searchfor):
#    query = urllib.urlencode({'q': searchfor})
    # build url
#    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
#    print url

    # build url
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + str(searchfor).replace(" ", "+")

    # set user agent, so we won't get banned...
    headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0' }
    request = urllib2.Request(url, None, headers)

    # open url
    search_response = urllib2.urlopen(request)
    # get result
    search_results = search_response.read()
    # decode json resultss
    results = json.loads(search_results)
    # get response data from json
    data = results['responseData']

    # return attribute of interest
    # TODO: this seems to be a problem. Maybe because of unsolved captcha.
    if data:
        return data['cursor']['estimatedResultCount']
    else:
        return 0


if __name__ == '__main__':
    pyplag()
