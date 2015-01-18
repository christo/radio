#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2010-2012 BjÃ¶rn EdstrÃ¶m <be@bjrn.se>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""" program for generating soma.fm playlists.

This program will create a playlist with one each of soma.fm:s
streams, for quick zapping between channels.
"""

import BeautifulSoup
import optparse
import re
import socket
import sys
import urllib2


SOMAFM_URL = 'http://somafm.com/'


def download(url):
    '''Download url

       Will throw urllib2 exceptions on errors.
    '''

    return urllib2.urlopen(url).read()


def parse_soma_fm(html):
    '''Take the front page html from soma.fm and parse out all the
       channels.

       A bit shaky, will probably need continous updates as soma.fm
       updates their web page.

       Yields tuples of (channel title, description, playlist link).
    '''

    soup  = BeautifulSoup.BeautifulSoup(html)

    def strip_comments(p):
        return filter(lambda q: not isinstance(q, BeautifulSoup.Comment), p)

    def strip_empty(p):
        return filter(lambda q: q.string.strip() != '', p)

    for channel in soup.findAll('li'):
        tmp = channel.find('h3').contents[0]
        tmp = tmp.strip()
        title = tmp
        tmp = channel.findAll('a')[0]
        href = dict(tmp.attrs)[u'href']
        url = SOMAFM_URL + href.strip('/')
        description = dict(tmp.findAll('img')[0].attrs)[u'alt']
        yield (title, description, url + '.pls')


def parse_pls(txt):
    '''Stupid parsing of pls-style playlists. Will ignore most
       information, except the paths.

       No validation of any kind takes place.

       Yields the paths in the playlist.
    '''

    entries = {}
    for row in txt.splitlines():
        if row.startswith('File'):
            file_n, path = row.split('=')
            yield path


def descr():
    '''Returns a program description.
    '''

    return __doc__.split('\n\n', 1)[1].strip()


def main():
    parser = optparse.OptionParser(usage='%prog [options]\n\n' + descr())
    parser.add_option('-o', action='store', dest='output',
                      metavar='PATH', default='-',
                      help='write output to PATH instead of stdout')
    parser.add_option('--recurse', action='store_true', default=False,
                      help='download playlists and write direct ' \
                           'stream url to output')
    #parser.add_option('--verify', action='store_true', default=False,
    #                  help='verify that stream url work')
    options, args = parser.parse_args()

    html = download(SOMAFM_URL)

    # Construct output playlist
    doc = []
    doc += ['[playlist]']
    doc += [None]
    i = 1
    for title, description, link in parse_soma_fm(html):
        path = link
        if options.recurse:
            for direct_link in parse_pls(download(link)):
                path = direct_link
                break
        # cjm: took out title because description repeats it before additional desc
        doc += ['Title%d=%s' % (i, description.replace("commercial-free radio from SomaFM", ""))]
        doc += ['File%d=%s' % (i, path)]
        i += 1
    doc[1] = 'numberofentries=%d' % (i - 1,)
    doc += ['Version=2']
    output = '\n'.join(doc)

    # Write
    if options.output == '-':
        print output
    else:
        fileobj = file(options.output, 'w')
        fileobj.write(output)
        fileobj.close()

    # Success!
    sys.exit(0)


if __name__ == '__main__':
    main()
