#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""check via google if file is a plagiarism"""

# TODO:
# - introduce a more or less objective "rating" value replacing the current "count" value, so the eval function has some boundaries
# - define a clear data structure for the rating format (e.g. dict with word and rating)
# - make the whole file thing a little more safe using exception handling
# - make sure all words are outputted to html and not only the middle of a chunk...
# - Should we really rely on google so much?!


import json
import re
import urllib
import urllib2


THRESH_ABOVE0 = 0
THRESH_ABOVE2 = 10
THRESH_ABOVE5 = 100
THRESH_ABOVE10 = 1000



def pyplag():
    """main function"""
    data = checkforplag_newalgo('data/sample_data_1')
    outputtohtml('out/out.html', data)




def checkforplag(path):
    """check file at path if it is a plag"""
    # open file with data under test
    fd = open(path, 'r')

    data = []

    # go through all lines in file
    for line in fd:
        # check if line starts with # to check for comments
        # this is used to quickly alter the testdata
        if line[0] == '#':
            print "comment"
            continue

        # tokenize line
        tokens = line.split()
        # if line is long enough check for plag
        if len(tokens) > 10:
            # search every segement of line
            for i in xrange(0,len(tokens) - 5):
                segment = ' '.join(tokens[i:i+6])
#                print "[" + str(altgooglesearch(segment)).rjust(15) + "] " + segment
                data.append({"word": tokens[i],"count": altgooglesearch(segment)})
    fd.close()
    return data





def checkforplag_newalgo(path):

    data = []

    fd = open(path, 'r')

    # plan:
    # - split text into paragraph
    # - split paragraphs into sentences
    # - check sentences for significant parts
    # - pack everything into a nice data package with rating values for every word

    # TODO: Assumption: every line is a paragraph
    # This is not true if copy-pasted from a pdf file?!
    for line in fd:

        # filter short lines like newlines and titles
        if len(line) < 5 or line[0] == '#':
            continue

        print line

        # split line into sentences if it ends with .!?
        # TODO: a sentece should only start with a capital letter! Otherwise abbreviations like e.g. are also recognized
        sentences = re.split(r'\s*[!?.]\s*', line)
        
        for sentence in sentences:
            count = altgooglesearch(sentence.replace("\n",""))
            data.append({"word": sentence,"count": count})




    fd.close()
    return data






def outputtohtml(path, data):
    """output data to html"""
    fd = open(path, 'w')

    fd.write('<html>')
    fd.write('<head>')
    fd.write('<title>sample_data_1</title>')
    fd.write('<meta name="generator" content="pyplag">')
    fd.write('<meta http-equiv="content-type" content="text/html; charset=UTF-8">')
    fd.write('<meta http-equiv="content-style-type" content="text/css">')
    fd.write('<link href="./screen.css" rel="stylesheet" type="text/css" media="screen">')
    fd.write('</head>')
    fd.write('<body>')

    # TODO: don't do the color thing on a word basis, but on a substring basis
    for entry in data:
        if entry["count"] > THRESH_ABOVE10:
            spanclass = "10"
            fd.write('<span class="above' + spanclass + '">' + entry["word"] + '</span> ')
        elif entry["count"] > THRESH_ABOVE5 and entry["count"] <= THRESH_ABOVE10:
            spanclass = "5"
            fd.write('<span class="above' + spanclass + '">' + entry["word"] + '</span> ')
        elif entry["count"] > THRESH_ABOVE2 and entry["count"] <= THRESH_ABOVE5:
            spanclass = "2"
            fd.write('<span class="above' + spanclass + '">' + entry["word"] + '</span> ')
        elif entry["count"] > THRESH_ABOVE0 and entry["count"] <= THRESH_ABOVE2:
            spanclass = "0"
            fd.write('<span class="above' + spanclass + '">' + entry["word"] + '</span> ')
        elif entry["count"] == 0:
            fd.write(entry["word"] + ' ')
        else:
            fd.write(entry["word"] + ' ')



#        if entry["count"] > 100000:
#            color = "00"
#        if entry["count"] > 10000:
#            color = "30"
#        if entry["count"] > 1000:
#            color = "70"
#        if entry["count"] > 100:
#            color = "A0"
#        if entry["count"] > 10:
#            color = "D0"
#        if entry["count"] == 0:
#            color = "00"
#        else:
#            color = "FF"
#        fd.write('<font color="#' + color + '0000">' + entry["word"] + '</font> ')


    fd.write("</body>")
    fd.write("</html>")




def altgooglesearch(searchfor):
    """use http google site to search"""
#    url = 'http://www.google.com/search?q=%22' + str(searchfor).replace(" ", "+") + "%22"
    url = 'http://www.google.com/search?q=%22' + urllib.quote(str(searchfor)) + '%22'

    # set user agent, so we won't get banned...
    headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0' }
    request = urllib2.Request(url, None, headers)


    # DEBUG
#    print "for: " + str(searchfor)
#    print "url: " + str(url)
#    print "headers: " + str(headers)
#    print "request: " + str(request.__dict__)


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
    """search using old (deprecated) google api. will ban after about 10 queries or so"""
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
