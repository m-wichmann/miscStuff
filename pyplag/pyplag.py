#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# TODO:
# - Add User Agent, so google won't ban us.


import json
import urllib


def pyplag():
    # open file with data under test
    fd = open('sample_data_1', 'r')

    try:
        # go through all lines in file
        for line in fd:
            # tokenize line
            tokens = line.split()
            # if line is long enough check for plag
            if len(tokens) > 10:
                # search every segement of line
                for i in xrange(0,len(tokens) - 5):
                    segment = ' '.join(tokens[i:i+6])
                    print googlesearch(segment)
    # make sure file is closed if something happens
    except Exception:
        fd.close()


def googlesearch(searchfor):
    # build query
    query = urllib.urlencode({'q': searchfor})
    # build url
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
    # open url
    search_response = urllib.urlopen(url)
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
